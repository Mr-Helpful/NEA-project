# very basic GUI at start, text based
class MVP:
    def __init__(self):
        pass

    # prints out the board, along with the current players hand
    def printBoard(self, board, player):
        if(type(board) == list):
            b = board
        else:
            b = board.getBoard()
        print("   ABCDEFGHIJKLMNO")
        b = ["".join(i) for i in b]
        for i in range(len(b)):
            lineNo = str(i+1).ljust(3," ")
            line = b[i]
            print(str(lineNo) + str(line))
        print(" "*6,end="")
        print(player.hand)

    def makeMove(self, board, player, game):
        columnLabels = [chr(i) for i in range(65,65+15)]
        rowLabels = [str(i+1) for i in range(15)]

        rowColumn = input("choose a row/column to edit (A-O or 1-15):\n")
        while True:
            if(rowColumn in columnLabels):
                orientation = 1
                rowColumn = columnLabels.index(rowColumn)
                break

            elif(rowColumn in rowLabels):
                orientation = 0
                rowColumn = int(rowColumn) - 1
                break
            rowColumn = input("invalid row/column entered, please try again:\n")
        check, play, lineChanges = self.getPlay(rowColumn, orientation, board, player, game)
        return(check, rowColumn, orientation, play)

    def getPlay(self, rC, orientation, board, player, game):
        print("The current line is:")
        row = board.getBoardRotation(orientation)[rC]
        print("".join(row))
        play = input("input the new row to be played:\n")
        while True:
            check, lineChanges = game.checkMove(rC, orientation, play, player)

            if(not(check)):
                print("invalid play, please try again")
            return(check, play, lineChanges)

    def confirmPlay(self, rowColumn, orientation, play, board, player):
        print("the new board will be:")
        self.printBoard(board, player)
        play = input("do you want to play the move (y/n):\n")
        if(play in ["y","yes","ok","true"]):
            return(True)
        return(False)

    def takeTurn(self, menu):
        print("1) print the board")
        print("2) make a play")
        print("3) pass move")
        while(True):
            choice = input("enter a choice:\n")
            if(choice in menu.keys()):
                break
        return(menu[choice])

    def exit(self):
        print("\nexiting game")
        quit()

    def mainScreen(self, menu, board):
        print("1) play a game")
        print("2) exit")
        while(True):
            choice = input("enter a choice:\n")
            if(choice in menu.keys()):
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
    g = MVP()
    g.printBoard(board, hand)
    g.exit()
    print("the end is never the end")
