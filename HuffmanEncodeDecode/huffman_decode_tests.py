import unittest
from huffman import *
import subprocess

class TestList(unittest.TestCase):
    def test_01a_test_file1_parse_header(self):
        f = HuffmanBitReader('file1_compressed_soln.txt')
        header = f.read_str()        
        f.close()
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.compare_freq_counts(parse_header(header), expected)
        
    def test_01_test_file1_decode(self):
        huffman_decode("file1_compressed_soln.txt", "file1_decoded.txt")
        err = subprocess.call("diff -wb file1.txt file1_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_not_exist_decode(self):
        self.assertRaises(FileNotFoundError, huffman_decode, "notexist.txt", "notexist.txt")

    def test_empty_decode(self):
        huffman_decode("empty_out_compressed_soln.txt", "empty_decoded.txt")
        err = subprocess.call("diff -wb empty_file.txt empty_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_02_test_file2_decode(self):
        huffman_decode("file2_compressed_soln.txt", "file2_decoded.txt")
        err = subprocess.call("diff -wb file2.txt file2_decoded.txt", shell = True)
        self.assertEqual(err, 0)
    def test_03_test_file3_decode(self):
        huffman_decode("file3_soln.txt", "file3_decoded.txt")
        err = subprocess.call("diff -wb file3.txt file3_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_single_char_decode(self):
        huffman_decode("single_char_soln.txt", "single_char_decoded.txt")
        err = subprocess.call("diff -wb single_char.txt single_char_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_multiline_decode(self):
        huffman_decode("multiline_compressed_soln.txt", "multiline_decoded.txt")
        err = subprocess.call("diff -wb multiline.txt multiline_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def test_dec_decode(self):
        huffman_decode("declaration_compressed_soln.txt", "declaration_decoded.txt")
        err = subprocess.call("diff -wb declaration.txt declaration_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    # def test_WAP_decode(self):
    #     huffman_decode("file_WAP_compressed_soln.txt", "file_WAP_decoded.txt")
    #     err = subprocess.call("diff -wb file_WAP.txt file_WAP_decoded.txt", shell = True)
    #     self.assertEqual(err, 0)

    def compare_freq_counts(self, freq, exp):
        for i in range(256):
            stu = 'Frequency for ASCII ' + str(i) + ': ' + str(freq[i])
            ins = 'Frequency for ASCII ' + str(i) + ': ' + str(exp[i])
            self.assertEqual(stu, ins)
                
if __name__ == '__main__': 
   unittest.main()
