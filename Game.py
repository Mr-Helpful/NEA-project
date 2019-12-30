class Game:
    DefaultTilesPerPlayer = 7
    def __init__(self, players, board, bag, GUI):
        self.players = players
        self.playerScores = {player.name: 0 for player in players}
        self.playerHands = {player.name: [] for player in players}
        self.passedTurns = {player.name: 0 for player in players}
        self.board = board
        self.bag = bag
        self.GUI = GUI
        self.gameOngoing = True
        print("new game initialised")
        self.setup()
        self.play()

    def setup(self):
        for player in self.players:
            hand = self.playerHands[player.name]
            newTiles = self.bag.getTiles(Game.DefaultTilesPerPlayer)
            hand.extend(newTiles)

    def play(self):
        while(self.gameOngoing):
            self.takeTurn()

        self.endGame()

    def endGame(self):
        self.GUI.displayScores(self)

    def takeTurn(self):
        for player in self.players:
            self.takePlayerTurn(player)

    def takePlayerTurn(self, player):
        # about this point is where the encapsulation in the player class should occur

        nPlay = player.takeTurn(self)

        if(nPlay.confirmed == "passed"):
            self.passedTurn(player)
            return()

        valid = self.checkMove(player, nPlay)
        #valid = True
        if(valid):
            print("valid")
            score = self.board.getScore(self, nPlay)
            print(score)
            self.playerScores[player.name] += score
            self.board.updateBoard(nPlay)
            self.updateHand(player, nPlay)

    # give each player the option to pass a turn. If one of them passes three consecutive turns in a row the game is over
    # this will need a method to stop players "rage quitting", when they reach a score higher than the AI and winning against it that way
    # maybe just disable this method of checking when playing against an AI
    # or refine it to when a player has passed three turns in a row AND the bag is empty.
    def passedTurn(self, player):

        # a debugging step to allow the game to be exited early
        self.passedTurns[player.name] += 1

        if(self.bag.isEmpty()):
            self.passedTurns[player.name] += 1
        if(self.passedTurns[player.name] >= 3):
            self.gameOngoing = False
        return(False)

    def checkMove(self, player, nPlay):
        boardCorrect = self.board.checkValidPlay(nPlay)
        self.board.getChanges(nPlay)
        handCorrect = self.checkValidHand(player, nPlay)

        print("hand:" + str(handCorrect))

        if(boardCorrect and handCorrect):
            return(True)
        return(False)

    def changeHand(self, player, nPlay, copy = True):
        if(copy):
            hand = self.playerHands[player.name][:]
        else:
            hand = self.playerHands[player.name]

        print(hand)
        print(nPlay.changes)

        for c in nPlay.changes:
            if(c == "."):
                pass
            elif(c in hand):
                hand.remove(c)
            elif("." in hand):
                hand.remove(".")
            else:
                return(False)
        return(True)

    def checkValidHand(self, player, nPlay):
        return(self.changeHand(player, nPlay))

    def updateHand(self, player, nPlay):
        self.changeHand(player, nPlay, False)
        noLetters = len(nPlay.changes)

        newTiles = self.bag.getTiles(noLetters)
        hand = self.playerHands[player.name]
        hand.extend(newTiles)
