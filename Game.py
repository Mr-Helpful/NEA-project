class Game:
    def __init__(self, players, board, bag, GUI):
        self.players = players
        self.playerScores = {player: 0 for player in players}
        self.passedTurns = {player: 0 for player in players}
        self.board = board
        self.bag = bag
        self.GUI = GUI
        self.gameOngoing = True
        print("new game initialised")
        self.play()

    def play(self):
        while(self.gameOngoing):
            self.takeTurn()

    def endGame(self):
        # give each player the option to pass a turn. If one of them passes three consecutive turns in a row the game is over
        # this will need a method to stop players "ragequitting", when they reach a score higher than the AI and winning against it that way
        # maybe just disable this method of checking when playing against an AI
        # or refine it to when a player has passed three turns in a row AND the bag is empty.
        pass

    def takeTurn(self):
        for player in self.players:
            self.takePlayerTurn(player)

    def takePlayerTurn(self, player):
        print("\nIt is {}'s turn".format(player.name))
        turnStillInPlay = True
        menu = {"1":self.printBoard, "2":self.tryMove, "3":self.passTurn}
        while(turnStillInPlay):
            choice = self.GUI.takeTurn(menu)
            turnStillInPlay = choice(player)
            print("turnStillInPlay: {}".format(turnStillInPlay))

    def printBoard(self, player):
        self.GUI.printBoard(self.board, player)
        return(True)

    def tryMove(self, player):
        player.makeMove(self.board, self.GUI, self.bag)
        check, rowColumn, orientation, play = self.GUI.makeMove(self.board, player, self)
        if(not(check)):
            return(True)

        board = self.board.editBoard(rowColumn, orientation, play)
        confirmed = self.GUI.confirmPlay(rowColumn, orientation, play, board, player)
        print("play confirmed: {}".format(confirmed))
        if(confirmed):
            player.makeMove(self.board, self.GUI, self.bag)
            return(False)
        return(True)

    def passTurn(self, player):
        if(self.bag.isEmpty()):
            self.passedTurns[player] += 1
        if(self.passedTurns[player] >= 3):
            self.gameOngoing = False
        return(False)

    def checkMove(self, rC, orientation, play, player):
        boardCorrect = self.board.checkValidPlay(rC, orientation, play)
        lineChanges = self.board.getChanges(rC, orientation, play)
        handCorrect = player.checkValidPlay(lineChanges)
        print("handCorrect: {}".format(handCorrect))

        if(boardCorrect and handCorrect):
            return(True, lineChanges)
        return(False, lineChanges)
