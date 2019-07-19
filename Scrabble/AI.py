import Player

class AI(player):
    def __init__(self):
        pass

    def makemove(self,board):
        # overwrites the player's makemove method preventing it from being used
        pass

    def getmoves(self,board):
        # move the brute force method to here
        pass

    def scoremoves(self,moves,weighting):
        # rates the moves found using their score and some basic heuristics
        pass
