import unittest
import subprocess
from concordance import *


class TestList(unittest.TestCase):


    def test_01(self):
        conc = Concordance()
        conc.load_stop_table("stop_words.txt")
        conc.load_concordance_table("file1.txt")
        conc.write_concordance("file1_con.txt")
        err = subprocess.call("diff -wb file1_con.txt file1_sol.txt", shell = True)
        self.assertEqual(err, 0)


    def test_02(self):
        conc = Concordance()
        conc.load_stop_table("stop_words.txt")
        conc.load_concordance_table("file2.txt")
        conc.write_concordance("file2_con.txt")
        err = subprocess.call("diff -wb file2_con.txt file2_sol.txt", shell = True)
        self.assertEqual(err, 0)


    # 0.021s        0.015    0.033     0.0456
    def test_declaration(self):
        conc = Concordance()
        conc.load_stop_table("stop_words.txt")
        conc.load_concordance_table("declaration.txt")
        conc.write_concordance("declaration_con.txt")
        err = subprocess.call("diff -wb declaration_con.txt declaration_sol.txt", shell = True)
        self.assertEqual(err, 0)

    # passed!! in 1.933s            1.953             1.896s
    # def test_dictionary(self):
    #     conc = Concordance()
    #     conc.load_stop_table("stop_words.txt")
    #     conc.load_concordance_table("dictionary_a-c_new.txt")
    #     conc.write_concordance("dictionary_a-c_con.txt")
    #     err = subprocess.call("diff -wb dictionary_a-c_con.txt dictionary_a-c_sol.txt", shell = True)
    #     self.assertEqual(err, 0)

    # passed in 4.525s          5.066s   4.849s       4.309 s       3.184 s
    # def test_WAP(self):
    #     conc = Concordance()
    #     conc.load_stop_table("stop_words.txt")
    #     conc.load_concordance_table("War_And_Peace.txt")
    #     conc.write_concordance("WAP_con.txt")
    #     err = subprocess.call("diff -wb WAP_con.txt War_And_Peace_sol.txt", shell = True)
    #     self.assertEqual(err, 0)

    def test_no_stop_file(self):
        conc = Concordance()
        conc.load_concordance_table("file1.txt")
        conc.write_concordance("file1_nostop_con.txt")
        err = subprocess.call("diff -wb file1_nostop_con.txt file1_nostop_soln.txt", shell = True)
        self.assertEqual(err, 0)

    def test_different_stop_file(self):
        conc = Concordance()
        conc.load_stop_table("diff_stop_words.txt")
        conc.load_concordance_table("myfile.txt")
        conc.write_concordance("myfile_con.txt")
        err = subprocess.call("diff -wb myfile_con.txt myfile_sol.txt", shell = True)
        self.assertEqual(err, 0)

    # passed in 1.406s          7.136s         7.068s        60.728    59.941    58.920    59.456
    # def test_the_file(self):
    #     conc = Concordance()
    #     # conc.load_stop_table("stop_words.txt")
    #     conc.load_concordance_table("file_the.txt")
    #     conc.write_concordance("file_the_con.txt")
    #     err = subprocess.call("diff -wb file_the_con.txt file_the_sol.txt", shell = True)
    #     self.assertEqual(err, 0)

    def test_number_file(self):
        ''' Edge Case: Test fiile with numbers only '''
        conc = Concordance()
        conc.load_concordance_table("numbers.txt")
        conc.write_concordance("numbers_con.txt")
        err = subprocess.call("diff -wb numbers_con.txt numbers_sol.txt", shell=True)
        self.assertEqual(err, 0)

    def test_special_file(self):
        ''' Edge Case: Test special characters '''
        conc = Concordance()
        conc.load_concordance_table("special.txt")
        conc.write_concordance("special_con.txt")
        err = subprocess.call("diff -wb special_con.txt special_sol.txt", shell=True)
        self.assertEqual(err, 0)


    def test_nonexistent(self):
        conc = Concordance()
        self.assertRaises(FileNotFoundError, conc.load_stop_table, "notexistent.txt")
        self.assertRaises(FileNotFoundError, conc.load_concordance_table, "notexistent.txt")
        self.assertIsNone(conc.write_concordance("none_con.txt"))   # dont add to git
        err = subprocess.call("diff -wb file1_nostop_con.txt file1_nostop_soln.txt", shell = True)
        self.assertEqual(err, 0)
    def test_empty_file(self):
        emptyconc = Concordance()
        emptyconc.load_stop_table("stop_words.txt")
        emptyconc.load_concordance_table("emptyfile.txt")
        emptyconc.write_concordance("emptyfile_con.txt")
        err = subprocess.call("diff -wb emptyfile_con.txt emptyfile_soln.txt", shell = True)
        self.assertEqual(err, 0)

        
if __name__ == '__main__':
    unittest.main()
