'''
A simple class used to encapsulate all of the parts of a play
'''

class Play:
    def __init__(self):
        self.orientation = 0
        self.rC = 0
        self.line = ""
        self.changes = []
        self.confirmed = False
