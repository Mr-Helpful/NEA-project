import Play

class Player:
    def __init__(self, name, handSize, bag, imageName = None):
        self.name = name
        self.imageName = imageName

    def takeTurn(self, game):
        menu = {"1":self.makeMove, "2":self.passTurn}
        nPlay = Play.Play()
        turnStillInPlay = True

        startStr = "It is {}'s turn\n".format(self.name)

        while(turnStillInPlay):
            choice = game.GUI.takeTurn(menu, startStr)
            turnStillInPlay = choice(game, nPlay)

        return(nPlay)

    # ask the user to make a move through the GUI
    def makeMove(self, game, nPlay):
        game.GUI.makeMove(game, self, nPlay)
        game.GUI.confirmPlay(game, self, nPlay)

        if(nPlay.confirmed):
            return(False)

        return(True)

    def passTurn(self, game, nPlay):
        nPlay.confirmed = "passed"
        return(False)

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
