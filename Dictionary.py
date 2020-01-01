'''
A trie based mathod of storing a dictionary.
This allows it to be more compact and allow for faster searching
'''
import pickle
import copy
import time
import os

import Bag

class Dictionary:
    dataFolder = "Data"
    def __init__(self, trieFile, wordFile, bag):
        self.writeTrie = "/Users/acolby/Documents/School_Work/_Computer_science/NEA-project/Scrabble/Data/"
        self.trie = self.retrieveDict(trieFile, wordFile, bag)

    def retrieveDict(self, trieFiles, wordFiles, bag):
        t1 = time.time()
        # retreives the trie for use in the program
        trie = self.readTrie(trieFiles)

        # optimisation: don't do this unless trie does not exist
        words = self.readWords(wordFiles)

        # this if is used to check if a trie file already exists and if it does
        # then it will skip all later parts of the selection statement
        if(trie):
            pass

        # if a trieFile cannot be found but a word file can
        elif(words):

            # then it uses the words list to create a trie
            trie = self.convertWords(words, bag)

            # finally it stores the newly made trie in the trieFile to make booting
            # faster next time
            # on average, this leads to a time save factor of 6.3*
            self.storeTrie(trie, trieFiles)

        # if neither a trieFile or a wordFile can be found, it throws an error
        else:
            raise Exception("No dictionary found upon initialisation")
        t2 = time.time()
        print("trie loaded in {:.2f} seconds".format(t2-t1))
        return(trie)

    def convertWords(self, words, bag):
        # removes words longer than 15 letters
        # > this makes the trie smaller
        # > and makes the search more efficient
        # also, in a similar vein, removes words with more letters than in the scrabble word bag
        # > for example "zzzz" is not a valid word as it has more "z"s (and blanks) than are in the word
        # This leads to a reduction by 30,878,791 bytes / 31,999,201 bytes = 96.5%

        # then converts a list of words to a trie

        for word in words:
            if(not(bag.checkWordInBag(word))):
                words.remove(word)

        trie = Trie(15, words)
        return(trie)

    def readWords(self, wordFiles):
        for file in wordFiles:
            try:
                with open(file, "r") as f:
                    lines = f.read().split("\n")
                    # opens a pre-existing words file and returns it as a list
                return(lines)
            except FileNotFoundError:
                pass
        return(False)

    def readTrie(self, trieFiles):
        for file in trieFiles:
            try:
                with open(file, "rb") as f:
                    # uses pickle to open a pre-existing trie object
                    trie = pickle.load(f)
                return(trie)
            except(FileNotFoundError, EOFError):
                pass
        return(False)

    def storeTrie(self, trie, trieFile):
        with open(trieFile[0], "wb") as f:
            # uses pickle to store the trie once converted
            pickle.dump(trie, f)

    def checkForWord(self, word):
        # checks if a word is present within the trie structure
        return(self.trie.checkForWord(word))


class Node:
    # defines the initialisation of a single node object
    # "." defines a root node
    def __init__(self):
        self.children = {}

# defines a node used to construct a trees
# this will later be used to construct a trie

# Trie:
# A type of tree used to store words
# allows for easier lookup of words stored
# will be used later to dramatically decrease lookup times

class Tree():

    # defines the character to start a tree drawing on
    startTree = "-"

    # defines the character to extend a tree drawing with
    extendTree = "|-"

    # defines the values needed to initialise a Tree object object
    # "" must be used to represent a root node of a tree
    def __init__(self):

        # defines the root Node of the tree as a Node with value ""
        self._rootNode = Node()

    # prints the entire trie connected to the node from which this method is called
    # mostly used for debug version
    # slightly laggy if used on a particularly large tree
    # due to the fact that it uses a lot of printing
    # setting CurNode and starter to 0 is used as a flag that these need to be updated
    # this is required as they can't be defaulted to a value relating to self as this hasn't been recognised yet
    def printTree(self,CurNode = 0,starter = 0):

        # if CurNode is 0
        # updates CurNode to the correct value
        # as self is defined in the parameters
        # and therefore cannot be used in default values
        if(CurNode == 0):
            CurNode = self._rootNode

        # updates starter to the correct value
        if(starter == 0):
            starter = self.startTree

        # calls itself on every node in the current node's children
        for key, node in CurNode.children.items():
            print(starter + key)
            self.printTree(node," |"+starter)

