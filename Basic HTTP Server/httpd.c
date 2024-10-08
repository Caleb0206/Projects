# include "httpd.h"

int main(int argc, char *argv[])
{
	// Server Port between 1024 and 65535
	if(argc != 2)
	{
		fprintf(stderr, "Usage: ./a4download <int between 1024 and 65535>\n");
		return 1;
	}
	if(atoi(argv[1]) < 1024 || atoi(argv[1]) > 65535)
	{
		fprintf(stderr, "Integer between 1024 and 65535\n");
		return 1;
	}
	int port = atoi(argv[1]);
		
	// create TCP socket for the server to listen
	int server_socket = socket(AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in server_sa;
	memset(&server_sa, 0, sizeof(server_sa));
	server_sa.sin_family = AF_INET;
	server_sa.sin_port = htons(port);
	server_sa.sin_addr.s_addr = htonl(INADDR_ANY);  // listen on any network device

	// bind server socket to server address/port
	if (bind(server_socket, (struct sockaddr *) &server_sa, sizeof(server_sa)) == -1) {
		printf("Error: bind()\n");
		return EXIT_FAILURE;
	}

	// configure socket's listen queue
	if (listen(server_socket, DEFAULT_BACKLOG) == -1) {
		printf("Error: listen()\n");
		return EXIT_FAILURE;
	}

	printf("Listening on port: %d\n", port);

	// infinite loop to accept client requests
	for(;;) 
	{
		struct sockaddr_in client_sa;
		socklen_t client_sa_len = sizeof(client_sa); // initialize length variable
		char client_addr[INET_ADDRSTRLEN];

		int client_socket = accept(server_socket, (struct sockaddr *) &client_sa, &client_sa_len);
		if(client_socket == -1)
		{
			// failed to create client socket, continue listening after
			perror("accept socket error");
			continue;
		}
		
		inet_ntop(AF_INET, &(client_sa.sin_addr), client_addr, INET_ADDRSTRLEN);  // convert client IP address into printable string
		
		// need to malloc in case of scenario clien_socket gets overwritten when multiple threads run at same time
                int *client_socket_ptr = malloc(sizeof(int));
                if (client_socket_ptr == NULL) {
                        perror("Error allocating memory");
                        close(client_socket);
                        continue;
                }
                *client_socket_ptr = client_socket;

		pthread_t client_thread;
		if( pthread_create(&client_thread, NULL, handle_client_request, client_socket_ptr) != 0)
		{
			char *error_response = "HTTP/1.1 500 Internal Error: pthread\r\n";
	                send(client_socket, error_response, strlen(error_response), 0);
                	close(client_socket);
			free(client_socket_ptr);

			return EXIT_FAILURE;
		}
		pthread_detach(client_thread);
	}

	return EXIT_SUCCESS;
}

void *handle_client_request(void *param) {
	int client_socket = *((int *) param);
	char buf[MAXLENGTH+1];
	memset(buf, 0, MAXLENGTH+1);
	ssize_t bytes_read = recv(client_socket, buf, sizeof(buf), 0);
	
	char *error_response = NULL; // initialize a string for error response

	if (bytes_read <= 0) 
	{
		close(client_socket);
		return NULL;
	}
	buf[bytes_read-2] = '\0';  // remove "\r\n"
	
	// extract the first line of the request by finding where the first "\r\n" is
	char *request_line_end = strstr(buf, "\r\n");
    	if (request_line_end == NULL) 
	{
        	error_response = "HTTP/1.1 400 Bad Request\r\n";
        	send(client_socket, error_response, strlen(error_response), 0);
        	close(client_socket);
	        return NULL;
	}
	
	// print out the request on the server side
        printf("%s\r\n", buf);

	// null-terminate the request line (so now it's just parsing the first line)
    	*request_line_end = '\0';
	
	// parse the first line by spaces
    	char request[10] = {0}, path[100]= {0}, http_version[10] = {0};
	
	if(sscanf(buf, "%s %s %s", request, path, http_version) != 3 ||
		       	*request == 0 || *path == 0 || strcmp(http_version, "HTTP/1.1") != 0)
	{
		error_response = "HTTP/1.1 400 Bad Request\r\n";
                send(client_socket, error_response, strlen(error_response), 0);
                close(client_socket);
                return NULL;
	}
	char *file_path = path + 1; // ignore the '\' in front of the actual file
	
	if (strcmp(request, "GET") == 0) 
	{
		runGet(client_socket, file_path);
	} 
	else if (strcmp(request, "HEAD") == 0) 
	{
		runHead(client_socket, file_path);
	}
	else 
	{
		// Tested with :  curl -v -X POST http://localhost:8080/file.txt
		error_response = "HTTP/1.1 501 Not Implemented\r\n";
		send(client_socket, error_response, strlen(error_response), 0);
		close(client_socket);
		return NULL;
	}
	close(client_socket);
	return NULL;
}

void runGet(int clientSocket, char* filePath)
{
	// Delay feature
	char *delay_ptr = strstr(filePath, "delay"); ;
	if(delay_ptr != NULL)
        {
                int seconds = atoi(delay_ptr + 5 + 1); // parses "delay/##" to just "##"
                sleep(seconds);
		
		
		char response[MAXLENGTH];
	       	
		// Print a HEAD request but with content length 0
	       	snprintf(response, sizeof(response),
                	"HTTP/1.1 200 OK\r\n"
			"Content-Type: text/html\r\n"
			"Content-Length: 0\r\n"
			"\r\n");

	        send(clientSocket, response, strlen(response), 0);
		
		return;
	}      
	const char *error_response = "HTTP/1.1 404 Not Found\r\n";
	// GET html	
	// every response needs a header, so runHead
	if(runHead(clientSocket, filePath) == 0) // if runHead has 404 error, return out of this function
		return;

	FILE *file = fopen(filePath, "r");
        if (file == NULL)
        {
		// File not found
                send(clientSocket, error_response, strlen(error_response), 0);
                return;
        }
        char file_buf[MAXLENGTH];
        ssize_t bytes_read;

	// send out / print contents of the file
        while ((bytes_read = fread(file_buf,1, sizeof(file_buf), file)) > 0)
        {
                send(clientSocket, file_buf, bytes_read, 0);
        }

        fclose(file);
}
int runHead(int clientSocket, char* filePath)
{
	// HEAD html 
	// Test: curl -v -I http://localhost:8080/file.txt
	struct stat file_stat;
	if (strstr(filePath, "..") != NULL || stat(filePath, &file_stat) < 0) 
	{
		// File not found
        	const char *response = "HTTP/1.1 404 Not Found\r\n\r\n";
        	send(clientSocket, response, strlen(response), 0);
	        return 0; // return false
	}

	// file found, can proceed and print its info
	char response[MAXLENGTH];
    	snprintf(response, sizeof(response),
        	"HTTP/1.1 200 OK\r\n"
       		"Content-Type: text/html\r\n"
             	"Content-Length: %ld\r\n"
             	"\r\n",
             	file_stat.st_size);

	send(clientSocket, response, strlen(response), 0);
	return 1; // return success
}


