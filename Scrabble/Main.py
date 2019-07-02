'''
improvements:
 - removed outdated currentData variable
 - added a method to the Trie, which allows it to find all solutions for a row
  - and also allows it to take into consideration the players hand
 - used os to find the path of the current directory
  - this allows it to find all of the neccessary resources for execution
'''

'''
This is code for a scrabble game.
It has a somewhat simplified AI opponent, which can only play one word per turn
Improvements still to make:
> make a Trie class, which inherits from a Tree class (needed as it is also used for minimaxing)
> create a "game" object for each new game
> Improve the AI of the opponent
 > Update the function for finding all plays in a row
  > create a seperate trie for the players current hand
  > And then intersect it with the main word trie
 > When minimaxing, use a tree format to save on recomputing the possible plays every time the opposing player makes a move
 > Make a function for finding all the playable rows
 > Make a function for checking the score of a play
 > Use a trie for lookup
 > add weights for moves
  > playing a common letter on a double/triple word score is weighted lower
  > getting rid of an uncommon letter is ranked higher
   > use the score of the letter to judge this
> Keep the board when the user chooses to save
> Create a function for playing an old file
 > Create a function for getting all used files
> Create a function for changing a username
 > Create a function for writing to user data
> Create a function for checking the board weights for a row
'''

'''
necessary imports
==================================================
'''

# used for picking a somewhat random tile from the scrabble "bag"
# ideally a truly random function would be used
# but if this module is used with the users plays as a seed, the overall effect will create enough entropy to ensure games are somewhat varied
import random

# used for checking for possible plays using the dictionary
# will likely be replaced by a Trie based design, which will need to be custom coded
import re

# used pretty much only for testing purposes and bootup
# it is used to find the times used to execute each part
# in testing this is used to determine which functions need to be optimised
# in bootup this is used to keep the user up to date and allow the user some time to read messages
import time


# used to store game states, players, etc
# mostly used as all of these are modelled as objects and therefore this is just easier to use
import pickle

# used to find the current directory of the script in order to find relevant resources such as game boards
import os

# used to store relevant data types in a single database
import sqlite3

'''
Constants to be defined
==================================================
'''

# defines the selection of scrabble tiles in the bag
# in the format "letter", score, quantity
# "." defines the blank tiles
# change if you want to add or remove tiles
# . is used to represent empty squares on the board for later
global Tiles
Tiles = [["a",1,9]
        ,["b",3,2]
        ,["c",3,2]
        ,["d",2,4]
        ,["e",1,12]
        ,["f",4,2]
        ,["g",2,3]
        ,["h",4,2]
        ,["i",1,9]
        ,["j",8,1]
        ,["k",5,1]
        ,["l",1,4]
        ,["m",3,2]
        ,["n",1,6]
        ,["o",1,8]
        ,["p",3,2]
        ,["q",10,1]
        ,["r",1,6]
        ,["s",1,4]
        ,["t",1,6]
        ,["u",1,4]
        ,["v",4,2]
        ,["w",4,2]
        ,["x",8,1]
        ,["y",4,2]
        ,["z",10,1]
        ,[".",0,2]
        ]

