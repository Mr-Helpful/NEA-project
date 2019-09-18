import copy

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

    def getFlippedBoard(self):
        board = self.board
        flippedBoard = ["" for _ in range(self.size)]
        for y in board:
            for x in range(len(y)):
                flippedBoard[x] += y[x]
        return(flippedBoard)

# need to rework this algortihm, as it currently doesn't work
    def getAllWords(self):
        allWords = []
        for row in self.board:
            words = row.split(".")
            while("" in words):
                words.pop("")
            allWords.extend(words)

        for column in self.getFlippedBoard():
            words = column.split(".")
            while("" in words):
                words.pop("")
            allWords.extend(words)
        return(allWords)

# algorithm:
# > makes a copy of the board
# > start on the center row and records the word passing through the center
# > removes all parts of the word which don't have another word connected
# > records which words cross through it
    def getAllWords(self):
        words = []
        board = self.expandBoard(self.board)
        hWords = self.getWords(board)
        words.extend(hWords)

        board = self.getFlippedBoard(board)
        vWords = self.getWords(board)
        words.extend(vWords)
        return(words)

    def getWords(self, board):
        words = []
        for r in range(len(board)):
            for c in range(len(board[r])):
                word = self.checkPlaceForStart(board, r, c)
                words.append(word)
        return(words)

    def expandBoard(self, board):
        # expands the board to include a ring of blank spaces around the edge
        # this allows the search on the edge of the board without errors
        # also copies the original board so that any edits made whilst searching don't affect it
        board = copy.copy(board)
        extension = ["."*(len(b)+2)]
        board = ["."+i+"." for i in board]
        board = extension.extend(board).extend(extension)
        return(board)

    def checkPlaceForStart(self, board, r, c):
        before = board[r][c-1]
        after = board[r][c+1]
        if(after != "." and before == "."):
            word = self.getWord(board[r], c)
            return(word)
        return(False)

    # finds the end of a word where the start point is placed
    def getWord(self, row, startPoint):
        endPoint = testPoint
        while True:
            if(row[endPoint] == "."):
                break
            endPoint += 1

        return(row[startPoint:endPoint])

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

    def checkValidBoard(self, dictionary):
        validWords = self.checkValidWords(dictionary)


    def checkValidPostitions(self):
        board = self.expandBoard(self.board)
        stack = [[9,9]]
        while True:
            coords = stack.pop(0)
            r = coords[0]
            c = coords[1]
            board[r][c] = "."
            stack.extend(self.checkPosition(board, r, c))
            if(len(stack) == 0):
                break

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

    def checkValidWords(self, dictionary):
        words = self.getAllWords()
        valid = True
        for word in words:
            if(not(Dictionary.checkValidPlay(word))):
                valid = False
        return(valid)

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

        for

        numChanges = len(changes) - changes.count(".")

if(__name__ == "__main__"):
    b = Board()
    board = ["......a........"
            ,"......l........"
            ,"......p........"
            ,"......h........"
            ,"......a........"
            ,"......b........"
            ,".spaghetti....."
            ,"......t........"
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
