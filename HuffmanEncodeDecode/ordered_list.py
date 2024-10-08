class Node:
    '''Node for use with doubly-linked list'''

    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None


class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.dummy = Node("dummy")
        self.dummy.next = self.dummy
        self.dummy.prev = self.dummy

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.dummy.next == self.dummy

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance.  Assume that all items added to your
           list can be compared using the < operator and can be compared for equality/inequality.
           Make no other assumptions about the items in your list'''
        new_node = Node(item)
        # if the list is empty
        if self.is_empty():
            new_node.prev = self.dummy
            self.dummy.next = new_node
            new_node.next = self.dummy
            self.dummy.prev = new_node
            return True

        temp = self.dummy.next
        # list has >= 1 items
        while temp != self.dummy and item > temp.item:
            # while the temp loop node is not the dummy node and the new node is greater than the temp loop node
            temp = temp.next
        if item == temp.item:
            return False

        # exits when new_node's item is greater than the temp's node, so found place  for new_node to be in
        new_node.prev = temp.prev  # sets the added node's previous value to the current node's previous value
        new_node.next = temp
        temp.prev.next = new_node
        temp.prev = new_node
        return True

    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list)
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        if self.is_empty():
            return False

        temp = self.dummy.next
        # list has >= 1 items
        while temp != self.dummy and temp.item != item:
            # while the temp loop node is not the dummy node and the new node not equal to the temp loop node
            temp = temp.next
        # if the temp node is not the item (item is not found), return False
        if temp == self.dummy:
            return False
        # item found, return True
        temp.prev.next = temp.next
        temp.next.prev = temp.prev
        temp.next = None
        temp.prev = None
        return True

    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        if self.is_empty():
            return None
        count = 0
        temp = self.dummy.next
        # list has >= 1 items
        while temp != self.dummy and temp.item != item:
            # while the temp loop node is not the dummy node and the temp node doesn't equal the item
            temp = temp.next
            count += 1
        # if the temp node is not the item (item is not found), return False
        if temp == self.dummy:
            return None
        return count

    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        if index < 0:
            raise IndexError

        count = 0
        temp = self.dummy.next
        # list has >= 1 items
        while temp != self.dummy and count != index:
            # while the temp loop node is not the dummy node and the count doesn't equal the index
            temp = temp.next
            count += 1
        if temp == self.dummy:
            raise IndexError
        # pop the value
        previous_node = temp.prev
        previous_node.next = temp.next
        temp.next.prev = previous_node
        temp.next = temp.prev = None
        return temp.item

    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        return self.search_helper(self.dummy.next, item)

    def search_helper(self, start_node, item):
        if start_node == self.dummy:
            return False
        if start_node.item == item:
            return True
        return self.search_helper(start_node.next, item)

    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        if self.is_empty():
            return []

        temp = self.dummy.next
        result_list = []
        # list has >= 1 items
        while temp != self.dummy:
            # while the temp loop node is not the dummy node
            result_list.append(temp.item)
            temp = temp.next
        return result_list

    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        if self.is_empty():
            return []

        return self.python_list_reversed_helper(self.dummy.next)

    def python_list_reversed_helper(self, start_node):
        if start_node == self.dummy:
            return []
        return self.python_list_reversed_helper(start_node.next) + [start_node.item]

    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.size_helper(self.dummy.next)

    def size_helper(self, node):
        if node == self.dummy:
            return 0
        return 1 + self.size_helper(node.next)