# defines the weights on the regular scrabble board
# change if you want to change the board
global BoardWeights
BoardWeights = [["3w","  ","  ","2l","  ","  ","  ","3w","  ","  ","  ","2l","  ","  ","3w"]
               ,["  ","2w","  ","  ","  ","3l","  ","  ","  ","3l","  ","  ","  ","2w","  "]
               ,["  ","  ","2w","  ","  ","  ","2l","  ","2l","  ","  ","  ","2w","  ","  "]
               ,["2l","  ","  ","2w","  ","  ","  ","2l","  ","  ","  ","2w","  ","  ","2l"]
               ,["  ","  ","  ","  ","2w","  ","  ","  ","  ","  ","2w","  ","  ","  ","  "]
               ,["  ","3l","  ","  ","  ","3l","  ","  ","  ","3l","  ","  ","  ","3l","  "]
               ,["  ","  ","2l","  ","  ","  ","2l","  ","2l","  ","  ","  ","2l","  ","  "]
               ,["3w","  ","  ","2l","  ","  ","  ","St","  ","  ","  ","2l","  ","  ","3w"]
               ,["  ","  ","2l","  ","  ","  ","2l","  ","2l","  ","  ","  ","2l","  ","  "]
               ,["  ","3l","  ","  ","  ","3l","  ","  ","  ","3l","  ","  ","  ","3l","  "]
               ,["  ","  ","  ","  ","2w","  ","  ","  ","  ","  ","2w","  ","  ","  ","  "]
               ,["2l","  ","  ","2w","  ","  ","  ","2l","  ","  ","  ","2w","  ","  ","2l"]
               ,["  ","  ","2w","  ","  ","  ","2l","  ","2l","  ","  ","  ","2w","  ","  "]
               ,["  ","2w","  ","  ","  ","3l","  ","  ","  ","3l","  ","  ","  ","2w","  "]
               ,["3w","  ","  ","2l","  ","  ","  ","3w","  ","  ","  ","2l","  ","  ","3w"]
               ]

# gives the directory tree under which to find the relevant files for operation
global filePrefix
filePrefix = os.getcwd() + "/"

# defines the file names which the program uses as memory
# will create a new file if there is no file available
global files
files = ["Scrabble_Board"]

# defines the file name for the user's data to be stored in
# includes username, current difficulty and previous scores
# ideally will be encoded
global userFile
userFile = "User_Data"

# defines the file being used as a ditionary
global dictFile
dictFile = "Scrabble_Dictionary(crucial)"

'''
Definitions of classes
==================================================
'''

# defines a single node object
# only has a value and children
# very simplistic as this will allow it to support quicker pickling later on
# mostly for minimax tree saving as this will be helpful in load times for games
# also reduces eventual file size of pickled objects

class Node:

    # defines the initialisation of a single node object
    # "" defines a root node
    def __init__(self,value):

        # defines the value of the node
        # will either be defined as an alphabetic character
        # or an empty string for the root Tree object
        # the end of the word node's value is defined as the EOW character
        # end of word node have node children connected to it
        self.value = value

        # defines the children of the Node
        # this will be used to move through the tree
        self.children = []

# defines a node used to construct a trees
# this will later be used to construct a trie

# Trie:
# A type of tree used to store words
# allows for easier lookup of words stored
# will be used later to dramatically decrease lookup times

class Tree():

    # defines the character to start a tree drawing on
    StartTree = "-"

    # defines the character to extend a tree drawing with
    ExtendTree = "|-"

    # defines the values needed to initialise a Tree object object
    # "" must be used to represent a root node of a tree
    def __init__(self):

        # defines the root Node of the tree as a Node with value ""
        self._rootNode = Node(".")

    # prints the entire trie connected to the node from which this method is called
    # mostly used for debug version
    # slightly laggy if used on a particularly large tree
    # due to the fact that it uses a lot of printing
    # setting CurNode and starter to 0 is used as a flag that these need to be updated
    # this is required as they can't be defaulted to a value relating to self as this hasn't been recognised yet
    def print_tree(self,CurNode = 0,starter = 0):

        # if CurNode is 0
        # updates CurNode to the correct value
        # used as self is defined in the parameters
        # and therefore cannot be used in default values
        if(CurNode == 0):
            CurNode = self._rootNode

        # updates starter to the correct value
        if(starter == 0):
            starter = self.StartTree

        # prints out the branch of the tree
        print(starter + CurNode.value)

        # calls itself on every node in the current node's children
        for node in CurNode.children:
            self.print_tree(node," |"+starter)

