from tkinter import *
import numpy as np
import os

import Dictionary
import Player
import Board
import Play
import Bag

# this has to be last so that it overwrites the Image method of the tkinter class
# this is needed as everything is loaded from the tkinter module
from PIL import Image, ImageTk, ImageDraw

# very basic GUI at start, text based
class MVP:
    def __init__(self):
        pass

    # prints out the board, along with the current players hand
    def printBoard(self, game, player, board = False):
        if(not(board)):
            board = game.board.getBoard()

        display = "   ABCDEFGHIJKLMNO\n"

        board = ["".join(i) for i in board]
        for i in range(len(board)):
            lineNo = str(i+1).ljust(3," ")
            line = board[i]
            display += str(lineNo) + str(line) + "\n"

        display += " "*6

        hand = game.playerHands[player.name]
        display += "".join(hand) + "\n"
        return(display)

    def makeMove(self, game, player, nPlay):
        display = self.printBoard(game, player)
        rowColumn = input(display + "choose a row/column to edit (A-O or 1-15):\n")

        columnLabels = [chr(i) for i in range(65,65+15)]
        rowLabels = [str(i+1) for i in range(15)]
        while True:
            if(rowColumn in columnLabels):
                nPlay.orientation = 1
                nPlay.rC = columnLabels.index(rowColumn)
                break

            elif(rowColumn in rowLabels):
                nPlay.orientation = 0
                nPlay.rC = int(rowColumn) - 1
                break

            rowColumn = input(display + "invalid row/column entered, please try again:\n")
        self.getPlay(game, player, nPlay, display)

    def getPlay(self, game, player, nPlay, display):
        inputStr = display + "The current line is:\n"

        row = game.board.getBoardRotation(nPlay.orientation)[nPlay.rC]
        inputStr += "".join(row) + "\n"

        line = input(inputStr + "input the new row to be played:\n")
        while True:
            if(len(line) == 15):
                break

            line = input(inputStr + "invalid length, please re-enter:\n")

        nPlay.line = line

    def confirmPlay(self, game, player, nPlay):
        newBoard = game.board.getEditedBoard(nPlay)

        inputStr = "the new board will be:"
        inputStr += self.printBoard(game, player, newBoard)
        inputStr += "do you want to play the move (y/n):\n"

        play = input(inputStr)
        if(play in ["y","yes","ok","true"]):
            nPlay.confirmed = True

    def takeTurn(self, menu, startStr = ""):
        startStr += "1) make a play\n"
        startStr += "2) pass move\n"
        while(True):
            choice = input(startStr  + "enter a choice:\n")
            if(choice in menu.keys()):
                break
        return(menu[choice])

    def displayScores(self, game):
        display = []
        for player in game.players:
            name = str(player.name) + ":"
            score = game.playerScores[player.name]
            display.append([name, str(score)])

        display = ["\n".join(d) for d in display]
        display = "\n\n".join(display)
        print(display)

    def exit(self):
        print("\nexiting game")
        quit()

    def mainScreen(self, menu, board):
        startStr = "1) play a game\n"
        startStr += "2) exit\n"
        startStr += "enter a choice:\n"
        while(True):
            choice = input(startStr)
            if(choice in menu.keys()):
                return(menu[choice])

class Draggable:
    def __init__(self, object, snapCoords, snapRadius):
        self.dragObject = object

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
        widget = self.dragObject
        if(self.dragging):
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
            widget = self.dragObject
            x = widget.winfo_x() - widget._drag_start_x + event.x
            y = widget.winfo_y() - widget._drag_start_y + event.y
            self.currentCoords[0] = x
            self.currentCoords[1] = y
            widget.place(x = x, y = y)

    def holdup(self, event):
        cont = input("try me!")
        print("done")

