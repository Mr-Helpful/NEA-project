from tkinter import *
import numpy as np
import os

import Dictionary
import Player
import Board
import copy
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
    def __init__(self, Window, object, snapCoords, snapRadius):
        self.Window = Window
        self.dragObject = object

        # determines whether the object is being dragged
        self.dragging = False
        self.currentCoords = [0,0]
        self.snapCoords = snapCoords
        self.snapRadius = snapRadius
        self.make_draggable()

    def make_draggable(self):
        self.dragObject.bind("<Button-1>", self.toggle_drag)
        self.dragObject.bind("<Motion>", self.on_drag_motion)

    def remove_drag(self):
        self.dragObject.unbind("<Button-1>")
        self.dragObject.unbind("<Motion>")

    def blank_function(self):
        pass

    def toggle_drag(self, event):

        # toggle the dragging variable
        self.dragging = not(self.dragging)
        widget = self.dragObject
        if(self.dragging):
            self.dragObject.lift()
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
                self.currentCoords[0] = p[0]
                self.currentCoords[1] = p[1]

    def on_drag_motion(self, event):
        if(self.dragging):
            widget = self.dragObject
            x = widget.winfo_x() - widget._drag_start_x + event.x
            y = widget.winfo_y() - widget._drag_start_y + event.y
            self.currentCoords[0] = x
            self.currentCoords[1] = y
            widget.place(x = x, y = y)

class Tile:
    def __init__(self, Window, Bag, snapCoords, snapRadius, letter = "_", score = "0", x = 0, y = 0):
        self.Window = Window
        self.snapCoords = snapCoords
        self.snapRadius = snapRadius
        self.letter = letter
        self.score = Bag.scores[self.letter]
        self.buildTile(x, y)

    def buildTile(self, x, y):
        frm = Frame(self.Window, relief = "raised", borderwidth = 3, width = 50, height = 50)
        frm.place(x = x, y = y)

        msg = Label(frm, text = self.letter, font = ("Helvetica", 25), width = 1, height = 1)
        msg.place(x = 11, y = 3)
        self.linkEvents(msg, frm)

        msg = Label(frm, text = self.score, font = ("Helvetica", 10), width = 1, height = 1)
        msg.place(x = 32, y = 27)
        self.linkEvents(msg, frm)

        self.Drag = Draggable(self.Window, frm, self.snapCoords, self.snapRadius)

        self.widget = frm

    def fixPlace(self):
        self.widget.unbind("<Button-1>")
        self.widget.unbind("<Motion>")

    def linkEvents(self, child, parent):
        bindtags = list(child.bindtags())
        bindtags.insert(1, parent)
        child.bindtags(tuple(bindtags))

    def getCoords(self):
        return(self.Drag.currentCoords)

    def delete(self):
        self.widget.destroy()

class GameScreen:
    def __init__(self, board, Bag, Dictionary, Players, PlayerHands):
        self.Window = Tk()

        print("initialising variables")
        self.Board = board
        self.Bag = Bag
        self.Dictionary = Dictionary
        self.Players = Players
        self.PlayerHands = PlayerHands
        self.initVariables()

        print("building GUI")
        self.buildGUI()

        print("running GUI")
        self.runGUI()

    def initVariables(self):
        self.boardSnaps = []
        self.handTiles = []
        self.boardTiles = []
        self.currentPlayer = list(self.Players.keys())[0]

    def buildGUI(self):
        size = 50
        self.Window.title("Tile testing")
        self.Window.config(background = "#ececec")
        self.Window.config(width = 1100, height = 850)
        self.createBoard()
        self.addPicture()
        self.addDetails()
        self.buildTiles()
        self.addSwapHand()

    def createBoard(self):
        bg = Frame(self.Window, bg = "#000000", width = 788, height = 788)
        bg.place(x = 5, y = 5)
        bg.lower()

        colours = {"2l":"#b2c6e9",
                   "3l":"#446bc7",
                   "2w":"#ffb381",
                   "3w":"#ff0000",
                   "St":"#ffb381",
                   "  ":"#ffffff"}

        size = 50
        offset = 10

        for x in range(15):
            for y in range(15):
                newCoords = [offset + (size + 2) * x, offset + (size + 2) * y]
                self.boardSnaps.append(newCoords)

                weight = self.Board.weights[y][x]
                sqr = Frame(bg, width = size, height = size, bg = colours[weight])
                sqr.place(x = newCoords[0] - 5, y = newCoords[1] - 5)

        self.boardLayout = bg

    def addPicture(self):
        imageName = self.currentPlayer.imageName
        photo = Image.open(imageName)
        img = ImageTk.PhotoImage(photo)

        panel = Label(self.Window, image = img)

        # a reference needs to be kept to the original object
        # this is required for the image to be displayed properly
        panel.image = img
        panel.place(x = 800, y = 5)

    def addDetails(self):
        frm = Frame(self.Window, width = 225, height = 50)
        frm.place(x = 800, y = 250)

        msg = Label(frm, text = self.currentPlayer.name, font = ("Helvetica",25), bg = "#ececec")
        msg.pack(side=RIGHT)

    def buildTiles(self):
        snapRadius = 26
        startX = 800
        startY = 310
        tiles = self.PlayerHands[self.currentPlayer.name]
        for tile in tiles:
            allCoords = self.boardSnaps + [[startX, startY]]

            newTile = Tile(self.Window, self.Bag, allCoords, snapRadius, tile, x = startX, y = startY)
            self.handTiles.append(newTile)
            startX += 50

    def addSwapHand(self):
        msg = Message(self.Window, text = "Swap the Hands")
        msg.bind("<Button-1>", self.swapHand)
        msg.place(x = 800, y = 400)

    def findTilesOnBoard(self):
        for tile in self.handTiles:
            coords = tile.getCoords()
            if(coords in self.boardSnaps):
                tile.fixPlace()
                self.boardSnaps.remove(coords)
                self.handTiles.remove(tile)
                self.boardTiles.append(tile)
                hand = self.PlayerHands[self.currentPlayer.name]
                hand.remove(tile.letter)

    def swapHand(self, event):
        self.findTilesOnBoard()
        self.delHand()

        nextPlayer = self.Players[self.currentPlayer]
        self.currentPlayer = nextPlayer

        self.buildTiles()

    def delHand(self):
        for tile in self.handTiles:
            tile.delete()

    def runGUI(self):
        self.Window.mainloop()

