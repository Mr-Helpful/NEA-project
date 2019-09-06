

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

    def checkValidBoard(self,Dictionary):
        words = self.getAllWords()
        valid = True
        for word in words:
            if(not(Dictionary.checkValidPlay(word))):
                valid = False
        return(valid)

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
