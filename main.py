import re


class HashTable:

    def __init__(self, initial_size=32):
        self._capacity = initial_size
        self._data = [""] * self._capacity
        self._size = 0

    # initial_hash_function
    # input : key - String
    # output : suma % self.capacity - int
    # effect : it returns the hash value of the string 'key'
    def initial_hash_function(self, key):
        suma = 0
        for charx in key:
            suma += ord(charx)
        return suma % self._capacity

    # add
    # input : key - String
    # output : None
    # effect : it adds the string 'key' in the hashtable
    def add(self, key):

        maybeIn = self.lookup(key)
        if maybeIn != -1:
            return maybeIn

        if self._size / self._capacity > 0.7:
            self._capacity = self._capacity * 2
            self._size = 0
            data = self._data
            self._data = [""] * self._capacity
            for oldKey in data:
                self.add(oldKey)
        index = self.initial_hash_function(key)
        while index < self._capacity and self._data[index] != "":
            index += 1
        if index == self._capacity:
            index = 0
        while index < self._capacity and self._data[index] != "":
            index += 1
        self._data[index] = key
        self._size += 1
        return index

    # lookup
    # input : key - String
    # output : index - int
    # effect : returns the index of the string 'key' from the hashtable
    def lookup(self, key):
        index = self.initial_hash_function(key)
        while index < self._capacity and self._data[index] != key:
            index += 1
        if index == self._capacity:
            index = 0
        while index < self._capacity and self._data[index] != key:
            index += 1
        if index == self._capacity:
            return -1
        return index

    def __str__(self):
        result = "["
        for i in self._data:
            result += " " + i + ", "
        result += "]"
        return result


tokens = []
beforeMinus=["==","=","+","-","*","/",">","<","<=",">=","%"]
f = open("error.in", "r", encoding="utf8")
d = open("token.in", "r", encoding="utf8")
for line in d.readlines():
    tokens.append(line.split("#")[0])

lines = f.readlines()
program = []
pif = []
errors = []
symbolTable = HashTable()
lastToken = ""
for k in range(len(lines)):
    line = lines[k]
    quotesNr = 0
    newLine = ""
    for i in range(len(line)):
        ch = line[i]
        if line[i] == ' ' and quotesNr % 2 != 0:
            ch = "#space#"
        if line[i] == '\n' and quotesNr % 2 != 0:
            ch = "#enter#"
        if line[i] == '\t' and quotesNr % 2 != 0:
            ch = "#tab#"
        if line[i] == '"':
            quotesNr += 1
            if (quotesNr % 2 == 1):
                if newLine.rfind('"') == -1:
                    for i in range(len(tokens)):
                        newLine = newLine.replace(tokens[i], ' #' + str(i) + '# ')
                else:
                    lastSubstring = newLine[newLine.rfind('"') + 1:]
                    for i in range(len(tokens)):
                        lastSubstring = lastSubstring.replace(tokens[i], ' #' + str(i) + '# ')
                    newLine = newLine[:newLine.rfind('"') + 1] + lastSubstring
        newLine += ch
    if newLine.rfind('"') == -1:
        for i in range(len(tokens)):
            newLine = newLine.replace(tokens[i], ' #' + str(i) + '# ')
    elif quotesNr % 2 == 0:
        lastSubstring = newLine[newLine.rfind('"') + 1:]
        for i in range(len(tokens)):
            lastSubstring = lastSubstring.replace(tokens[i], ' #' + str(i) + '# ')
        newLine = newLine[:newLine.rfind('"') + 1] + lastSubstring
    line = newLine
    for i in range(len(tokens)):
        line = line.replace('#' + str(i) + '#', tokens[i])
    x = re.split('\s', line)

    x = list(filter(None, x))
    for i in range(len(x)):
        token = x[i]
        if lastToken!="":
            token = lastToken+token
            lastToken = ""
        if (token == "-" and (x[i-1] in beforeMinus)):
            lastToken = token
            continue

        token = token.replace("#space#", " ")
        token = token.replace("#tab#", "\t")
        token = token.replace("#enter#", "\n")
        if token.lower() in tokens:
            pif.append((token, -1))
        elif re.findall('^[a-zA-Z_]\w*$|^".*"$|^[-]{0,1}[0-9]\d*$|^[-]{0,1}[0-9]\d*,\d*$|^0$|^\'.\'$', token):
            pif.append((token, symbolTable.add(token)))
        else:
            errors.append("Lexical error at line " + str(k) + " at token :" + token)

print(symbolTable)
print(pif)
print(errors)
