import Dictionary
import Database
import Player
import Board
import Game
import Bag
import GUI
import AI

import os
import re

'''
Currently:
> refactoring implementation of makeMove into Player
> expressing passing all Game attributes through the object of Game

To do:
> Refactor implementation of makeMove into Player as much as possible.
 > Try to get it to the point where Game simply has to call the takeTurn method from Player
 > This will later be useful when coding the AI

> Seperate out the private and public variables and use getters and setters where appropriate
 > The need for this is likely going to be low as most of the variables are passed down in this implementation

> Properly comment your code!

> Create a scoring system for the plays made
 > Implement this in the board class
 > If you want to be secure about this, the Player and Scrabble classes should be the only ones directly accessed by the user
  > I.e. through the GUI
'''

class Scrabble:
    def __init__(self):
        self.bag = Bag.Bag()
        self.GUI = GUI.MVP()
        self.setupFiles()
        self.run()

    # sets up all objects which either have a dependancy on a file, or another object
    def setupFiles(self):
        paths = self.getFilePaths()
        self.dictionary = Dictionary.Dictionary(paths["trieFile"], paths["wordFile"], self.bag)
        self.database = Database.Database(paths["database"])
        self.board = Board.Board(self.dictionary, self.bag)

    def getFilePaths(self):
        dataPath = os.getcwd() + "/Data"
        walkNames = os.walk(dataPath)
        fileNames = list(walkNames)[0][2]
        regexes = {"wordFile":".*List","trieFile":".*Trie","database":".*\.db"}
        filePaths = {}
        for key in regexes.keys():
            regex = regexes[key]
            Paths = self.findFiles(dataPath, fileNames, regex)
            filePaths[key] = Paths
        return(filePaths)

    def findFiles(self, dataPath, fileNames, regex):
        pathNames = []
        r = re.compile(regex)
        for name in fileNames:
            if(r.match(name)):
                fullPath = self.extendPath(dataPath, name)
                pathNames.append(fullPath)
        return(pathNames)

    def extendPath(self, dataPath, fileName):
        return(dataPath + "/" + fileName)

    def exit(self, *args):
        self.GUI.exit()

    def playGame(self):
        players = self.getDefaultPlayers()
        self.game = Game.Game(players, self.board, self.bag, self.GUI)

    def run(self):
        menu = {"1":self.playGame,"2":self.exit}
        choice = self.GUI.mainScreen(menu, self.board)
        choice()

    def getDefaultPlayers(self):
        player1 = Player.Player("Player 1", 7, self.bag)
        player2 = Player.Player("Player 2", 7, self.bag)
        return([player1, player2])

if(__name__ == "__main__"):
    s = Scrabble()
