

# very basic GUI at start, text based
class GUI:
    def __init__(self):
        self.MVP()
        pass

    def MVP(self):
        # code for text based AI
        pass

    def printBoard(self, board, hand):
        print("   ABCDEFGHIJKLMNO")
        for i in range(len(board)):
            lineNo = str(i+1).ljust(3," ")
            line = board[i]
            print(str(lineNo) + str(line))
        print(" "*6,end="")
        print(hand)

    def playGame(self, board, hand):
        menu = {"1":printBoard,"2":makeMove}

    def exit(self, *args):
        print("\nexiting game")
        quit()

    def mainScreen(self, board, hand):
        menu = {"1":self.playGame,"2":self.exit}
        print("1) play a game")
        print("2) exit")
        while(True):
            choice = input("enter a choice:\n")
            if(choice in menu.keys()):
                choice = int(choice)
        menu[choice](board, hand)

    def full(self):
        # code for the final GUI
        pass


if(__name__ == "__main__"):
    board = ["......a........"
            ,"......l........"
            ,"......p........"
            ,"......h........"
            ,"......a........"
            ,"......b........"
            ,".spaghetti....."
            ,"......t........"
            ,"......t........"
            ,"......i........"
            ,"..............."
            ,"..............."
            ,"..............."
            ,"..............."
            ,"..............."
            ]
    hand = "ahgskfj"
    g = GUI()
    g.printBoard(board, hand)
    g.exit()
    print("the end is never the end")
