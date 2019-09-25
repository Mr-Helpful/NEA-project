import Player

class AI(player):
    def __init__(self):
        pass

    def makeMove(self,board):
        # overwrites the player's makemove method preventing it from being used
        pass

    def getMoves(self,board):
        # move the brute force method to here
        pass

    def scoreMoves(self,moves,weighting):
        # rates the moves found using their score and some basic heuristics
        pass
