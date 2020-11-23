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
        self._Q = lines[0].split("\n")[0].split(" ")
        self._E = lines[1].split("\n")[0].split(" ")
        self._q0 = lines[2].split("\n")[0]
        self._table = {}

        for line in lines[3:]:
            line = line.split("->")
            rhs = line[1].split("|")
            listOfLists = []
            for production in rhs:
                production = production.split(" ")
                listOfLists.append(production)
            self._table[line[0]] = listOfLists

    @staticmethod
    def printState(list):
        x = "{ "
        for el in list:
            x += el + ", "
        x += "}"
        return x


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
                print("Q = " + Grammar.printState(self._Q))
            elif option == 2:
                print("E = " + Grammar.printState(self._E))
            elif option == 3:
                print("P = " + self.printProductions())
            elif option ==4 :
                print("P = " + self.printProductionsForNonTerminal())
            elif option == 5:
                print("S = " + self._q0)



    def printProductionsForNonTerminal(self):
        nonTerminal = input("give a nonterminal\n")
        if nonTerminal in self._Q:
            return self.printNonTerminalProductions(nonTerminal)
        return ""


main = Grammar("myGrammar.in")
main.main()

