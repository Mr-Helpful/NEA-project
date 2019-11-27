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

if(__name__ == "__main__"):
    pass
