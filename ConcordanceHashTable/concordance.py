from hash_quad import *
import string

class Concordance:
    ''' Code Coverage Missing: 105, 107, 121, 157, 160, 175, 180, 184 (covered by hash_quad_tests.py and hash_quad_helper_tests.py) '''
    def __init__(self):
        self.stop_table = None          # hash table for stop words
        self.concordance_table = None   # hash table for concordance

    def load_stop_table(self, filename):
        """ Read stop words from input file (filename) and insert each word as a key into the stop words hash table.
        Starting size of hash table should be 191: self.stop_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        self.stop_table = HashTable(191)
        try:
            with open(filename, 'r') as fileInput:
                for line in fileInput:
                    if len(line.strip()) > 0:
                        line = line.strip()
                        self.stop_table.insert(line.lower())
        except FileNotFoundError:
            raise FileNotFoundError


    def load_concordance_table(self, filename):
        """ Read words from input text file (filename) and insert them into the concordance hash table,
        after processing for punctuation, numbers and filtering out words that are in the stop words hash table.
        (The stop words hash table could possibly be None.)
        Do not include duplicate line numbers (word appearing on same line more than once, just one entry for that line)
        Starting size of hash table should be 191: self.concordance_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        self.concordance_table = HashTable(191)
        lines = []
        try:
            with open(filename, 'r') as fileInput:
                lines = fileInput.readlines()
        except FileNotFoundError:
            raise FileNotFoundError
        lineNum = 0
        for line in lines:
            lineNum += 1
            temp_line = self.helper_remove(line).lower()
            tempList = temp_line.split()

            used_table = HashTable(len(tempList)*2)
            for token in tempList:
                token = token.strip()
                if self.stop_table and self.stop_table.in_table(token):
                    continue
                elif not used_table.in_table(token) and token.isalpha():  # check for repeated line numbers (same word)

                    used_table.insert(token, lineNum)
                    if self.concordance_table.in_table(token):  # repeated word, different line number
                        existing_lines_list = self.concordance_table.get_value(token)
                        existing_lines_list.append(lineNum)
                        self.concordance_table.insert(token, existing_lines_list)
                    else:   # new word, add the word and its line number
                        self.concordance_table.insert(token, [lineNum])
                    '''
                    used_table.insert(token, {str(lineNum)})
                    # print(token, used_table.get_value(token))
                    if self.concordance_table.in_table(token):
                        existing_lines_list = self.concordance_table.get_value(token)
                        existing_lines_dictionary = used_table.get_value(token)
                        existing_lines_dictionary.add(str(lineNum))
                        # print(lineNum, existing_lines)
                        # print(lineNum, existing_lines_dictionary, lineNum not in existing_lines_dictionary)
                        if lineNum not in existing_lines_dictionary:
                            existing_lines_list.append(lineNum)
                            self.concordance_table.insert(token, existing_lines_list)
                    '''
        fileInput.close()
    def helper_remove(self, str):
        str = str.replace("'", "")
        for char in string.punctuation:
            str = str.replace(char, " ")

        return str.strip()



    def write_concordance(self, filename):
        """ Write the concordance entries to the output file(filename)
        See sample output files for format."""
        fileOutput = open(filename, 'w')
        keys = self.concordance_table.get_all_keys()
        keys.sort()
        for item in keys:
            if item is not None:
                out = item + ": " + ' '.join(map(str, self.concordance_table.get_value(item)))
                fileOutput.write(out + "\n")
        fileOutput.close()
