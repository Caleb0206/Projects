import unittest
from hash_quad import *

class TestList(unittest.TestCase):
    ''' Code Coverage Missing: 105, 107, 113-114, 121, (covered by hash_quad_helper_tests.py) '''
    def test_01a(self):
        ht = HashTable(6)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_table_size(), 7)

    def test_01b(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_num_items(), 1)

    def test_01c(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertAlmostEqual(ht.get_load_factor(), 1/7)

    def test_01d(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_all_keys(), ["cat"])

    def test_01e(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.in_table("cat"), True)

    def test_01f(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_value("cat"), 5)

    def test_01g(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_index("cat"), 3)

    def test_02(self):
        ht = HashTable(7)
        ht.insert("a", 0)
        self.assertEqual(ht.get_index("a"), 6)
        ht.insert("h", 0)
        self.assertEqual(ht.get_index("h"), 0)
        ht.insert("o", 0)
        self.assertEqual(ht.get_index("o"), 3)
        ht.insert("v", 0) # Causes rehash
        self.assertEqual(ht.get_index("a"), 12)
        self.assertEqual(ht.get_index("h"), 2)
        self.assertEqual(ht.get_index("o"), 9)
        self.assertEqual(ht.get_index("v"), 16)

    def test_repeats(self):
        ht = HashTable(7)
        ht.insert("a", 0)
        self.assertEqual(ht.get_index("a"), 6)
        ht.insert("a", 77)
        self.assertEqual(ht.get_index("a"), 6)
        self.assertEqual(77, ht.get_value("a"))
        ht.insert("b", 0)
        ht.insert("c", 0)
        ht.insert("d", 0)
        ht.insert("e", 0)
        ht.insert("f", 0)
        ht.insert("g", 0)
        ht.insert("a", 22)
        self.assertEqual(22, ht.get_value("a"))
        self.assertEqual(7, ht.get_num_items())

    def test_not_found(self):
        ht = HashTable(7)
        self.assertIsNone(ht.get_index("a"))
        self.assertIsNone(ht.get_value("a"))

    def test_in_table(self):
        ht = HashTable(5)
        ht.insert("abcd")
        ht.insert("dcba")
        self.assertFalse(ht.in_table("bcda"))
        self.assertTrue(ht.in_table("dcba"))

        hash_table = HashTable(10)  # Create a hash table of size 10 (replace with your actual size)

        # Add some elements to the hash table
        hash_table.insert('apple', 10)
        hash_table.insert('banana', 15)
        hash_table.insert('orange', 20)

        # Test cases for elements present in the hash table
        self.assertTrue(hash_table.in_table('apple'))
        self.assertTrue(hash_table.in_table('banana'))
        self.assertTrue(hash_table.in_table('orange'))

        # Test cases for elements not present in the hash table
        self.assertFalse(hash_table.in_table('grape'))
        self.assertFalse(hash_table.in_table('pear'))

    def test_overflow(self):    #code coverage lines 46, 82-89
        ht = HashTable(7)
        ht.insert("aaaaaaaa")
        ht.insert("aaaaaaaaa", "five") # 9 a's
        ht.insert("aaaaaaaab", "fise") # 8 a's 1 b
        ht.insert("aaaaaaaaa", "six")  # 9 a's
        ht.insert("baaa")
        ht.insert("cdba", "seven")
        self.assertEqual(5, ht.get_num_items())
        ht.insert("caaa")
        ht.insert("cdba", "eight")
        ht.insert("aaac")
        self.assertFalse(ht.in_table("aaaaaaaac"))
        self.assertIsNone(ht.get_index("aaaaaaaac"))
        self.assertFalse(ht.in_table("aaaaaaaaaac"))
        self.assertTrue(ht.in_table("aaaaaaaab"))
        self.assertEqual(7, ht.get_num_items())

    def test_multiple_same_key(self):    #code coverage lines 46, 82-89
        ht = HashTable(7)
        ht.insert("a")
        ht.insert("a")
        ht.insert("a")
        ht.insert("a")
        self.assertEqual(1, ht.get_num_items())

if __name__ == '__main__':
   unittest.main()
