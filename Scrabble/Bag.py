import random

class Bag:
    def __init__(self):
        self.bag = self.defaultBag()

    def defaultBag(self):
        return([["a",1,9]
               ,["b",3,2]
               ,["c",3,2]
               ,["d",2,4]
               ,["e",1,12]
               ,["f",4,2]
               ,["g",2,3]
               ,["h",4,2]
               ,["i",1,9]
               ,["j",8,1]
               ,["k",5,1]
               ,["l",1,4]
               ,["m",3,2]
               ,["n",1,6]
               ,["o",1,8]
               ,["p",3,2]
               ,["q",10,1]
               ,["r",1,6]
               ,["s",1,4]
               ,["t",1,6]
               ,["u",1,4]
               ,["v",4,2]
               ,["w",4,2]
               ,["x",8,1]
               ,["y",4,2]
               ,["z",10,1]
               ,[".",0,2]
               ])

    def getTiles(self, noTiles):

        newTiles = []
        for _ in range(noTiles):
            self.tiles = random.shuffle(self.tiles)


    def removeTile(self)