class Full:
    def __init__(self, Board, Bag, Dictionary, Player):
        self.Window = Toplevel()

        print("building GUI")
        self.buildGUI(Board, Player)

        print("running GUI")
        self.runGUI()

    def buildGUI(self, Board, Player):
        size = 50
        self.Window.title("Tile testing")
        self.Window.config(background = "#ececec")
        self.Window.config(width = 1000, height = 850)
        snapCoords = self.createBoard(Board)
        self.addPicture(Player)
        self.addDetails(Player)
        self.buildTiles(snapCoords)

    def createBoard(self, Board):
        bg = Frame(self.Window, bg = "#000000", width = 788, height = 788)
        bg.place(x = 5, y = 5)

        colours = {"2l":"#b2c6e9",
                   "3l":"#446bc7",
                   "2w":"#ffb381",
                   "3w":"#ff0000",
                   "St":"#ffb381",
                   "  ":"#ffffff"}

        snapCoords = []
        size = 50
        offset = 10

        for x in range(15):
            for y in range(15):
                newCoords = [offset + (size + 2) * x, offset + (size + 2) * y]
                snapCoords.append(newCoords)

                weight = Board.weights[y][x]
                sqr = Frame(self.Window, width = size, height = size, bg = colours[weight])
                sqr.place(x = newCoords[0], y = newCoords[1])

        return(snapCoords)

    def addPicture(self, Player):
        imageName = Player.imageName
        photo = Image.open(imageName)
        img = ImageTk.PhotoImage(photo)

        panel = Label(self.Window, image = img)

        # a reference needs to be kept to the original object
        # this is required for the image to be displayed properly
        panel.image = img
        panel.place(x = 800, y = 5)

    def addDetails(self, Player):
        msg = Message(self.Window, text = Player.name)

    def buildTiles(self, snapCoords):
        snapRadius = 20
        startX = 10
        startY = 10
        for _ in range(15):
            self.addTile(snapCoords, snapRadius, x = startX, y = startY)

    def addTile(self, snapCoords, snapRadius, Letter = "_", Score = 10, x = 0, y = 0):
        frm = Frame(self.Window, relief = "raised", borderwidth = 3, width = 50, height = 50)
        frm.place(x = x, y = y)

        msg = Label(frm, text = Letter, font = ("Helvetica", 25), width = 1, height = 1)
        msg.place(x = 11, y = 3)
        self.linkEvents(msg, frm)

        msg = Label(frm, text = Score, font = ("Helvetica", 10), width = 1, height = 1)
        msg.place(x = 32, y = 27)
        self.linkEvents(msg, frm)

        Draggable(frm, snapCoords, snapRadius)

    def linkEvents(self, child, parent):
        bindtags = list(child.bindtags())
        bindtags.insert(1, parent)
        child.bindtags(tuple(bindtags))

    def runGUI(self):
        self.Window.mainloop()

'''
Testing
-------------------------------------------------------
'''

# sets up all objects which either have a dependancy on a file, or another object
def setupFiles(Bag):
    paths = getFilePaths()
    dictionary = Dictionary.Dictionary(paths["trieFile"], paths["wordFile"], Bag)
    board = Board.Board(Dictionary, Bag)
    return(dictionary, board)

def getFilePaths():
    dataPath = os.getcwd() + "/Data"
    walkNames = os.walk(dataPath)
    #print(list(walkNames)[0][2])
    #print(list(walkNames))
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

    imageName = "/Users/acolby/Documents/School_Work/_Computer_science/NEA-project/Scrabble/Data/Default.jpeg"

    player = Player.Player("Player1", 7, bag, imageName)

    weights = [["  ","  ","3w","3w","  ","  ","  ","  ","  ","  ","  ","3w","3w","  ","  "]
              ,["  ","3w","  ","  ","  ","2w","2w","2w","2w","2w","  ","  ","  ","3w","  "]
              ,["3w","  ","  ","2w","2w","  ","  ","  ","  ","  ","2w","2w","  ","  ","3w"]
              ,["3w","  ","2w","  ","  ","  ","3l","3l","3l","  ","  ","  ","2w","  ","3w"]
              ,["  ","  ","2w","  ","3l","3l","  ","  ","  ","3l","3l","  ","2w","  ","  "]
              ,["  ","2w","  ","  ","3l","  ","2l","2l","2l","  ","3l","  ","  ","2w","  "]
              ,["  ","2w","  ","3l","  ","2l","  ","  ","  ","2l","  ","3l","  ","2w","  "]
              ,["  ","2w","  ","3l","  ","2l","  ","St","  ","2l","  ","3l","  ","2w","  "]
              ,["  ","2w","  ","3l","  ","2l","  ","  ","  ","2l","  ","3l","  ","2w","  "]
              ,["  ","2w","  ","  ","3l","  ","2l","2l","2l","  ","3l","  ","  ","2w","  "]
              ,["  ","  ","2w","  ","3l","3l","  ","  ","  ","3l","3l","  ","2w","  ","  "]
              ,["3w","  ","2w","  ","  ","  ","3l","3l","3l","  ","  ","  ","2w","  ","3w"]
              ,["3w","  ","  ","2w","2w","  ","  ","  ","  ","  ","2w","2w","  ","  ","3w"]
              ,["  ","3w","  ","  ","  ","2w","2w","2w","2w","2w","  ","  ","  ","3w","  "]
              ,["  ","  ","3w","3w","  ","  ","  ","  ","  ","  ","  ","3w","3w","  ","  "]
              ]

    board.setWeights(weights)

    f = Full(board, bag, dictionary, player)
