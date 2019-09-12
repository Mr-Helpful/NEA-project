import Player as p
import Board as b

# very basic GUI at start, text based
class MVP:
    def __init__(self):
        pass

    # prints out the board, along with the current players hand
    def printBoard(self, board, player):
        print("   ABCDEFGHIJKLMNO")
        for i in range(len(board)):
            lineNo = str(i+1).ljust(3," ")
            line = board[i]
            print(str(lineNo) + str(line))
        print(" "*6,end="")
        print(player.hand)

    def makeMove(self, *args):
        pass

    def playGame(self, board, hand, players):
        print("")
        menu = {"1":self.printBoard,"2":self.makeMove}
        print("1) print the board")
        print("2) make a play")
        while(True):
            choice = input("enter a choice:\n")
            if(choice in menu.keys()):
                choice = int(choice)
        menu[choice](board, hand)

    def exit(self):
        print("\nexiting game")
        quit()

    def mainScreen(self, board, hand):
        menu = {"1":playGame,"2":exit}
        print("1) play a game")
        print("2) exit")
        while(True):
            choice = input("enter a choice:\n")
            if(choice in menu.keys()):
                choice = int(choice)
        return(menu[choice])


class fullGUI:
    def __init__(self):
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