# defines a Trie
class Trie(Tree):

        # defines the character used to start a word
        SOW = "("

        # defines the character used to end a word
        EOW = ")"

        # defines the character used to start the trie from the beginning
        repeatChar = "§"

        def __init__(self, trieSize, words):
            self._rootNode = Node()
            self._startNode = Node()

            self._rootNode.children["("] = self._startNode
            self.setup(trieSize, words)

        def findChild(self, node, char):

            # if the value is blank it returns all of the children
            if(char == "."):
                return(node.children.values())

            # the .get method is used here instead of just indexing the dictionary
            # this is because if the item does not exist in the dictionary it will return None
            val = node.children.get(char)

            # when forced to a boolean (used in if statements) None becomes False
            # therefore val can simply be returned here
            return(val)

        # checks if a node contributes the end of a word
        def checkEnd(self,node):

            # returns True only if None is not returned from findChild
            val = bool(self.findChild(node, self.EOW))

            return(val)

        # stores an entire word in the trie
        # makes use of the self.add_child() method
        def storeWord(self, word):

            # root is the node object currently being worked on
            root = self._startNode

            # goes through each character in the word
            for char in word:

                # does a check for the correct character in the current nodes children

                charCheck = self.findChild(root, char)

                # checks whether a node doesn't exist for the correct letter
                if(not(charCheck)):

                    # if no node object exists, it creates a new node object to store the word
                    newNode = Node()
                    root.children[char] = newNode
                    root = newNode
                else:

                    # otherwise it will just navigate down that node
                    root = charCheck
            endNode = Node()
            root.children[self.EOW] = endNode


        # allows for storage of a list of words at once
        def storeWords(self, trieSize, words):
            nWords = []

            # iterates through words and calls storeWord() on each one
            for word in words:
                if(len(word) >= trieSize):
                    self.storeWord(word)
                    nWords.append(word)

            return(nWords)

        # defines the function used to populate and format the trie
        def setup(self, trieSize, words):
            words = self.storeWords(trieSize, words)
            print("trie with size {} set up".format(trieSize))

            # if the trie does not comprise of only one letter words
            # then it will create a new trie and add it to itself
            # however this trie will be one branch shorter
            if(trieSize != 1):
                newTrie = Trie(trieSize - 1, words)
                self._rootNode.children["§"] = newTrie._rootNode
                pass

        # returns a list of all the words stored within the tree
        # this represents a somewhat depth first search of the trie
        # the trie will also never be more than 15 items deep
        # due to these two reasons the depth of the call stack for this recursive implementation
        # will never be more than 15 frames and the recursion is unlikely to ever cause an error.
        def retrieveWords(self, node = 0, string = ""):

            # self._startNode cannot be used as a default
            # so this represents a hack to set it as a default
            if(node == 0):
                node = self._startNode

            # sets up the empty wordlist at the start and fills it using recursion
            wordList = []

            for key, value in node.children.items():

                # if a word has a EOW character connected to it, we add it to the wordList
                if(key == self.EOW):
                    wordList.append(string)

                # an else is used as we don't want the function to consider the branches off of EOW characters
                else:
                    # builds up a string using the previous part of the string and the character stored at the node
                    newString = string + key

                    # passes the implementation down the layers
                    wordList.extend(self.retrieveWords(child,newString))

            # passes the extended wordList up the layers
            return(wordList)

        def negateRow(self, row):
            nRow = list("abcdefghijklmnopqrstuvwxyz") + [self.SOW, self.EOW, self.repeatChar]
            for item in row:
                nRow.remove(item)

            return(nRow)

        def translateRow(self, row):
            # replaces each item in the row with its equivalent list of valid letters
            # ignores lists already in the string

            nRow = []
            for r in row:
                if(type(r) == type([])):
                    nRow.append(r)
                elif(r == "."):
                    nRow.append(list("abcdefghijklmnopqrstuvwxyz") +  # the standard alphabet
                                [self.SOW, self.EOW, self.repeatChar])# and special characters
                else:
                    nRow.append([r])

            nRow = self.negateRow(nRow)
            return(nRow)

        def removeBranches(self, node, unuseable):
            newNode = copy.copy(node)

            for item in unuseable:
                try:
                    del newNode.children[item]
                except KeyError:
                    pass

            return(newNode)

        # prunes the tree to only represent letters present in the hand and row
        # this allows a simpler approach to finding the plays that work for the row
        # idea from: https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
        # for a similar reason to the word retrieval algorithm this method can be recursive
        def pruneForRow(self, row, node = 0):
            if(node == 0):
                node = copy.copy(self._rootNode)

            if(len(row) == 0):
                return()

            fItem = row.pop(0)
            node = self.removeBranches(node, fItem)

            for child in node.children.values():
                self.pruneTree(row, child)

            # removes any items that aren't in the list from the children of the trie
            # this occurs at each branch

            return(node)

        def pruneSubTrie(self, node, hand):

            # this represents the base case
            # the multiplication acts as an OR gate
            # the only nodes for which the length of node.children is 0 are the EOW nodes
            if(len(hand) * len(node.children) == 0):
                return()

            # removing all duplicates from the hand ensures we do not get equivalent calls
            # this reduces the amount of processing required
            sHand = set(hand)

            # called can be a dictionary as they exhibit a similar behavior to sets
            # this is needed as there may be some overlap between the called items
            # for example: "." would cause "a" to be called, as would "a"
            # this is also useful as it is the format used to store the nodes
            called = {}

            # this preserves an EOW character if one is present in the children
            # otherwise it would be removed by the algorithm
            end = self.findChild(node, self.EOW)
            if(end):
                called[self.EOW] = end

            for tiles in sHand:
                for tile in tiles:
                    # checks if children are present for the particular node and letter tile
                    children = self.findChild(node, tile)

                    # if children exist for this specific letter tile
                    # then it processes the children
                    if(children):

                        # creates a shallow copy of hand, so that it is not edited by the remove operation
                        newHand = hand[:]
                        # this creates the variable newHand, which is the hand variable with the tile subtracted from it
                        newHand.remove(tile)

                        for child in children:
                            # the recursive aspect
                            self.pruneSubTrie(child, newHand)

                            # adds the child to the dictionary of called nodes
                            called[tile] = child

            # this, in effect, removes all the children of the trie that weren't called during this operation
            node.children = called

        def getSubTries(self, node):
            node = node.children["§"]
            nodes = [node]

            while(node):
                node = node.children["§"]
                nodes.append(node)

            return(nodes)

        def pruneForHand(self, node, hand):
            subTries = self.getSubTries(root)

            for subTrie in self._subTries:
                self.pruneSubTrie(subTrie, hand)

        def checkForWord(self, word, node = 0):
            if(node == 0):
                node = self._startNode

            if(len(word) == 0):
                return(self.checkEnd(node))

            letter = word[0]
            word = word[1:]
            newNode = self.findChild(node, letter)
            if(newNode):
                return(self.checkForWord(word, newNode))
            return(False)

        def fitRow(self, row, hand = ".e.ar.."):
            '''
            This needs a major rewrite!
            '''
            # this formats both the row and the hand correctly for the pruning algorithms
            row = self.translateRow(row)
            row = self.negateRow(row)

            hand = self.translateRow(hand)

            # prunes the tree using the row on the board
            node = self.pruneForRow(Row)

            # retrieves all the possible words from this new tree
            Solutions = self.retrieveWords(node)

            return(Solutions)

if(__name__ == "__main__"):
    # testing code here
    b = Bag.Bag()

    writeTrie = "/Users/acolby/Documents/School_Work/_Computer_science/NEA-project/Scrabble/Data/"
    wordFile = [writeTrie + "WordList"]
    trieFile = [writeTrie + "WordTrie"]
    d = Dictionary(trieFile, wordFile, b)
    w = d.checkForWord("zomotherapeutic")
    print("The word exists" if(w) else "No word matches")

    words = d.fitRow("...f...s.a.....")
