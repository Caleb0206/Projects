# include "a4download.h"

int main(int argc, char *argv[])
{
	char *files[100];
	char *urls[100];
	int time[100] = {0};
	int line_count = 0;
	
	int max_processes;
	if (argc != 3)
	{
		fprintf(stderr, "Invalid usage: ./a4download <file name> <postive int>\n");
		return EXIT_FAILURE;
	}
	if (atoi(argv[2]) < 0)
	{
		fprintf(stderr, "Invalid argument. Number > 0\n");
		return EXIT_FAILURE;
	}	
	FILE *downloadsPtr = fopen(argv[1], "r");
	
	if (downloadsPtr == NULL) {
        	perror("Error opening file");
        	return EXIT_FAILURE;
    	}

	// after checking file is valid and integer is valid, can proceed
	max_processes = atoi(argv[2]);
	
	// load the file names, urls, and time delays and return the number of lines in the download file
	line_count = loadArrays(downloadsPtr, files, urls, time);

	fclose(downloadsPtr);
	
	// Run fork children processes
	runForkChildren(max_processes, line_count, files, urls, time);

	// Free parsed array memories 
	for(int j = 0; j < line_count; j++)
	{
		free(files[j]);
        	free(urls[j]);
	}
	

}

// function loads the file names, urls, and times to download. returns the number of lines in the file
int loadArrays(FILE *filePtr, char **fileNames, char **urlStrings, int *timeDelay)
{
        int numOfLines = 0;
        char line[1024] = {0};
        while(fgets(line, sizeof(line), filePtr) != NULL)
        {
                // Remove the newline character from the line if it exists
                line[strcspn(line, "\n")] = '\0';

                // separate the line by spaces
                char *token = strtok(line, " ");

                // load all the arras with the read values
                if (token != NULL) {
                    fileNames[numOfLines] = strdup(token); // mallocs memory
                    token = strtok(NULL, " ");
                }
                if (token != NULL) {
                    urlStrings[numOfLines] = strdup(token); // mallocs memory
                    token = strtok(NULL, " ");
                }

                if (token != NULL) {
                    timeDelay[numOfLines] = atoi(token);
                } else {
                    timeDelay[numOfLines] = 0; // no max number of seconds provided
                }

                numOfLines++;
        }

        return numOfLines;
}
void runForkChildren(int maxProcesses, int numOfLines, char **fileNames, char **urlStrings, int *timeDelay)
{
        int current_processes = 0;
        LineNumNode lineNodeArr[100];

        // for loop vars
        int i = 0, j = 0;

        while(i < numOfLines || current_processes > 0)
        {
                // make a new child process if current amount of processes is less than the maximum
                while(i < numOfLines && current_processes < maxProcesses)
                {
                        pid_t pid = fork();
                        if (pid == -1)
                        {
                            perror("fork");
                            return;
                        }
                        else if (pid == 0)
                        {
                                // child process

                                // convert the time in seconds to a string
                                char time_str[12];
                                snprintf(time_str, sizeof(time_str), "%d", timeDelay[i]);

                                // "-s" is to hide the curl command's output
                                execlp("curl", "curl", "-m", time_str, "-o", fileNames[i], "-s", urlStrings[i], (char *)NULL);
                        }
                        else
                        {
                                // parent process
                                printf("process %d processing line %d\n", pid, i + 1);

                                // store process pid and line number    
                                lineNodeArr[i].pid = pid;
                                lineNodeArr[i].line_num = i + 1;

                                i++;
                                current_processes++;
                        }
                }
                // see if the child status has exited
                int status;
                pid_t exited_pid = wait(&status);

                if(exited_pid > 0)
                {
                        int line_number = -1;

                        // Find the line number for the exited pid
                        for (j = 0; j < i; j++)
                        {
                                if (lineNodeArr[j].pid == exited_pid)
                                {
                                        line_number = lineNodeArr[j].line_num;
                                        break;
                                }
                        }

                        // if the child process has exited, decrement current_processes
                        current_processes--;

                        if(line_number != -1)
                        {

                                if (WIFEXITED(status))
                                {
                                        if (WEXITSTATUS(status) == 0)
                                                printf("process %d processing line %d exited normally\n", exited_pid, line_number);
                                        else
                                        {
                                                fprintf(stderr, "process %d processing line %d terminated with exit status: %d\n",
                                                                exited_pid, line_number, WEXITSTATUS(status));
                                        }
                                }
                        }
                }
        }
}
