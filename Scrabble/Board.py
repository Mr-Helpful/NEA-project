

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

    def checkValidBoard(self, Dictionary):
        words = self.getAllWords()
        valid = True
        for word in words:
            if(not(Dictionary.checkValidPlay(word))):
                valid = False
        return(valid)

    # orientation refers to whether the play is made across or down the board
    # rC refers to the number of the row/column of the board the play was made in
    def scorePlay(self, orientation, rC, play, tiles):
        board = self.board
        if(orientation == "down"):
            board = self.getFlippedBoard(board)

        line = board[rC]

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