class mainMenu:
    def __init__(self):
        self.Window = Tk()
        self.buildMenu()
        self.runMenu()

    def buildMenu(self):
        btn1 = Message(self.Window, text = "Play a game", width = 100)
        btn1["bg"] = "white"
        btn1.bind("<Button-1>", self.newGame)
        btn1.pack(side = LEFT)
        btn1.place(x = 50, y = 50)

        btn2 = Message(self.Window, text = "Read the rules", width = 100)
        btn2["bg"] = "white"
        btn2.bind("<Button-1>", self.readRules)
        btn2.pack(side = LEFT)
        btn2.place(x = 50, y = 100)

        btn3 = Message(self.Window, text = "Quit the app", width = 100)
        btn3["bg"] = "white"
        btn3.bind("<Button-1>", self.quit)
        btn3.pack(side = LEFT)
        btn3.place(x = 50, y = 150)

    def newGame(self, event):
        pass

    def readRules(self, event):
        # doesn't need to initiate a variable as the window will act on its own
        rulesBox("Rules")

    def linkEvents(self, child, parent):
        bindtags = list(child.bindtags())
        bindtags.insert(1, parent)
        child.bindtags(tuple(bindtags))

    def quit(self, event):
        self.Window.destroy()

    def runMenu(self):
        self.Window.mainloop()

class rulesBox:
    def __init__(self, name):
        self.root = Toplevel()
        self.root.title(name)
        self.buildScrollBox()
        self.addElements()

    def buildScrollBox(self):
        frame=Frame(self.root,width=300,height=300)
        frame.place(x=10, y=10)
        frame.config(relief = "ridge", borderwidth = 3)
        self.frm=Frame(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,300,1000))
        self.frm.bind_all("<MouseWheel>", self.wheel)

        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.frm.yview)
        self.linkEvents(self.frm, frame)

        self.frm.config(yscrollcommand=vbar.set)
        self.frm.pack(side=LEFT,expand=True,fill=BOTH)

    def addElements(self):
        self.addText()
        self.addGif()
        self.addPictures()

    def addText(self):
        txt = '''The game of Scrabble can be played by (not currently) 2-4 players'''
        txt1 = Message(self.frm, text)
        txt1.place(x=5, y=5)

    def addGif(self):
        pass

    def addPictures(self):
        pass

    def wheel(self, event):
        self.canvas.yview_scroll(-event.delta, "units")

    def linkEvents(self, child, parent):
        bindtags = list(child.bindtags())
        bindtags.insert(1, parent)
        child.bindtags(tuple(bindtags))

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

    players = []
    players.append(Player.Player("Player1", 7, bag, imageName))
    players.append(Player.Player("Player2", 7, bag, imageName))

    nPlayer = {}
    for i in range(len(players)):
        p1 = players[i-1]
        p2 = players[i]
        nPlayer[p1] = p2

    playerHands = {}
    for p in nPlayer.keys():
        playerHands[p.name] = bag.getTiles(7)

    print(playerHands)

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

    boardTwo = copy.copy(board)
    boardTwo.weights = weights

    player = Player.Player("Player1", 7, bag, imageName)

    #f = GameScreen(board, bag, dictionary, nPlayer, playerHands)
    m = mainMenu()
