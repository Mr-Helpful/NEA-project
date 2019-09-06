import GUI

class Player:
    def __init__(self, name, hand = ""):
        self.name = name
        self.hand = hand
        pass

    def makeMove(self):
        # ask the user to make a move through the GUi
        pass

    def checkMove(self, move):
        # checks whether a move made by a player is valid
        pass

    def getHand(self):
        # returns the player's hand
        return(self.hand)

    def setHand(self, hand):
        
