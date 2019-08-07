# used to store game states, players, etc
# mostly used as all of these are modelled as objects and therefore this is just easier to use
import pickle

# provides an interface for the SQL database
class database:
    def __init__(self,filename):
        self.setup(filename)
        pass
