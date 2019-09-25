import AI
import Board
import Database
import Dictionary
import Game
import GUI
import Player

class Scrabble:
    def __init__(self):
        self.b = Board.Board()
        self.db = Database.database()
        self.d = Dictionary.Dictionary()
        self.GUI = GUI.GUI()
        self.run()

    def run(self):
        choice = self.GUI.mainScreen(self.b)
        self.choice()

    def exit(self, *args):
        self.GUI.exit()

    def playGame(self):
        self.game = Game.Game(players, self.board, self.DB)
