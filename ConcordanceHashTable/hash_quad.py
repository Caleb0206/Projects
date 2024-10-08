import math
from fractions import Fraction
class HashTable:
    def __init__(self, table_size): # add appropriate attributes, NO default size
        ''' Initializes an empty hash table with a size that is the smallest
            prime number that is >= table_size (i.e. if 10 is passed, 11 will 
            be used, if 11 is passed, 11 will be used.)'''
        self.table_size = self.next_prime(table_size)
        self.keys = [None] * self.table_size
        self.values = [None] * self.table_size
        self.num_items = 0

    def insert(self, key, value=None):
        ''' Inserts an entry into the hash table (using Horner hash function to determine index, 
        and quadratic probing to resolve collisions).
        The key is a string (a word) to be entered, and value can be anything (Object, None, list, etc.).
        If the key is not already in the table, the key is inserted along with the associated value
        If the key is in the table, the new value replaces the existing value.
        If load factor is greater than 0.5 after an insertion, hash table size should be increased
        to the next prime greater than 2*table_size.'''

        initial_index = self.horner_hash(key) % self.table_size
        index = initial_index
        if self.keys[index] == key:         # if there is a repeat
            self.values[index] = value
            return
        if self.keys[index] is None:
            self.keys[index] = key
            self.values[index] = value
            self.num_items += 1
        else:

            i = 1
            while self.keys[index] != key and self.keys[index] is not None:

                index = (initial_index + i ** 2) % self.table_size
                i += 1
            # i = 1
            # while self.keys[(index + i**2) % self.table_size] != key and self.keys[(index + i**2) % self.table_size] is not None:
            #     i += 1
            #
            # index = (index + i**2) % self.table_size

            if self.keys[index] == key:     # check for repeats here as well
                self.values[index] = value
            else:
                self.keys[index] = key
                self.values[index] = value
                self.num_items += 1

        # Rehash:
        if self.get_load_factor() > 0.5:
            self.table_size = self.next_prime(2*self.table_size)
            tempKeys = self.keys
            tempVals = self.values

            hash_values = []  # Create an empty list to store hash values

            for k in tempKeys:
                if k is not None:
                    hash_val = self.horner_hash(k) % self.table_size
                    hash_values.append(hash_val)
                else:
                    hash_values.append(None)

            self.keys = [None] * self.table_size
            self.values = [None] * self.table_size


            for a in range(len(tempKeys)):

                if tempKeys[a] is not None:

                    initial_reIndex = hash_values[a]
                    reIndex = initial_reIndex
                    if self.keys[reIndex] is None:
                        self.keys[reIndex] = tempKeys[a]
                        self.values[reIndex] = tempVals[a]
                    else:
                        j = 1
                        while self.keys[reIndex] is not None:
                            reIndex = (initial_reIndex + j ** 2) % self.table_size
                            j += 1


                        self.keys[reIndex] = tempKeys[a]
                        self.values[reIndex] = tempVals[a]


    def horner_hash(self, key):
        ''' Compute the hash value by using Horner’s rule, as described in project specification.
            This method should not mod with the table size'''
        sum = 0
        n = min(len(key), 8)
        for i in range(n):
            sum += ord(key[i]) * 31**(n-1-i)

        return sum
    def isPrime(self, n): # copied from Geeks For Geeks
        # Function that returns True if n is prime, else returns False
        # Corner cases
        if (n <= 1):
            return False
        if (n <= 3):
            return True
        # This is checked so that we can skip
        # middle five numbers in below loop
        if (n % 2 == 0 or n % 3 == 0):
            return False
        for i in range(5, int(math.sqrt(n) + 1), 6):
            if (n % i == 0 or n % (i + 2) == 0):
                return False
        return True
    def next_prime(self, n):
        ''' Find the next prime number that is > n.'''
        # Copied from Geeks For Geeks
        # Base case
        if (n <= 1):
            return 2
        prime = n
        found = False
        # Loop continuously until isPrime returns
        # True for a number greater than n
        if not self.isPrime(n):
            while (not found):
                prime = prime + 1
                if (self.isPrime(prime) == True):
                    found = True
        return prime

    def in_table(self, key):
        ''' Returns True if key is in an entry of the hash table, False otherwise.'''
        index = self.horner_hash(key) % self.table_size
        initial_index = index
        i = 1
        while self.keys[index] != key and self.keys[index] is not None:
            index = (initial_index + i ** 2) % self.table_size
            i += 1

        return self.keys[index] == key

    def get_index(self, key):
        ''' Returns the index of the hash table entry containing the provided key. 
        If there is not an entry with the provided key, returns None.'''
        index = self.horner_hash(key) % self.table_size
        initial_index = index
        i = 1
        while self.keys[index] != key:
            index = (initial_index + i ** 2) % self.table_size
            i += 1
            if index == initial_index:  # Avoid infinite loop
                break
        if self.keys[index] == key:
           return index
        return None

    def get_all_keys(self):
        ''' Returns a Python list of all keys in the hash table.'''
        all_keys = []
        for item in self.keys:
            if item is not None:
                all_keys.append(item)
        return all_keys

    def get_value(self, key):
        ''' Returns the value associated with the key. 
        If key is not in hash table, returns None.'''
        index = self.get_index(key)
        if index is None:
            return None
        return self.values[index]

    def get_num_items(self):
        ''' Returns the number of entries in the table.'''
        return self.num_items

    def get_table_size(self):
        ''' Returns the size of the hash table.'''
        return self.table_size

    def get_load_factor(self):
        ''' Returns the load factor of the hash table (entries / table_size).'''
        return Fraction(self.num_items, self.table_size)

