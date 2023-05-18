from bisect import bisect_left
from collections import Counter
import sys
from itertools import chain
from math import ceil

class HashTable:
    """This class defines an ordered map from sets to values,
    implemented using a hash table.

    It supports the methods put, get, containsKey, size and isEmpty.
    It does not support removing items, though.

    It can also be used like a Python dictionary:

    >>> table = HashTable()
    >>> table[3] = "hello"   # This calls table.put(3, "hello")
    >>> table[3]             # This calls table.get(3)
    "hello"
    >>> for key in table: print(key) # This calls table.iter()
    hello
    >>> len(table)           # This calls table.size()
    1"""

    # The maximum load factor
    _max_load_factor = 0.5
    # How much to grow the array on resizing
    _growth_factor = 2
    # The initial capacity
    _initial_capacity = 3

    # The hash table - one array for keys and one for values
    _keys: list
    _values: list
    # How many key-value pairs are in the hash table
    _size: int

    def __init__(self):
        """Creates an empty map."""

        self._create_table(self._initial_capacity)

    def _create_table(self, capacity):
        """Initialise the hash table with a given capacity."""

        self._keys = [None] * capacity
        self._values = [None] * capacity
        self._size = 0

    def _load_factor(self):
        """Returns the current load factor of the hash table."""

        return self._size / len(self._keys)

    def isEmpty(self) -> bool:
        """Returns true if the map is empty."""

        return self._size == 0

    def containsKey(self, key) -> bool:
        """Does the map contain the given key?"""

        return self.get(key) is not None

    def get(self, key):
        """Returns the value associated with the given key."""

        index = self._probe(key)
        if self._keys[index] is None:
            return None
        else:
            return self._values[index]

    def put(self, key, value):
        """Inserts the specified key-value pair into the map,
        overwriting the old value with the new value if the map
        already contains the specified key."""
        index = self._probe(key)
        if self._keys[index] is None:
            self._size += 1
        self._keys[index] = key
        self._values[index] = value
        if self._load_factor() > self._max_load_factor:
          self._resize()

        

    def _probe(self, key):
        """Returns the index where key should be stored in the hash
        table. If key is already present, returns the position where
        it is stored. Otherwise, returns the position of the free
        space which should be used."""
        index = hash(key) % len(self._keys)
        while True:
            if self._keys[index] == key or self._keys[index] is None:
                return index
            index = (index + 1) % len(self._keys)





    def _resize(self):
        """Grow the array to the next size up."""

        # Save the old key-value pairs
        keys = self._keys
        values = self._values

        # Create an empty hash table
        self._create_table(ceil(len(self._keys) * self._growth_factor))

        # Store the old key-value pairs in the new table
        for i in range(len(keys)):
            if keys[i] is not None:
                self.put(keys[i], values[i])

    def __iter__(self):
        """Iterates through all keys in the map, in an undefined order."""

        for key in self._keys:
            if key is not None:
                yield key

    def size(self) -> int:
        """Returns the number of key-value pairs in the map."""

        return self._size

    def statistics(self) -> str:
        """Returns some statistics about the hash table (for debugging)."""

        avg_distance, max_distance = self._average_and_max_distance()
        return "Hash table, size %d, capacity %d, load factor %.2f, average distance %.2f, max distance %d, max cluster size %d" % (self.size(), len(self._keys), self._load_factor(), avg_distance, max_distance, self._max_cluster_size())

    def _average_and_max_distance(self):
        """Returns the average and maximum distance of an item from its
        preferred position (for debugging)."""

        distances = []
        for i, key in enumerate(self._keys):
            if key is not None:
                distances.append((i - hash(key)) % len(self._keys))
        if distances:
            return sum(distances)/len(distances), max(distances)
        else:
            return 0, 0

    def _max_cluster_size(self):
        """Returns the maximum cluster size (for debugging)."""

        if len(self._keys) == 0: return 0

        result = 0
        i = 0
        n = len(self._keys)

        while True:
            # Find the size of the current cluster.
            cluster_size = 0
            # "cluster_size < n" is to make sure the loop terminates
            # when all the hash buckets are full.
            while self._keys[i % n] is not None and cluster_size < n:
                cluster_size += 1
                i += 1
            i += 1

            result = max(result, cluster_size)
            if i >= n: break

        return result

    def check(self):
        """Check that the hash table is valid."""

        self._check_keys_unique()
        self._check_size_field_correct()
        self._check_locations_correct()
        self._check_load_factor_respected()

    def _check_size_field_correct(self):
        """Checks that self._size has the correct value."""

        actual_size = len([key for key in self._keys if key is not None])
        if self._size != actual_size:
            raise AssertionError("_size field is incorrect: map contains %d keys but self._size=%d" % (actual_size, self._size))

    def _check_keys_unique(self):
        """Checks that each key only appears once."""

        c = Counter(self._keys)

        for key in c:
            if key is not None and c[key] > 1:
                raise AssertionError("There are duplicate keys: Key %s appears %d times" % (key, c[key]))

    def _check_locations_correct(self):
        """Checks that each key is stored at the correct location."""

        for pos, key in enumerate(self._keys):
            if key is not None:
                preferred = hash(key) % len(self._keys)

                if pos >= preferred:
                    candidates = range(preferred, pos)
                else:
                    candidates = chain(range(preferred, len(self._keys)), range(pos))

                for cell in candidates:
                    if self._keys[cell] is None:
                        raise AssertionError("A key is stored at the wrong location: key %s is stored at index %d but should be stored at index %d (starting index for search is %d)" % (key, pos, cell, preferred))

    def _check_load_factor_respected(self):
        """Checks that the load factor does not exceed _max_load_factor."""

        if self._load_factor() > self._max_load_factor:
            raise AssertionError("The load factor is too high: Load factor is %f (size=%d, capacity=%d) but max allowed is %f" % (self._load_factor(), self.size(), len(self._keys), self._max_load_factor))

    # Functions that allow the hash table to be used like a Python dict

    def __getitem__(self, key):
        """This is called when the user writes 'x = table[key]'."""

        return self.get(key)
    
    def __setitem__(self, key, value):
        """This is called when the user writes 'table[key] = value'."""

        self.put(key, value)

    def __contains__(self, key):
        """This is called when the user writes 'key in table'."""

        return self.containsKey(key)

    def __str__(self):
        """This is called to show the hash table as a string."""

        # Use a dict comprehension to convert the hash table into a dict:
        # https://docs.python.org/3/tutorial/datastructures.html#dictionaries
        # Then show the dict as a string.

        return str({key: self[key] for key in self})
        # This code is the same as:
        # d = {}
        # for key in self:
        #   d[key] = self[key]
        # return str(d)
        # Note that 'for key in self' calls self.__iter__ to produce
        # the keys, and 'self[key]' calls self.__getitem__.

    def __repr__(self):
        """This is called to show the hash table as a string."""

        return repr({key: self[key] for key in self})

# Some code to check that the hash table is working
if __name__ == '__main__':
    table = HashTable()
    keys = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6]
    values = list(range(len(keys)))

    for i in range(len(keys)):
        table[keys[i]] = values[i]
        print(table)
        table.check()
    for i in range(len(keys)):
        print(table[keys[i]])
    print(table.statistics())
