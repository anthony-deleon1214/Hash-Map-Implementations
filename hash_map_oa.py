# Name: Anthony Deleon-Birth
# OSU Email: deleonba@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: June 3, 2022
# Description: Implementation of an Open Addressing HashMap using Quadratic Probing
#              HashMap is built on top of an underlying DynamicArray for storage


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Creates a tuple containing the key-value pair
        Resizes table if necessary
        Hashes the provided key to determine where to place the item
        If index is empty, places tuple at that index
        Otherwise, uses quadratic probing until finding
        an empty index, tombstone, or the value matching the key
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)
        new_entry = HashEntry(key, value)
        hashed_index = self._hash_function(key) % self._capacity
        item = self._buckets[hashed_index]
        if not item:
            self._buckets[hashed_index] = new_entry
            self._size += 1
            return
        if item.key == key and not item.is_tombstone:                                   # If key is present and not a tombstone
            self._buckets[hashed_index] = new_entry                                     # Overwrite, but do not increase
            return
        elif item.key == key and item.is_tombstone:                                     # If key is present, but it is a tombstone
            self._buckets[hashed_index] = new_entry                                     # Overwrite and increase size
            self._size += 1
            return
        if self.contains_key(key):                                                      # Check if key is present and not a tombstone
            new_index = self._quadratic_probing_get(hashed_index, key)                  # Returns index that is either empty or has matching key
            self._buckets[new_index] = new_entry                                        # Overwrite item, but do not increase size
            return
        new_index = self._quadratic_probing_put(hashed_index, key)
        item = self._buckets[new_index]
        if item and item.key == key and item.is_tombstone:
            self._buckets[new_index] = new_entry
            return
        self._buckets[new_index] = new_entry
        self._size += 1
        return

    def table_load(self) -> float:
        """
        Calculates the load factor for the HashMap
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Subtracts size from capacity to determine number of empty buckets in HashMap
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Creates a new DynamicArray
        Iterates through existing array
        Rehashes all values found
        Inserts each entry into new array
        Updates self._buckets reference to new array
        Updates capacity to new capacity
        """
        if new_capacity < 1 or new_capacity < self._size:
            return
        self._capacity = new_capacity                                   # Update capacity to new_capacity
        new_array = DynamicArray()                                      # Create a new array for storage
        old_array = self._buckets                                       # Save reference to initial underlying
        self._buckets = new_array                                       # Change self._buckets reference to the new array
        self._size = 0                                                  # Update size to 0
        for _ in range(new_capacity):                                   # Mimic the initialization of the underlying
            new_array.append(None)
        for i in range(0, old_array.length()):
            item = old_array[i]                                         # Go through old array and check each index
            if item and not item.is_tombstone:                          # If index is not empty and not tombstone,
                self.put(item.key, item.value)                          # call put method, which will resize if necessary
        return

    def get(self, key: str) -> object:
        """
        Hashes the provided key using self._hash_function
        Checks the index obtained from the output of the hash function
        If the index does not contain the input key,
        Quadratic Probing is used to check indices until finding and index
        Containing the matching key or None
        Returns None if item not found
        Returns value if item is found
        """
        hashed_index = self._hash_function(key) % self._capacity            # Hash the provided key
        item = self._buckets[hashed_index]
        if item and item.key == key and not item.is_tombstone:              # If key at hashed index matches input key, return item
            return item.value
        hashed_index = self._quadratic_probing_get(hashed_index, key)       # Else, update hashed_index using quadratic probing helper function
        item = self._buckets[hashed_index]
        if item and not item.is_tombstone:
            return item.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if underlying DynamicArray is empty
        If not empty, checks if the specified key is in the array
        Returns True if key is found and is not a tombstone
        Returns False otherwise
        """
        if self._buckets.length() == 0:
            return False
        hashed_index = self._hash_function(key) % self._capacity            # Hash the provided key
        item = self._buckets[hashed_index]
        if item is None:                                                    # Return False if finding an empty index
            return False
        if item.key == key:                                                 # Check if key matches
            if item.is_tombstone:
                return False                                                # Return False if tombstone, True otherwise
            return True
        hashed_index = self._quadratic_probing_get(hashed_index, key)       # Else, update hashed_index using quadratic probing helper function
        item = self._buckets[hashed_index]
        if item and not item.is_tombstone:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Hashes input key
        Iterates through underlying DynamicArray using quadratic probing
        Continues iterating until finding empty index or input key
        Sets index to "_TS_" if value at index is the input key
        If empty is found, exits
        """
        hashed_index = self._hash_function(key) % self._capacity
        item = self._buckets[hashed_index]
        if item and item.key == key and not item.is_tombstone:
            item.is_tombstone = True
            self._size -= 1
            return
        elif item and item.key == key:
            return
        elif not item:
            return
        hashed_index = self._quadratic_probing_get(hashed_index, key)
        item = self._buckets[hashed_index]
        if item and item.key == key and not item.is_tombstone:
            item.is_tombstone = True
            self._size -= 1
        else:
            return

    def clear(self) -> None:
        """
        Changes self._buckets reference to a new DynamicArray instance
        Appends None to new array to maintain capacity
        """
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Iterates through underlying DynamicArray
        Appends any keys to a new DynamicArray
        Stops iterating after new array length reaches HashMap size
        Returns populated DynamicArray
        """
        keys_array = DynamicArray()
        keys_counter = 0
        for i in range(0, self._buckets.length()):
            if keys_counter >= self._size:
                break
            item = self._buckets[i]
            if item is not None and not item.is_tombstone:
                keys_array.append(item.key)
                keys_counter += 1
        return keys_array

    # Debug and potentially create a second version that only returns a matching key or None
    # Potentially throwing off some of the comparisons in the tests

    def _quadratic_probing_put(self, start_index: int, key: str) -> int:
        """
        Used for put method
        Iterates through underlying DynamicArray
        Increments counter if index is not empty or tombstone
        Wraps around to start of array if incremented beyond capacity
        Returns first index that
        """
        i = 1                                                               # Initialize the counter
        new_index = start_index + i**2                                      # Calculate new_index initially
        if new_index >= self._capacity:                                     # Subtract capacity from index if index >= capacity
            new_index = new_index - self._capacity                          # Used in edge case where start_index is last index in map
        item = self._buckets[new_index]                                     # Store reference to item at new_index
        while item and not item.is_tombstone:                               # Loop while item is not None and not tombstone
            if item.key == key:                                             # If item is the matching key/value pair, return new_index
                return new_index
            i += 1                                                          # Else, increment counter
            new_index = start_index + i**2                                  # Recalculate new_index
            while new_index >= self._capacity:                              # If new_index is larger than self._capacity
                new_index = new_index - self._capacity                      # Subtract the capacity from new_index and repeat until less than capacity
            item = self._buckets[new_index]                                 # Update value stored at item
        return new_index                                                    # Return new_index if item is None

    def _quadratic_probing_get(self, start_index: int, key: str) -> int:
        """
        Used for get and remove methods
        Iterates through underlying DynamicArray
        Increments counter if occupied index is found
        Returns if matching key or None is found
        """
        i = 1
        new_index = start_index + i**2
        if new_index >= self._capacity:                                     # Subtract capacity from index if index >= capacity
            new_index = new_index - self._capacity                          # Used in edge case where start_index is last index in map
        item = self._buckets[new_index]                                     # Store reference to item at new_index
        while item:                                                         # Loop while not finding empty index
            if item.key == key:                                             # If key is found, return index
                return new_index
            i += 1                                                          # Else, increment counter and continue probing
            new_index = start_index + i**2
            while new_index >= self._capacity:                              # If new_index is larger than self._capacity
                new_index = new_index - self._capacity                      # Subtract the capacity from new_index and repeat until less than capacity
            item = self._buckets[new_index]                                 # Update value stored at item
        return new_index                                                    # Return if empty is found


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
