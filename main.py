
class HashTable:

    def __init__(self, initial_size=32):
        self.capacity = initial_size
        self.data = [""] * self.capacity
        self.size = 0

    # initial_hash_function
    # input : key - String
    # output : suma % self.capacity - int
    # effect : it returns the hash value of the string 'key'
    def initial_hash_function(self, key):
        suma = 0
        for charx in key:
            suma += ord(charx)
        return suma % self.capacity

    # add
    # input : key - String
    # output : None
    # effect : it adds the string 'key' in the hashtable
    def add(self, key):
        if self.size / self.capacity > 0.7:
            self.capacity = self.capacity * 2
            self.size = 0
            data = self.data
            self.data = [""] * self.capacity
            for oldKey in data:
                self.add(oldKey)
        index = self.initial_hash_function(key)
        while index < self.capacity and self.data[index] != "":
            index += 1
        if index == self.capacity:
            index = 0
        while index < self.capacity and self.data[index] != "":
            index += 1
        self.data[index] = key
        self.size += 1

    # lookup
    # input : key - String
    # output : index - int
    # effect : returns the index of the string 'key' from the hashtable
    def lookup(self, key):
        index = self.initial_hash_function(key)
        while index < self.capacity and self.data[index] != key:
            index += 1
        if index == self.capacity:
            index = 0
        while index < self.capacity and self.data[index] != key:
            index += 1
        if self.data[index] == key:
            return index
        return -1

    def __str__(self):
        result = "["
        for i in self.data:
            result += " " + i + ", "
        result += "]"
        return result


b = HashTable()
b.add("a")
b.add("b")
b.add("cb")
b.add("cc")
b.add("bc")
print(b.lookup("a"))
print(b.lookup("cb"))
print(b.lookup("bc"))
print(b.lookup("b"))
print(b)
