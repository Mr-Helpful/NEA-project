import copy
from Dictionary import *
import Bag

class Board:
    size = 15
    def __init__(self,boardName = None):
        # tests for a specialised board being used
        if(boardName == None):
            self.generateStandardBoard()

    def generateStandardBoard(self):
        self.weights = [["3w","  ","  ","2l","  ","  ","  ","3w","  ","  ","  ","2l","  ","  ","3w"]
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
        self.board = ["."*self.size for _ in range(self.size)]

    def setBoard(self, board):
        self.board = board

    def getBoard(self):
        return(self.board)

    def getFlippedBoard(self, board = False):
        if(not(board)):
            board = self.board
        flippedBoard = ["" for _ in range(len(board))]
        for y in board:
            for x in range(len(y)):
                flippedBoard[x] += y[x]
        return(flippedBoard)

    # expandBoard copies the board and expands it to leave a ring of blank spaces
    # around the edge.
    # this form of the board is useful when checking if the entire board is valid
    # as it prevents indexing errors from being thrown and instead returns a blank
    # tile.
    # the reason it copies the board is to allow it to be manipulated without
    # affecting the original board, which should only ever be modified by a player
    # making a valid move on it.
    def expandBoard(self, board):

        # makes a shallow copy of the board passed into the function
        newBoard = board[:]
        extension = ["."*(len(newBoard)+2)]
        newBoard = ["."+i+"." for i in newBoard]
        rList = []
        rList.extend(extension)
        rList.extend(newBoard)
        rList.extend(extension)
        return(rList)

    def checkValidBoard(self, dictionary):
        validWords = self.checkValidWords(dictionary)
        validPositions = self.checkValidPostitions()
        if(validWords):
            print("all words played are valid")
        if(validPositions):
            print("all positions played are valid")

        if(validWords and validPositions):
            return(True)
        return(False)

    def checkValidWords(self, dictionary):
        words = self.getAllWords()
        print(words)
        valid = True
        for word in words:
            if(not(dictionary.checkForWord(word))):
                valid = False
        return(valid)

    # algorithm:
    # > starts from the top left hand corner of the board
    # > if a play has both an empty space before it and a filled space after then
    # it is considered to be the start of a word
    # > when it finds the start of a word it adds the whole word to the dictionary
    # and then moves along one row
    def getAllWords(self):
        words = []
        board = self.expandBoard(self.board)
        print(board)
        print("_________________________")
        print("\n".join(board))
        hWords = self.getWords(board)
        words.extend(hWords)

        board = self.getFlippedBoard(board)
        vWords = self.getWords(board)
        words.extend(vWords)
        words = [i for i in words if(i != '')]
        return(words)

    def getWords(self, board):
        words = []
        for r in range(len(board)-2):
            for c in range(len(board[r])-2):
                word = self.checkPlaceForStart(board, r+1, c+1)
                words.append(word)
        return(words)

    def checkPlaceForStart(self, board, r, c):
        before = board[r][c-1]
        after = board[r][c+1]
        if(after != "." and before == "."):
            word = self.getWord(board[r], c)
            return(word)
        return('')

    # finds the end of a word where the start point is placed
    def getWord(self, row, startPoint):
        endPoint = startPoint
        while True:
            if(row[endPoint] == "."):
                break
            endPoint += 1

        return(row[startPoint:endPoint])

    def checkValidPostitions(self):
        board = self.expandBoard(self.board)
        stack = [[9,9]]
        while True:
            print(len(stack))
            coords = stack.pop(0)
            r = coords[0]
            c = coords[1]
            board[r] = self.deleteEntry(board[r], c)
            stack.extend(self.checkPosition(board, r, c))
            if(len(stack) == 0):
                break

    def deleteEntry(self, line, c):
        line = list(line)
        line[c] = "."
        line = str(line)
        return(line)

    def checkPosition(self, board, r, c):
        stack = []
        if(board[r][c+1] != "."):
            stack.append([r,c+1])
        if(board[r][c-1] != "."):
            stack.append([r,c-1])
        if(board[r+1][c] != "."):
            stack.append([r+1,c])
        if(board[r-1][c] != "."):
            stack.append([r-1,c])
        return(stack)

    # finds the letters which vary on the line before the play and after
    # this would likely not be necessary for the final GUI, as it would be easier to find the new letters played
    def getChanges(self, line, play):
        changedLetters = []
        for i in range(len(line)):
            if(line[i] == play[i]):
                changedLetters.append(".")
            else:
                changedLetters.append(play[i])

        return(changedLetters)

    def getBoardLine(self, orientation, rC):
        board = self.board
        if(orientation == 1):
            board = self.getFlippedBoard(board)

        line = board[rC]

        return(line)

    # orientation refers to whether the play is made across or down the board
    # rC refers to the number of the row/column of the board the play was made in
    def scorePlay(self, orientation, rC, play, tiles):
        line = self.getBoardLine(orientation, rC)

        # the weights on the board have rotational symmetry, so they don't need to be flipped
        weights = self.weights[rC]

        changes = self.getChangedLetters(line, play)

        numChanges = len(changes) - changes.count(".")
        pass

if(__name__ == "__main__"):
    b = Board()
    board = ["......a........"
            ,"......l........"
            ,"......p........"
            ,"......h........"
            ,"......a........"
            ,"......b........"
            ,"......e........"
            ,"spaghetti......"
            ,"..............."
            ,"..............."
            ,"..............."
            ,"..............."
            ,"..............."
            ,"..............."
            ,"..............."
            ]
    b.setBoard(board)
    fBoard = b.getFlippedBoard()
    print("\n".join(fBoard))

    bag = Bag.Bag()
    wordFile = "WordList"
    trieFile = "WordTrie"
    d = Dictionary(trieFile, wordFile, bag)
    print("checking for valid board:")
    print(b.checkValidBoard(d))
