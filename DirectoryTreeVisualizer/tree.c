# include "tree.h" 


int main(int argc, char* argv[])
{
	DIR *dirPtr = NULL;
	int dirCount = 0;
       	int fileCount = 0;
	char theArgs[6] = {0};
	char *rootPath;
	struct stat rootDirStat;
	
	char preChars[1024] = {0};


	if(argc == 1)
	{
		printf("./tree <directory name>\n");
		return 1;
	}
	
	if(argc == 3)
	{
		// one arg
		rootPath = argv[2];
		strcpy(theArgs, argv[1]);
	}
	else if(argc == 4)
	{
		// two args
		rootPath = argv[3];
		strcpy(theArgs, argv[1]);
		strcat(theArgs, argv[2]);
		
	}
	else
	{
		// no args
		rootPath = argv[1];
	}
        stat(rootPath, &rootDirStat);
	
	if(strstr(theArgs, "s") == NULL)
		printf("%s\n", rootPath);
	else
		printf("[%11ld]  %s\n", (long)rootDirStat.st_size, rootPath); 	
	
	chdir(rootPath);

	runTree(dirPtr, ".", theArgs, 0, &dirCount, &fileCount, preChars);	
	closedir(dirPtr);


	printf("\n%d directories, %d files\n", dirCount, fileCount);

	return 0;
}
int compareEntryNames(const void *a, const void *b)
{
	struct dirent **entryA = (struct dirent **)a;
	struct dirent **entryB = (struct dirent **)b;

	return strcmp((*entryA)->d_name, (*entryB)->d_name);
}
void runTree(DIR *dir, char *rootDir, char *args, int indent, int *numOfD, int *numOfF, char *preChars)
{
        struct dirent *entry; // pointer to the current directory/entry
	struct dirent **entries = NULL; // pointer to an array of pointers to files/directories
	int countEntries = 0; // number of total entries (size of the entries array)
	
	DIR *next;	
        char *tempName;
	struct stat currentDirStat;
	char currentPath[1024];

	// for loop variables
	int i;
	int j;


	if((dir = opendir(rootDir)) == NULL)
        {
		printf("Error: Cannot open directory\n");
		return;
	}
        while((entry = readdir(dir)) != NULL) 
	{
		tempName = entry->d_name;
                       
		snprintf(currentPath, sizeof(currentPath), "%s/%s", rootDir, tempName);

		if(stat(currentPath, &currentDirStat) != -1)
		{
			if(strstr(args, "a") == NULL && tempName[0] != '.')	
			{
				// the "-a" arg is not in use, do not store the hidden files
				entries = realloc(entries, (countEntries + 1) * sizeof(struct dirent *));
				
				if (entries == NULL)
				{
					fprintf(stderr, "Error: Failed to allocate memory\n");
			                exit(EXIT_FAILURE);
				}
				entries[countEntries] = entry;
				countEntries++;
			}
			else if(strstr(args,"a") != NULL)
			{
				// if "-a" IS in use, DO store the hidden files
				entries = realloc(entries, (countEntries + 1) * sizeof(struct dirent *));
                                if (entries == NULL)
                               	{
					fprintf(stderr, "Error: Failed to allocate memory\n");
			                exit(EXIT_FAILURE);
                                }
                                entries[countEntries] = entry;
                                countEntries++;	
			}
		}
		else
			perror("Error: stat\n");
             
	}
	qsort(entries, countEntries, sizeof(struct dirent *), compareEntryNames);
	
	// Print all the entries from the sorted array
	for (i = 0; i < countEntries; i++)
	{
		if(strcmp(entries[i]->d_name, "..") == 0 || strcmp(entries[i]->d_name, ".") == 0 )
			continue;
		entry = entries[i];
		
		snprintf(currentPath, sizeof(currentPath), "%s/%s", rootDir, entry->d_name);
		stat(currentPath, &currentDirStat);
		
		for(j = 0; j < indent * 4; j+=4)
		{
			printf("%c%c%c%c", preChars[j], preChars[j+1], preChars[j+2], preChars[j+3]);
		}
		if(i+1 == countEntries)
		{
			printf("`");
			preChars[indent * 4] = ' ';
                        preChars[indent * 4 + 1] = ' ';
                        preChars[indent * 4 + 2] = ' ';
                        preChars[indent * 4 + 3] = ' ';
		}
		else
		{
			printf("|");
			preChars[indent * 4] = '|';
                        preChars[indent * 4 + 1] = ' ';
                        preChars[indent * 4 + 2] = ' ';
                        preChars[indent * 4 + 3] = ' ';
		}
		if(strstr(args, "s") == NULL)
		{
			printf("-- %s\n", entry->d_name);
		}
		else
		{
			// print the byte size
			 printf("-- [%11ld]  %s\n", (long)currentDirStat.st_size, entry->d_name);
		}

		if(S_ISDIR(currentDirStat.st_mode))
		{
			// increase amount of directories count
			(*numOfD)++;
			next = NULL;

			runTree(next, currentPath, args, indent+1, numOfD, numOfF, preChars);
			closedir(next);
		}
		else if(S_ISREG(currentDirStat.st_mode))
		{
			if(strstr(args,"a") != NULL)
			{
				// if arg has "a", count every file
				(*numOfF)++;
			}
			else if( (entry->d_name)[0] != '.')
			{
				// if arg does not have a, don't count hidden files
				(*numOfF)++;
			}
		}
	}
	closedir(dir);

	// free allocated memory
	free(entries);
}

