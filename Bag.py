import random
import copy

class Bag:
    def __init__(self, standard = True):
        if(standard):
            self.bag = self.defaultBag()
            self.scores = self.defaultScores()

    def defaultBag(self):
        return(list("a"*9
                   +"b"*2
                   +"c"*2
                   +"d"*4
                   +"e"*12
                   +"f"*2
                   +"g"*3
                   +"h"*2
                   +"i"*9
                   +"j"*1
                   +"k"*1
                   +"l"*4
                   +"m"*2
                   +"n"*6
                   +"o"*8
                   +"p"*2
                   +"q"*1
                   +"r"*6
                   +"s"*4
                   +"t"*6
                   +"u"*4
                   +"v"*2
                   +"w"*2
                   +"x"*1
                   +"y"*2
                   +"z"*1
                   +"."*2))

    def defaultScores(self):
        return({"a":1
               ,"b":3
               ,"c":3
               ,"d":2
               ,"e":1
               ,"f":4
               ,"g":2
               ,"h":4
               ,"i":1
               ,"j":8
               ,"k":5
               ,"l":1
               ,"m":3
               ,"n":1
               ,"o":1
               ,"p":3
               ,"q":10
               ,"r":1
               ,"s":1
               ,"t":1
               ,"u":1
               ,"v":4
               ,"w":4
               ,"x":8
               ,"y":4
               ,"z":10
               ,".":0})

    def isEmpty(self):
        return(len(self.bag) == 0)

    def getTiles(self, noTiles, modify = True):
        if(modify):
            bag = self.bag
        else:
            bag = self.bag[:]

        random.shuffle(bag)
        tiles = bag[:noTiles]
        bag = bag[noTiles:]
        return(tiles)

    def removeTile(self, bag, tile):
        bag.remove(tile)
        return(tile)

    def checkWordInBag(self, word):
        # performs a shallow copy on self.bag
        bag = self.bag[:]

        for letter in word:
            if(letter in bag):
                bag.remove(letter)
            elif("." in bag):
                bag.remove(".")
            else:
                return(False)

        return(True)

if(__name__ == "__main__"):
    # testing here
    b = Bag()

    word = "alphabetic"
    print("checking '{}':\n".format(word) + str(b.checkWordInBag(word)))

    word = "zzzz"
    print("checking '{}':\n".format(word) + str(b.checkWordInBag(word)))

    noTiles = 5
    print("\nGetting {} new letters".format(noTiles))
    print(b.getTiles(noTiles))
