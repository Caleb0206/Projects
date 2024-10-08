#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>
#include <stddef.h>
#include <sys/stat.h>

# define MAXLENGTH 1000
# define DEFAULT_BACKLOG 10

void *handle_client_request(void *param);
int runHead(int clientSocket, char* filePath);
void runGet(int clientSocket, char* filePath);


