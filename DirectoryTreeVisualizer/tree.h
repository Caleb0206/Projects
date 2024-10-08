# include <stdio.h>
# include <dirent.h>
# include <string.h>
# include <sys/stat.h>
# include <stdlib.h>
#include<unistd.h>

void runTree(DIR *dir, char *rootDir, char *args, int indent, int *numOfD, int *numOfF, char *preChars);
int compareEntryNames(const void *a, const void *b);

