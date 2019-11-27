import copy

import Dictionary
import Play
import Bag

class Board:
    size = 15
    def __init__(self, dictionary, bag):
        # tests for a specialised board being used
        self.dictionary = dictionary
        self.bag = bag
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
        # note here: in the official scrabble ruleset, the starting square is defined as a double word scorer.

        self.board = [["."]*self.size for _ in range(self.size)]
        middle = self.size // 2
        self.board[middle][middle] = "+"

    def setBoard(self, board):
        self.board = board

    def getFlippedBoard(self, board):
        flippedBoard = [[] for _ in range(len(board))]
        for y in board:
            for x in range(len(y)):
                flippedBoard[x].append(y[x])

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
        # makes a shallow copy of the board to be passed into the function
        newBoard = board[:]
        extension = [["."]*(len(newBoard)+2)]
        newBoard = [["."]+i+["."] for i in newBoard]
        rList = []
        rList.extend(extension)
        rList.extend(newBoard)
        rList.extend(extension)
        return(rList)

    def checkValidPlay(self, nPlay):
        board = self.getEditedBoard(nPlay)
        return(self.checkValidBoard(board))

    def checkValidBoard(self, board):
        validWords = self.checkValidWords(board)
        validPositions = self.checkValidPostitions(board)

        print("words:" + str(validWords))
        print("positions:" + str(validPositions))

        if(validWords and validPositions):
            return(True)
        return(False)

    def checkValidWords(self, board):
        words = self.getAllWords(board)
        valid = True
        for word in words:
            if(not(self.dictionary.checkForWord(word))):
                valid = False
        return(valid)

    # algorithm:
    # > starts from the top left hand corner of the board
    # > if a play has both an empty space before it and a filled space after then
    # it is considered to be the start of a word
    # > when it finds the start of a word it adds the whole word to the dictionary
    # and then moves along one row
    def getAllWords(self, board):
        words = []
        board = self.expandBoard(board)
        hWords = self.getWords(board)
        words.extend(hWords)

        board = self.getFlippedBoard(board)
        vWords = self.getWords(board)
        words.extend(vWords)
        words = [i for i in words if(i != [] and i != "")]
        words = ["".join(i) for i in words]
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

    def checkValidPostitions(self, board):
        changedBoard = self.eliminatePositions(board)
        for line in changedBoard:
            for tile in line:
                if(tile != "."):
                    return(False)
        return(True)

    def eliminatePositions(self, board):
        board = self.expandBoard(board)
        stack = [[8,8]]
        while True:
            coords = stack.pop(0)
            r = coords[0]
            c = coords[1]
            board[r][c] = "."
            stack.extend(self.checkPosition(board, r, c))
            if(len(stack) == 0):
                break
        return(board)

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
    def getChanges(self, nPlay):
        line = self.getBoardRotation(nPlay.orientation)[nPlay.rC]
        for i in range(len(line)):
            if(line[i] == nPlay.line[i]):
                nPlay.changes.append(".")

            # without this line, people could overwrite other's plays by playing blanks where there were tiles
            elif(nPlay.line[i] == "."):

                # this returns 15 underscores in a row
                # this is done as the underscore tile doesn't exist in the player's hand
                # and there are only two blank tiles in the bag
                # this means that any play which uses this format will be failed immediately
                nPlay.changes = ["_"*15]
                return()

            else:
                nPlay.changes.append(nPlay.line[i])

    def getBoardRotation(self, orientation, board = False):
        if(not(board)):
            board = self.board[:]

        if(orientation == 1):
            board = self.getFlippedBoard(board)

        return(board)

    def getEditedBoard(self, nPlay):
        board = self.getBoardRotation(nPlay.orientation)

        board[nPlay.rC] = list(nPlay.line)

        board = self.getBoardRotation(nPlay.orientation, board)
        return(board)

    def updateBoard(self, nPlay):
        board = self.getEditedBoard(nPlay)
        self.setBoard(board)

    def getAllChangedLines(self, nPlay):
        cLines = [nPlay]

        for i, char in enumerate(nPlay.changes):
            pPlay = self.getPerpendicularPlay(nPlay, i, char)
            if(pPlay):
                cLines.append(pPlay)

        return(cLines)

    def getPerpendicularPlay(self, nPlay, i, char):
        pPlay = copy.copy(nPlay)
        pPlay.orientation = not(pPlay.orientation)
        line = self.getBoardRotation(pPlay.orientation)[i]

        character = pPlay.changes[i]

        if(line[pPlay.rC] == char):
            return(False)

        longLine = ["."] + line + ["."]
        if(longLine[pPlay.rC] == "." and longLine[pPlay.rC + 2] == "."):
            return(False)

        pPlay.changes = ["."]*15
        pPlay.changes[pPlay.rC] = char
        pPlay.rC = i
        return(pPlay)

    def getScore(self, game, nPlay):
        allPlays = self.getAllChangedLines(nPlay)
        total = 0

        for play in allPlays:
            total += self.scoreRow(game, play)

        return(total)

    # orientation refers to whether the play is made across or down the board
    # rC refers to the number of the row/column of the board the play was made in
    def scoreRow(self, game, nPlay):
        weights = self.getBoardRotation(nPlay.orientation, self.weights)[nPlay.rC]

        tileScores = game.bag.scores

        total = 0
        mul = 1
        for tile, weight in zip(nPlay.changes, weights):
            score = tileScores[tile]
            if(tile == "."):
                pass
            elif(weight[1] == "l"):
                score *= int(weight[0])
            elif(weight[1] == "w"):
                mul *= int(weight[0])

            total += score

        return(total * mul)

if(__name__ == "__main__"):
    bag = Bag.Bag()
    wordFile = "WordList"
    trieFile = "WordTrie"
    dictionary = Dictionary.Dictionary(trieFile, wordFile, bag)
    b = Board(dictionary, bag)
    board = [list("......all......")
            ,list("......l........")
            ,list("......parry....")
            ,list("......h...e....")
            ,list("......a...s....")
            ,list("......b........")
            ,list("......e........")
            ,list("spaghetti......")
            ,list("...............")
            ,list("...............")
            ,list("...............")
            ,list("...............")
            ,list("...............")
            ,list("...............")
            ,list("...............")
            ]

    print(b.checkValidBoard(board))