# defines a Trie
class Trie(Tree):

        # defines the character used to end a word
        EOW = ")"

        def find_child(self,node,char):
            # firstly defines charCheck as False
            # this will remain the value of charcheck if it fails to find the relevant node
            charCheck = False

            # iterates over the current node's children
            for Cnode in node.children:

                # checks if the value of the node fits the character being searched for
                if(Cnode.value == char):

                    # if so it updates the value of charCheck to the node conataining this character
                    # it is formatted as a list for ease of use later
                    charCheck = [Cnode]

            # if the value is blank it returns all of the children
            if(char == "."):
                return(node.children)

            return(charCheck)


        # stores an entire word in the trie
        # makes use of the self.add_child() method
        def store_word(self,word):

            # root is the node object currently being worked on
            root = self._rootNode

            # goes through each character in the word
            for char in word:

                # does a check for the correct character in the current nodes children

                charCheck = self.find_child(root,char)

                # checks whether a node doesn't exist for the correct letter
                if(not(charCheck)):

                    # if no node object exists, it creates a new node object to store the word
                    newNode = Node(char)
                    root.children.append(newNode)
                    root = newNode
                else:

                    # otherwise it will just navigate down that node
                    root = charCheck[0]
            endNode = Node(self.EOW)
            root.children.append(endNode)

        # allows for storage of a list of words at once
        def store_words(self,words):

            # iterates through words and calls store_word() on each one
            for word in words:
                self.store_word(word)

        def retrieve_words(self,node = 0,string = ""):
            if(node == 0):
                node = self._rootNode
            wordList = []
            if(node.value == self.EOW):
                return(wordList.append(string))
            newString = string + node.value
            for child in node.children:
                wordList.extend(self.retrieve_words(child,newString))
            return(wordList)

        # tries to find all the possible matches for a row
        # uses a given hand
        # solutions are defaulted to empty on first execution
        # and are then built up over the execution of the function
        # and returned at the end
        # string is defaulted to empty upon initialisation
        # seperate solutions are then built up as string is passed down through the trie
        def fit_Row(self, Row, Hand = ".e.ar..", StartString = ""):

            Node = self._rootNode

            PSolutions = [[Row,Hand,Node,StartString]]

            Solutions = []

            while(len(PSolutions) != 0):

                NextItem = PSolutions[0]

                Row = NextItem[0]

                print(NextItem)

                NextChar = Row[0]

                Hand = NextItem[1]

                Node = NextItem[2]

                String = NextItem[3]

                if(len(Row) != 0 and len(Hand) != 0):

                    if(Node.value == self.EOW):

                        print("Solution Found!")

                        Solutions.append(String)

                    if(NextChar == "."):

                        # if a word has not been started yet the tree is still on the root node
                        if(Node == self._rootNode):

                            # the word can be shifted across without playing anything
                            PSolutions.append([Row[1:],Hand,Node,String + Node.value])

                            # goes over every tile in the hand
                            # i.e. the tiles that can be played
                            for char in Hand:

                                # adds the next character from the hand
                                # as it doesn't matter what character this is
                                matches = self.find_child(Node,char)

                                # tests if there are matches on the tree
                                if(matches):

                                    # if there are goes over every item in matches
                                    # this may be multiple matches in the case of a blank tile
                                    for match in matches:
                                        PSolutions.append([Row[1:],Hand.replace(char,"",1),match,String + Node.value])

                    # if the space in the row isn't blank, it must be a letter tile
                    else:

                        # there will only ever be one result from a letter char
                        # it will either be an EOW character or
                        match = self.find_child(Node,NextChar)

                        # if find_child returns an answer that is not false it has found a valid branch
                        if(match):

                            # therefore it just navigates down the node without playing anything
                            # as if a tile would be played from the hand it would be like overlapping them on the board
                            PSolutions.append([Row[1:],Hand,match,String + Node.value])

                PSolutions.remove(NextItem)

                time.sleep(0.5)

            # returns solutions
            return(Solutions)

# defines a new player
# will be initialised for every new player and for an AI

class Player():
    def __init__(self,name):
        self._name = name
        self._scores = []
        self._admin = False

    def get_name(self):
        return(self._name)

    def addScore(self,newScore):
        self._scores.append(newScore)

    def hash(self,string):
        hash = 0
        weight = 1
        for char in string:
            hash += (weight * ord(char)) % 1000
            weight *= 7
        return(hash)

    def check_admin(self,password):
        print(self.hash(password))

    def getTotal(self):
        total = sum(self._scores)
        return(total)

