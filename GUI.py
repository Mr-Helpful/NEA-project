from tkinter import *
import Board
import Dictionary
import Bag
import os

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

class Draggable:
    def __init__(self, object, snapCoords, snapRadius):

        # determines whether the object is being dragged
        self.dragging = False
        self.currentCoords = [0,0]
        self.snapCoords = snapCoords
        self.snapRadius = snapRadius
        self.make_draggable(object)

    def make_draggable(self, widget):
        widget.bind("<Button-1>", self.toggle_drag)
        widget.bind("<Motion>", self.on_drag_motion)
        widget.bind("<Button-2>", self.holdup)

    def toggle_drag(self, event):

        # toggle the dragging variable
        self.dragging = not(self.dragging)
        widget = event.widget
        if(self.dragging):
            print("drag started from widget: {}".format(widget))
            widget._drag_start_x = event.x
            widget._drag_start_y = event.y

        else:
            x = widget.winfo_x()
            y = widget.winfo_y()
            distances = {(p[0]-x)**2 + (p[1]-y)**2: p for p in self.snapCoords}
            minD = min(distances.keys())

            if(minD < self.snapRadius ** 2):
                p = distances[minD]
                widget.place(x = p[0], y = p[1])

    def on_drag_motion(self, event):
        if(self.dragging):
            widget = event.widget
            x = widget.winfo_x() - widget._drag_start_x + event.x
            y = widget.winfo_y() - widget._drag_start_y + event.y
            self.currentCoords[0] = x
            self.currentCoords[1] = y
            widget.place(x = x, y = y)

    def holdup(self, event):
        cont = input("try me!")
        print("done")

class Full:
    def __init__(self, Board, Bag, Dictionary):
        self.Window = Tk()
        self.buildGUI()
        self.runGUI()

    def buildGUI(self):
        self.Window.title("Tile testing")
        self.Window.config(background = "#fafafa")
        self.buildTiles()

    def buildTiles(self):
        snapCoords = [[10,10],[75,10]]
        snapRadius = 20
        for _ in range(2):
            self.addTiles(snapCoords, snapRadius)

    def addTiles(self, snapCoords, snapRadius, Letter = "_", Score = 0, x = 0, y = 0):
        frm = Frame(self.Window, relief = "raised", borderwidth = 5, width = 60, height = 60)
        frm.place(x = x, y = y)

        msg = Message(frm, text = Letter, font = ("Helvetica", 30))
        msg.place(x = 0, y = 0)
        self.linkEvents(msg, frm)

        Draggable(frm, snapCoords, snapRadius)

    def linkEvents(self, child, parent):
        bindtags = list(child.bindtags())
        bindtags.insert(1, parent)
        child.bindtags(tuple(bindtags))

    def runGUI(self):
        self.Window.mainloop()



# sets up all objects which either have a dependancy on a file, or another object
def setupFiles(Bag):
    paths = getFilePaths()
    dictionary = Dictionary.Dictionary(paths["trieFile"], paths["wordFile"], Bag)
    board = Board.Board(Dictionary, Bag)
    return(dictionary, board)

def getFilePaths():
    dataPath = os.getcwd() + "/Data"
    walkNames = os.walk(dataPath)
    fileNames = list(walkNames)[0][2]
    regexes = {"wordFile":".*List","trieFile":".*Trie"}
    filePaths = {}
    for key in regexes.keys():
        regex = regexes[key]
        Paths = findFiles(dataPath, fileNames, regex)
        filePaths[key] = Paths
    return(filePaths)

def findFiles(dataPath, fileNames, regex):
    pathNames = []
    r = re.compile(regex)
    for name in fileNames:
        if(r.match(name)):
            fullPath = extendPath(dataPath, name)
            pathNames.append(fullPath)
    return(pathNames)

def extendPath(dataPath, fileName):
    return(dataPath + "/" + fileName)

if(__name__ == "__main__"):

    bag = Bag.Bag()
    dictionary, board = setupFiles(bag)
    # these would usually be passed in, maybe with a customised board layout

    print("done")
    f = Full(board, bag, dictionary)
