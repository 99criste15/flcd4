

class FA:
    def __init__(self, fileIn):
        f = open(fileIn, "r")
        lines = f.readlines()
        self._Q = lines[0].split("\n")[0].split(" ")
        self._E = lines[1].split("\n")[0].split(" ")
        self._q0 = lines[2].split("\n")[0]
        self._F = lines[3].split("\n")[0].split(" ")
        D0 = lines[4].split("\n")[0].split("|")
        self._P = []
        self._isDFA = True
        self._table = {}

        for rule in D0:

            x = rule.split(" ")
            self._P.append(x)
            if (x[0], x[1]) in self._table:
                self._isDFA = False
            self._table[(x[0], x[1])] = x[2]


    @staticmethod
    def printState(list):
        x = "{ "
        for el in list:
            x += el + ", "
        x += "}"
        return x

    @staticmethod
    def printRules(list):
        x = "{ "
        for l in list:
            x += "δ(" + l[0] + "," + l[1] + ") = " + l[2] + ", "
        x += " }"
        return x


    def isAccepted(self,seq):
        if not self._isDFA:
            return False
        else:
            curState = self._q0
            for i in seq:
                if (curState, i) in self._table:
                    curState = self._table[(curState, i)]
                else:
                    return False
            if not curState in self._F:
                return False
            return True
    def main(self):
        option = -1
        menu = """0.Exit
1.Display the set of states
2.Display the alphabet
3.display transitions
4.display final states
5.check if sequence is accepted"""
        while option != 0:
            print(menu)
            option = int(input())
            if option == 1:
                print("Q = " + FA.printState(self._Q))
            elif option == 2:
                print("E = " + FA.printState(self._E))
            elif option == 3:
                print("P = " + FA.printRules(self._P))
            elif option == 4:
                print("F = " + FA.printState(self._F))
            elif option == 5:
                seq = input("give a sequence to be checked \n")

                if not self._isDFA:
                    print("the FA is not DFA\n")

                    continue
                else:
                    if self.isAccepted(seq):
                        print("accepted")
                    else:
                        print("The seq is not accepted")

