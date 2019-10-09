class Player:
    def __init__(self, name, handSize, bag):
        self.name = name
        self.handSize = handSize
        self.passes = 0
        self.setupHand(bag)

    def setupHand(self, bag):
        newTiles = bag.getTiles(self.handSize)
        self.hand = "".join(newTiles)

    # ask the user to make a move through the GUI
    def makeMove(self, board, GUI, bag):
        rowColumn, orientation, play, changes = GUI.makeMove(board, self, super())
        confirmed = GUI.confirmPlay(rowColumn, orientation, play, board)
        if(confirmed):
            board.makeMove(rowColumn, orientation, play)
            self.changeHand(changes)
            break

    def checkValidPlay(self, changes):
        hand = list(self.hand[:])
        for c in changes:
            if(c in hand):
                hand.remove(c)
            elif("." in hand):
                hand.remove(".")
            else:
                return(False)
        return(True)

    def checkMove(self, rC, orientation, play, board):
        boardCorrect = board.checkValidPlay(rC, orientation, play)
        lineChanges = board.getChanges(rC, orientation, play)

        if(lineChanges):
            handCorrect = self.checkValidPlay(lineChanges)
            if(handCorrect and boardCorrect):
                return(True, lineChanges)
        return(False, lineChanges)

    def changeHand(self, changes, bag):
        for change in changes:
            self.hand.pop(changes)

        newTiles = bag.getTiles(len(changes))
        self.hand.extend(newTiles)

    # returns the player's hand
    def getHand(self):
        return(self.hand)

    def addTiles(self, newTiles):
        pass

if(__name__ == "__main__"):
    pass