class Board():
    def __init__(self):
        self._board =  ["...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "...............",
                        "..............."]

    def getRows(self):
        board = []
        for row in range(15):
            rowOut = []
            for column in range(15):
                rowOut.append(self._board[row][column])
            board.append(rowOut)
        return(rowOut)

    def getColumns(self):
        board = []
        for column in range(15):
            rowOut = []
            for row in range(15):
                rowOut.append(self._board[row][column])
            board.append(rowOut)
        return(rowOut)


'''
Definitions of functions
==================================================
'''

'''
GUI Definitions
--------------------------------------------------
'''

# chooses the difficulty for the AI
def choose_difficulty():
    print("choose a difficulty")
    print("1) easy")
    print("2) medium")
    print("3) hard")
    print("4) somewhat difficult")
    choice = int(input(""))
    return(21-5*choice)                         # returns the difficulty in a useful format

# prints out a GUI based on number choices
def GUI(options):                             # options is a dictionary of choices and related functions
    for i in range(len(options)):
        print(str(i+1)+") {}".format(list(options.keys())[i]))
    choice = int(input("Choose an number to use:\n"))
    return((options.values())[choice-1])        # returns the function chosen

# GUI used to choose a file to read / write to
def choose_file():                       # uses a list of available files
    print("Available files:")
    label = 1
    for file in files:
        fileStatus = "empty"
        r = open(file,"r")                                  # opens the file in a readable format
        if(not(r.readlines() is None)):                     # checks whether the file is not empty
              fileStatus = "in use"                           # updates the file status to match
        print("",end="")
        print("{}) {}({})".format(label,file,fileStatus))   # prints out the file option, along with its status
        label += 1
    print("{}) or exit".format(label))
    choice = input("Choose a file to use:\n")
    if(choice == label+1):
        return(False)
    else:
        return(files[label-1])

'''
file handling
--------------------------------------------------
'''

# overwrites the board from the file called fileName. Uses the newFile list.
def write_file(newFile,fileName):
    w = open(fileName,"w")                      # opens the file object
    for line in newFile:
        w.write(line+"\n")                      # writes each line and uses a newline character

# gets the dictionary from the dictionary file
def retrieve_dictionary(dictFile):
    print(dictFile)
    with open(dictFile,"rb") as r:            # opens the dictfile for reading
        dictionary = pickle.load(r)
    return(dictionary)

'''
file related methods
--------------------------------------------------
'''

# replaces a item at index "index" in a string
# I had to include this as I couldn't find a string operator for this
def replace_item(string,index,newItem):
    List = list(string)                         # converts the string to a list
    List[index] = newItem                       # replaces the item in the list
    string = "".join(List)                      # converts the list to a string
    return(string)

def write_char(board,row,column,char):
    board[row] = replace_item(board[row],column,char)
    pass

# flipboard is used to determine whether to make the play horizontally or vertically
# lineNo is used to determine the row or column to play across
def writeline(board,lineNo,string,flipBoard=False):
    for i in range(0,16):               # iterates across the specified row/column
        if(flipBoard):
            write_char(board,i,lineNo,string[i])
        else:
            write_char(board,lineNo,i,string[i])

# resets the board; used when a new game is required
def reset_board(fileName):
    resetList = ["*"*15 for _ in range(15)]     # generates an empty board
    write_file(resetList,fileName)              # writes the empty board to the file

# checks whether a given file is currently in use
def check_used(file):
    noStars = [line.count("*") for line in file] # creates a list of the number of stars in each row
    if(sum(noStars)<15*15):                      # checks whether any of the stars have been replaced
        return(True)                             # returns true of false depending on this
    else:
        return(False)

'''
commonly used methods
--------------------------------------------------
'''

# used to produce a valid regex statement for a given pattern of blanks and letters
def create_expression(lines):
    dotNos = count_dots(lines)            # finds the pattern of dots within the lines
    phrase = "^[a-z]{0,"+str(dotNos[0])+"}" # creates the start expression
    end = "[a-z]{0,"+str(dotNos[len(dotNos)-1])+"}$"
    Sum = dotNos[0]
    for i in range(1,len(dotNos)-1):
        phrase += lines[Sum] + "[a-z]{"+str(dotNos[i])+"}"
        Sum += 1 + dotNos[i]
    phrase += lines[Sum] + end
    return(phrase)

