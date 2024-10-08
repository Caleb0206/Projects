class Queue:
    '''Implements an array-based, efficient first-in first-out Abstract Data Type
       using a Python array (faked using a List)'''

    def __init__(self, capacity):
        '''Creates an empty Queue with a capacity'''
        self.capacity = capacity
        self.items = [None]*capacity
        self.num_items = 0
        self.front = -1       # set the index of front to -1 since queue is empty
        self.back = -1        # set the index of back to -1 since queue is empty


    def is_empty(self):
        '''Returns True if the Queue is empty, and False otherwise
           MUST have O(1) performance'''
        return self.num_items == 0


    def is_full(self):
        '''Returns True if the Queue is full, and False otherwise
           MUST have O(1) performance'''
        return self.num_items == self.capacity


    def enqueue(self, item):
        '''If Queue is not full, enqueues (adds) item to Queue
           If Queue is full when enqueue is attempted, raises IndexError
           MUST have O(1) performance'''
        if self.is_full() or self.num_items + 1 > self.capacity:
            raise IndexError
        if self.is_empty():
            self.items[0] = item
            self.front = 0
            self.back = 0
        else:
            self.back = (self.back + 1) % self.capacity # circle back to index 0 if self.back + 1 = self.capacity
            self.items[self.back] = item
        self.num_items += 1

    def dequeue(self):
        '''If Queue is not empty, dequeues (removes) item from Queue and returns item.
           If Queue is empty when dequeue is attempted, raises IndexError
           MUST have O(1) performance'''
        if self.is_empty():
            raise IndexError
        temp = self.items[self.front]
        if self.front + 1 < self.capacity:
            self.front = self.front + 1
        else:
            self.front = (self.front+1) % self.num_items # circle back to start 0
        self.num_items -= 1
        return temp


    def size(self):
        '''Returns the number of elements currently in the Queue, not the capacity
           MUST have O(1) performance'''
        return self.num_items

