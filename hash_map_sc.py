# Name: Anthony Deleon-Birth
# OSU Email: delonba@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: June 3, 2022
# Description: Implementation of a Chained HashMap using singly-linked lists for chaining
#              HashMap is built on a DynamicArray for storage


from os import link
from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        Checks load factor
        If load factor is greater than 8, resizes table
        Hashes key to find target index
        If target index is occupied, places created node at start of list
        """
        if self.table_load() >= 8:
            self.resize_table(self._capacity*2)
        hashed_index = self._hash_function(key) % self._capacity
        item = self._buckets[hashed_index]
        key_check = item.contains(key)
        if key_check is not None:
            key_check.value = value
            return
        else:
            item.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Subtracts size from capacity to calculate empty buckets remaining
        """
        empty_count = 0
        for i in range(0, self._capacity):
            item = self._buckets[i]
            if item.length() == 0:
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        Divides size by capacity to calculate load factor
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Changes reference of self._buckets to a new DynamicArray
        Sets self._size to 0
        """
        new_array = DynamicArray()
        for i in range(0, self._capacity):
            new_array.append(LinkedList())
        self._buckets = new_array
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Creates a new DynamicArray
        Iterates through the underlying DynamicArray
        If an index is not None, rehashes the key
        Recalculates the index for placement
        Creates a new LinkedList at that index if one is not there
        Inserts the key/value pair at the target index
        Changes reference to the new array
        Updates self._capacity
        """
        if new_capacity < 1:
            return
        new_array = DynamicArray()
        for _ in range(new_capacity):
            new_array.append(LinkedList())
        for i in range(0, self._buckets.length()):
            item = self._buckets[i]
            if item is not None:
                for node in item:
                    new_hash = self._hash_function(node.key) % new_capacity
                    new_list = new_array[new_hash]
                    new_list.insert(node.key, node.value)
        self._capacity = new_capacity
        self._buckets = new_array
        return

    def get(self, key: str) -> object:
        """
        Hashes the provided key
        Checks the LinkedList stored at that index
        Iterates through LinkedList until finding target key or end of list
        Returns target item or None
        """
        hashed_index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[hashed_index]
        node = linked_list.contains(key)
        if node is not None:
            return node.value
        return node

    def contains_key(self, key: str) -> bool:
        """
        Hashes the provided key
        Goes to the hashed index
        Navigates the LinkedList stored at the index
        Returns true is a node with the matching key is found
        False if list is fully traversed without finding node
        """
        hashed_index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[hashed_index]
        node = linked_list.contains(key)
        if node is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Hashes provided key
        Navigates to target index
        Calls remove method on LinkedList at index
        """
        hashed_index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[hashed_index]
        if linked_list.remove(key):
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Creates a new DynamicArray
        Goes to each index in self._buckets
        Iterates through the LinkedList at each index
        Appends each found key to the new DynamicArray
        Returns new DynamicArray
        """
        keys_array = DynamicArray()
        for i in range(0, self._buckets.length()):
            linked_list = self._buckets[i]
            for node in linked_list:
                if node is not None:
                    keys_array.append(node.key)
        return keys_array


def find_mode(da: DynamicArray) -> tuple(DynamicArray, int):
    """
    TODO: Write this implementation
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)
    output_arr = DynamicArray()
    mode = None
    mode_count = 0
    for i in range(0, da.length()):                         # Add each element of the array to a hashmap
        if map.contains_key(da[i]):
            current_count = (map.get(da[i])+1)              # Store the current value for the key
            map.put(da[i], current_count)                   # Add 1 to the value stored with that key
        else:
            map.put(da[i], 1)                               # Add the key to the hashmap with a value of 1
            current_count = 1                               # Save current_count
        if current_count > mode_count:
            mode = da[i]
            mode_count = current_count
            output_arr = DynamicArray()
            output_arr.append(mode)
        elif current_count == mode_count:
            mode = da[i]
            output_arr.append(mode)
    return (output_arr, mode_count)

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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