# returns all the columns in the board
def board_columns(board):
    columns = []
    for i in range(15):
        column = ""
        for line in board:
            column += line[i]
        columns.append(column)
    return(columns)

def AI_turn():
    pass

# somewhat flawed method, I assume it's the AI's turn when they load a new file
# could be said to be somewhat unfair, but the other way could be exploited
def play_game(selectedFile,difficulty):
    while True:
        AI_turn(difficulty)
        pass

def splitPattern(pattern):
    branchedPatterns = []
    for i in range(0,len(pattern)):
        try:
            if(pattern[i]!="." and pattern[i-1]=="."):
                branchedPatterns.append(pattern[0:i+2],pattern[i+2:],0,1)
        except:
            x = 0
        try:
            if(pattern[i]!="." and pattern[i+1]=="."):
                branchedPatterns.append(pattern[i+2:],pattern[0:i+2],1,0)
        except:
            x = 0
    print(branchedPatterns)
    pass

# finds all possible words for a pattern using the dictionary
def find_words(dictionary,pattern):
    noDots = pattern.count(".")
    # need to piece it together through a regex
    p = re.compile(pattern)
    # and use it to iterate through the dictionary, checking for matches
    matches = list(filter(p.match,dictionary))
    matches = [match for match in matches if(noDots-match.count(".")<8 and noDots-match.count(".")>1)]
    return(matches)

# checks the score of a single play on a row
# uses the score of the tiles and the board multipliers
def check_score(play,row,pattern):
    multiplier = 1
    score = 0
    TileScore = 0
    for i in range(15):
        for x in Tiles:
            if(str(x[0])==str(play[i])):
                TileScore = x[1]
                break
        if(BoardWeights[row][i][1]=="w" and TileScore > 0):
            multiplier *= int(BoardWeights[row][i][0])
        if(BoardWeights[row][i][1]=="l"):
            score += int(BoardWeights[row][i][0])*TileScore
        else:
            score += TileScore
    if(pattern.count(".")-play.count(".")):
        score += 50
    score *= multiplier
    return(score)

# finds the max possible play in a list of possible plays
def check_max_play(plays,row,pattern):
    plays = [[play,check_score(play,row,pattern)] for play in plays]
    print(plays)
    plays.sort(key=lambda x: int(x[1]),reverse=True)
    if(len(plays)==0):
        return([None,0])
    return(plays[0])

# picks a number of tiles from the bag
def pick_tiles(hand):
    noTiles = 7-len(hand)
    availableTiles = [tile[0] for tile in Tiles if(tile[2]>0)]
    tilesLeft = sum([tile[2] for tile in Tiles])
    if(noTiles<tilesLeft):
        tilesToPick = noTiles
    else:
        tilesToPick = tilesLeft
    for i in range(tilesToPick):
        pick = random.randint(0,len(availableTiles)-1)
        Tiles[pick][2] -= 1
        hand += Tiles[pick][0]
    return(hand)

'''
menu options
--------------------------------------------------
'''

# function used to start a new game
def start_game():                        # uses files and choose_file to select a file to play on
    selected_file = choose_file()
    reset_board(selectedFile)                   # resets the board of the selected save
    difficulty = choose_difficulty()
    play_game(selected_file,difficulty)

# function used to load a pre-used game
def load_game():
    pass

# changes the username of the player
def change_name():
    pass

# quits program by throwing an error
def quit():
    raise Exception("program exited")    # throws an error in order to exit the program

'''
Menu options for the GUI
Need to be defined after the functions as it uses them
==================================================
'''
menuOptions = {
                            "Start a new game" : start_game,
                            "Load an old game" : load_game,
                            "Change username" : change_name,
                            "Quit the program" : quit
              }

if(__name__ == "__main__"):
    print("parsed successfully")
