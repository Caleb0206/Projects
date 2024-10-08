# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <sys/wait.h>
# include <fcntl.h>

int loadArrays(FILE *filePtr, char **fileNames, char **urlStrings, int *timeDelay);
void runForkChildren(int maxProcesses, int numOfLines, char **fileNames, char **urlStrings, int *timeDelay);

typedef struct {
        pid_t pid;
        int line_num;
} LineNumNode;

