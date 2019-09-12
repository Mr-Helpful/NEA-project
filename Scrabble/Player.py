class Player:
    def __init__(self, name, hand = ""):
        self.name = name
        self.hand = hand
        pass

    # ask the user to make a move through the GUI
    def makeMove(self):
        pass

    # checks whether a move made by a player is valid
    def checkMove(self, move):
        pass

    # returns the player's hand
    def getHand(self):
        return(self.hand)

    def addTiles(self, newTiles):
