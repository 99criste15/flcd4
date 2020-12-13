from copy import deepcopy


class Grammar:

    def printProductions(self):
        productions = []
        for pair in self._table:
            result = []
            rhs = self._table[pair]
            for prod in rhs:
                result.append("".join(prod))
            productions.append(pair + " -> " + "|".join(result))
        return "\n".join(productions)

    def printNonTerminalProductions(self, nonterminal):
        productions = []

        result = []
        rhs = self._table[nonterminal]
        for prod in rhs:
            result.append("".join(prod))
        productions.append(nonterminal + " -> " + "|".join(result))
        return "\n".join(productions)

    def __init__(self, fileIn):
        f = open(fileIn, "r")
        lines = f.readlines()
        self._N = lines[0].split("\n")[0].split(" ")
        self._E = lines[1].split("\n")[0].split(" ")
        if "@space@" in self._E:
            self._E.append(' ')
            self._E.remove("@space@")
        self._S = lines[2].split("\n")[0]
        self._table = {}
        self._ll1Table = [[[] for _ in range(len(self._E) + 1)] for _ in range(len(self._N) + 1)]
        self._first = {}
        self._follow = {}
        self._pathFirst = {}
        self._isLL1 = True
        for line in lines[3:]:
            line = line.split("\n")[0]
            line = line.replace("bar", "|")

            line = line.split("->")
            rhs = line[1].split("|")
            listOfLists = []
            for production in rhs:
                production = production.split(" ")
                for i in range(len(production)):
                    if production[i] == "@space@":
                        production[i] = " "
                listOfLists.append(production)
            self._table[line[0]] = listOfLists
        for nonterminal in reversed(self._N):
            self._follow[nonterminal] = []
            self._first[nonterminal] = self.first(nonterminal)
        self.follow()
        paths = list(self._pathFirst.keys())
        for path in paths:
            value = path[1]
            key = path[0]
            prod = self._pathFirst[path]
            if value == 'Îµ':
                del self._pathFirst[path]
                followsSymbols = self._follow[key]
                for symbol in followsSymbols:
                    if symbol != "$":
                        self._pathFirst[(key, symbol)] = prod
        for i in range(len(self._N)):
            nont = self._N[i]
            for j in range(len(self._E)):
                symbol = self._E[j]
                if (nont, symbol) in self._pathFirst:
                    self._ll1Table[i][j].append(self._pathFirst[(nont, symbol)])

    @staticmethod
    def printState(list):
        x = "{ "
        for el in list:
            x += el + ", "
        x += "}"
        return x

    def first(self, nonterminal):

        if nonterminal == "factor":
            print("ha")
        if nonterminal in self._first:
            return self._first[nonterminal]
        result = []
        prods = self._table[nonterminal]
        for prod in prods:

            if (prod[0] in self._E or prod[0] == 'Îµ') and prod[0] not in result:
                result.append(prod[0])
                if (nonterminal, prod[0]) in self._pathFirst:
                    self._isLL1 = False
                self._pathFirst[(nonterminal, prod[0])] = prod
            if prod[0] in self._N:

                if prod[0] in self._first:
                    x = self._first[prod[0]]
                else:
                    x = self.first(prod[0])
                    self._first[prod[0]] = x
                for ii in range(len(x)):
                    res = x[ii]
                    if (nonterminal, res) in self._pathFirst:
                        self._isLL1 = False
                    if res not in result:
                        result.append(res)
                        self._pathFirst[(nonterminal, res)] = prod
        return result

    def main(self):
        option = -1
        menu = """0.Exit
1.Display the set of non-terminals
2.Display the terminals
3.display productions
4.display productions for a given non-terminal
5.display initial state"""
        while option != 0:
            print(menu)
            option = int(input())
            if option == 1:
                print("N = " + Grammar.printState(self._N))
            elif option == 2:
                print("E = " + Grammar.printState(self._E))
            elif option == 3:
                print("P = " + self.printProductions())
            elif option == 4:
                print("P = " + self.printProductionsForNonTerminal())
            elif option == 5:
                print("S = " + self._S)

    def printProductionsForNonTerminal(self):
        nonTerminal = input("give a nonterminal\n")
        if nonTerminal in self._N:
            return self.printNonTerminalProductions(nonTerminal)
        return ""

    def checkIfIsLL1(self):

        return self._isLL1

    def parseSeq(self, seq):
        listStack = [self._S]
        outputTree = {}
        outputTree["S"] = Node("S", None, None)
        if self._isLL1:
            while len(seq) != 0:
                if len(listStack) == 0:
                    return {}
                if listStack[0] in self._N:

                    currentSymbol = listStack.pop(0)
                    if (currentSymbol, seq[0]) in self._pathFirst:
                        listStack2 = deepcopy(self._pathFirst[(currentSymbol, seq[0])])
                        listStack2.extend(listStack)
                        listStack = listStack2
                        path = self._pathFirst[(currentSymbol, seq[0])]
                        for i in range (len(path)):
                            if i < len(path)-1:
                                outputTree[path[i]] = Node(path[i], currentSymbol, path[i+1])
                            else:
                                outputTree[path[i]] = Node(path[i], currentSymbol, None)

                    else:
                        return {}
                elif listStack[0] == 'Îµ':
                    listStack.pop(0)
                elif listStack[0] == seq[0]:
                    listStack.pop(0)
                    seq = seq[1:]
                else:
                    return {}

            if len(listStack) != 0:
                return {}
            return outputTree
        return {}

    def follow(self):
        self._follow[self._S] = ["$"]
        refFollows = []
        for nont in self._table:
            for production in self._table[nont]:
                for i in range(len(production)):
                    if production[i] in self._N:
                        if i + 1 < len(production):
                            if production[i + 1] in self._E and production[i + 1] != 'Îµ':
                                if production[i + 1] not in self._follow[production[i]]:
                                    self._follow[production[i]].append(production[i + 1])
                            elif len(self._first[production[i + 1]]) > 1 or 'Îµ' not in self._first[production[i + 1]]:
                                filtered = list(filter(lambda x: x != 'Îµ' and x not in self._follow[production[i]],
                                                       self._first[production[i + 1]]))
                                self._follow[production[i]].extend(filtered)
                                if 'Îµ' in self._first[production[i + 1]]:
                                    if production[i + 1] not in self._follow[production[i]]:
                                        self._follow[production[i]].append(production[i + 1])
                                        refFollows.append(production[i])
                            else:
                                if nont != production[i]:
                                    if nont not in self._follow[production[i]]:
                                        self._follow[production[i]].append(nont)
                                    if production[i] not in refFollows:
                                        refFollows.append(production[i])
                        else:
                            if nont != production[i]:
                                if nont not in self._follow[production[i]]:
                                    self._follow[production[i]].append(nont)
                                if production[i] not in refFollows:
                                    refFollows.append(production[i])

        while len(refFollows) != 0:
            for follow in self._follow:
                ok = True
                toBeDeleted = []
                for item in self._follow[follow]:
                    if item in self._N:
                        if item not in refFollows:
                            toBeDeleted.append(item)
                            self._follow[follow].extend(self._follow[item])
                        else:
                            ok = False
                for item in toBeDeleted:
                    self._follow[follow].remove(item)
                if ok and follow in refFollows:
                    refFollows.remove(follow)


class Node:
    def __init__(self, id, parent, sibling):
        self._id = id
        self._parent = parent
        self._sibling = sibling

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def sibling(self):
        return self._sibling

    @sibling.setter
    def sibling(self, sibling):
        self._sibling = sibling


class ParserOutput:
    def __init__(self, table):
        self._table = table

    def printToScreen(self):
        for key in self._table:
            parent = self._table[key].parent if self._table[key].parent is not None else "-"
            sibling = self._table[key].sibling if self._table[key].sibling is not None else "-"
            print(key+"\t"+parent+"\t"+sibling)
