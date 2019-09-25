# very basic GUI at start, text based
class MVP:
    def __init__(self):
        pass

    # prints out the board, along with the current players hand
    def printBoard(self, board, player):
        print("   ABCDEFGHIJKLMNO")
        b = board.getBoard()
        for i in range(len(b)):
            lineNo = str(i+1).ljust(3," ")
            line = b[i]
            print(str(lineNo) + str(line))
        print(" "*6,end="")
        print(player.hand)

    def makeMove(self, board, player):
        columnLabels = [chr(i) for i in range(65,65+15)]
        rowLabels = [i+1 for i in range(15)]

        rowColumn = input("choose a row/column to edit (A-O,1-15):\n")
        while True:
            if(rowColumn in columnLabels):
                orientation = 1
                rowColumn = columnLabels.index(columnLabels) + 1
                break

            elif(rowColumn in rowLabels):
                orientation = 0
                break
            rowColumn = input("invalid row/column entered, please try again:\n")

        self.getPlay(rowColumn, orientation, board, player)
        return()

    def getPlay(self, rC, orientation, board, player):
        print("The current line is:")
        print(board.getBoardLine(rC, orientation))
        play = input("input the new row to be played:\n")
        while True:
            if(board.checkValidPlay()):
                break
            play = input("invalid play, please try again:\n")
        pass

    def takeTurn(self):
        print("")
        menu = {"1":printBoard,"2":makeMove}
        print("1) print the board")
        print("2) make a play")
        while(True):
            choice = input("enter a choice:\n")
            if(choice in menu.keys()):
                choice = int(choice)
        return(menu[choice])

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
