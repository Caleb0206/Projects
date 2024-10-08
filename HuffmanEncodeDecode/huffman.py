from ordered_list import *
from huffman_bit_writer import *
from huffman_bit_reader import *
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return type(other) == HuffmanNode and self.char == other.char
        
    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq == other.freq:
            return self.char < other.char
        return self.freq < other.freq

def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    file = open(filename)
    chars = [0] * 256
    fileString = file.read()

    for letter in fileString:
        chars[ord(letter)] += 1

    file.close()
    return chars

def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''

    ordered = OrderedList()
    # if len(char_freq) == 0:
    #     return
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            huff_node = HuffmanNode(i, char_freq[i])
            ordered.add(huff_node)

    while ordered.size() > 1:
        tempNode = ordered.pop(0)
        next = ordered.pop(0)
        temp_root = HuffmanNode(min(tempNode.char, next.char), tempNode.freq + next.freq)
        temp_root.left = tempNode
        temp_root.right = next
        ordered.add(temp_root)

    return ordered.pop(0)

def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    # print(vars(node))
    huff_array = ['']*256
    huff_array = create_code_helper(node, '', huff_array)
    #print(huff_array)
    return huff_array


def create_code_helper(root, zeroOne, array):
    if root is not None:
        if root.left is None and root.right is None and root.char is not None:
            array[root.char] = zeroOne
            return
        create_code_helper(root.left, zeroOne + '0', array)
        create_code_helper(root.right, zeroOne + '1', array)
    return array


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list associated with "aaabbbbcc", would return “97 3 98 4 99 2” '''

    header = ''
    for i in range(len(freqs)):
        if freqs[i] != 0: # and i != 10:    #ignore \n
            header += str(i) + ' ' + str(freqs[i]) + ' '

    return header.strip()


def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    # Read the file
    try:
        with open(in_file, 'r') as fileInput:
            data = fileInput.read()
            if not data:
                fileOutput = open(out_file, 'w')
                fileOutput.write('')
                fileOutput.close()
                # Bit Write the empty file
                out_file_compressed = out_file[0: out_file.index('.txt')] + '_compressed' + out_file[ out_file.index('.txt'):]
                bitWrite = HuffmanBitWriter(out_file_compressed)
                bitWrite.write_code('')
                bitWrite.close()
                return

    except FileNotFoundError:
        print("FileNotFoundError")
    freq = cnt_freq(in_file)


    out_file_compressed = out_file[0: out_file.index('.txt')] + '_compressed' + out_file[out_file.index('.txt'):]
    bitWrite = HuffmanBitWriter(out_file_compressed)

    # create the output file
    fileOutput = open(out_file, 'w')

    fileOutput.write(create_header(freq))
    bitWrite.write_str(str(create_header(freq)) + '\n')

    root = create_huff_tree(freq)
    code = create_code(root)
    strCode = ''
    if code is not None:

        for letter in data:
            if letter != '' and letter is not None and ord(letter) is not None:
                strCode += code[ord(letter)]

    # Regular File
    fileOutput.write('\r\n')
    fileOutput.write(strCode)

    # Huffman Bit Write
    bitWrite.write_code(strCode)
    fileOutput.close()
    bitWrite.close()

def parse_header(header_string):
    list_of_freq = [0] * 256
    temp_header = header_string.split(' ')
    i = 0
    while i < len(temp_header):
        # list_of_freq[ character ascii ] = frequency of character
        if '\n' in temp_header[i+1]:
            list_of_freq[int(temp_header[i])] = int(temp_header[i + 1].rstrip('\n'))
        else:
            list_of_freq[int(temp_header[i])] = int(temp_header[i+1])
        i += 2 # increment by two's
    return list_of_freq
def huffman_decode(encoded_file, decode_file):
    '''
    Decodes the encoded file and writes the decoded file as the actual string used to create the huffman tree.
    '''
    result = ""

    try:
        tempdata = HuffmanBitReader(encoded_file)
        tempdata.close()
    except FileNotFoundError:
        # tempdata.close()
        print("FileNotFoundError")
    data = HuffmanBitReader(encoded_file)
    header = data.read_str()
    if len(header) == 0:
        # print("EMPTY")
        fileOutput = open(decode_file, 'w')
        fileOutput.write('')
        fileOutput.close()
        data.close()
        return
    list_of_freq = parse_header(header)
    # count how many total characters there are
    counter = 0
    for i in list_of_freq:
        if i != 0:
            counter += i
    # creates the huffman tree
    tree_root = create_huff_tree(list_of_freq)
    temp = tree_root

    while counter != 0:
        if temp.left is None and temp.right is None:
            # if the node is a leaf
            result += chr(temp.char) # add the char of the node to the resulting string
            temp = tree_root # reset temp back to the root
            counter -= 1    # decrease the counter
        else:
            # traverse the tree
            if data.read_bit():     # 1
                temp = temp.right
            else:                   # 0
                temp = temp.left
    data.close()
    fileOutput = open(decode_file, 'w')
    fileOutput.write(result)
    fileOutput.close()


