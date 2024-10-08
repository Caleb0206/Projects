import unittest
from hash_quad import *

class TestList(unittest.TestCase):
    ''' Covers lines 101-134 '''
    def test_is_prime(self):
        ht = HashTable(7)
        self.assertFalse(ht.isPrime(1))
        self.assertFalse(ht.isPrime(0))
        self.assertFalse(ht.isPrime(6))
        self.assertFalse(ht.isPrime(49))
        self.assertTrue(ht.isPrime(2))

    def test_next_prime(self):
        ht = HashTable(7)
        self.assertEqual(2, ht.next_prime(1))
        self.assertEqual(7, ht.next_prime(6))
if __name__ == '__main__':
   unittest.main()
