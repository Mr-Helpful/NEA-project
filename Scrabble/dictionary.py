'''
A trie based mathod of storing a dictionary.
This allows it to be more compact and allow for faster searching
'''
import copy

class Dictionary:
    def __init__(self):
        self.Trie = self.retrieveDict()
        pass

    def retrieveDict(self):
        # retreives the trie for use in the program
        trieCheck = self.checkForTrie()
        wordCheck = self.checkForWords()
        if(trieCheck):
            self.readTrie(trieCheck)
        elif(wordCheck):
            self.convertWords(wordCheck)
        else:
            raise Exception("No dictionary found upon initialisation")
        pass

    def checkForTrie(self):
        # checks if there is a pre-existing trie from which it can load the dictionary
        pass

    def checkForWords(self):
        # checks if there is a word list available to convert into a trie
        pass

    def convertWords(self, words):
        # removes words longer than 15 letters
        # > this makes the trie smaller
        # > and makes the search more efficient
        # also, in a similar vein, removes words with more letters than in the scrabble word bag
        # > for example "zzz" is not a valid word as it has more "z"s than are in the word bag
        # then converts a list of words to a trie
        
        pass

    def readTrie(self, trieFile):
        # uses pickle to open a pre-existing trie object
        pass

    def storeTrie(self, trie):
        # uses pickle to store the trie once converted
        pass

    def checkForWord(self, word):
        # checks if a word is present within the trie structure
        self.Trie.checkForWord(word)



class Node:

    # defines the initialisation of a single node object
    # "" defines a root node
    def __init__(self,value):

        # defines the value of the node
        # will either be defined as an alphabetic character
        # or an empty string for the root Tree object
        # the end of the word node's value is defined as the EOW character
        # end of word node have node children connected to it
        self.value = value

        # defines the children of the Node
        # this will be used to move through the tree
        self.children = []

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
        self._rootNode = Node(".")

    # prints the entire trie connected to the node from which this method is called
    # mostly used for debug version
    # slightly laggy if used on a particularly large tree
    # due to the fact that it uses a lot of printing
    # setting CurNode and starter to 0 is used as a flag that these need to be updated
    # this is required as they can't be defaulted to a value relating to self as this hasn't been recognised yet
    def print_tree(self,CurNode = 0,starter = 0):

        # if CurNode is 0
        # updates CurNode to the correct value
        # used as self is defined in the parameters
        # and therefore cannot be used in default values
        if(CurNode == 0):
            CurNode = self._rootNode

        # updates starter to the correct value
        if(starter == 0):
            starter = self.startTree

        # prints out the branch of the tree
        print(starter + CurNode.value)

        # calls itself on every node in the current node's children
        for node in CurNode.children:
            self.print_tree(node," |"+starter)

# defines a Trie
class Trie(Tree):

        # defines the character used to end a word
        EOW = ")"

        def findChild(self,node,char):
            # firstly defines charCheck as False
            # this will remain the value of charcheck if it fails to find the relevant node
            charCheck = False

            # iterates over the current node's children
            for Cnode in node.children:

                # checks if the value of the node fits the character being searched for
                if(Cnode.value == char):

                    # if so it updates the value of charCheck to the node conataining this character
                    # it is formatted as a list for ease of use later
                    charCheck = Cnode

            # if the value is blank it returns all of the children
            if(char == "."):
                return(node.children)

            return(charCheck)

        # checks if a node contributes the end of a word
        def checkEnd(self,node):

            # if the node is attached to an EOW node
            if(self.findChild(node,self.EOW)):

                # it can be considered the end of the word
                return(True)

            # otherwise it isn't
            return(False)

        # stores an entire word in the trie
        # makes use of the self.add_child() method
        def storeWord(self, word):

            # root is the node object currently being worked on
            root = self._rootNode

            # goes through each character in the word
            for char in word:

                # does a check for the correct character in the current nodes children

                charCheck = self.findChild(root,char)

                # checks whether a node doesn't exist for the correct letter
                if(not(charCheck)):

                    # if no node object exists, it creates a new node object to store the word
                    newNode = Node(char)
                    root.children.append(newNode)
                    root = newNode
                else:

                    # otherwise it will just navigate down that node
                    root = charCheck
            endNode = Node(self.EOW)
            root.children.append(endNode)

        # allows for storage of a list of words at once
        def storeWords(self, words):

            # iterates through words and calls storeWord() on each one
            for word in words:
                self.storeWord(word)

        # returns a list of all the words stored within the tree
        def retrieveWords(self, node = 0, string = ""):

            # self._rootNode cannot be used as a default
            # so this represents a hack to set it as default
            if(node == 0):
                node = self._rootNode

            # if it encounters an end of word character, it will return the finished string
            if(node.value == self.EOW):
                return(string)

            # builds up a string using the previous part of the string and the character stored at the node
            newString = string + node.value

            # sets up the empty wordlist at the start and fills it using recursion
            wordList = []
            for child in node.children:

                # passes the implementation down the layers
                wordList.extend(self.retrieveWords(child,newString))

            # passes the extended wordList up the layers
            return(wordList)

        # gives an efficient method for searching for a word within the Trie
        def checkForWord(self, word):
            # stores all the nodes being processed
            nodes = [self._rootNode]

            for char in word:
                newNodes = []
                for node in nodes:
                    if(self.findChild(node,char)):
                        newNodes.extend(self.findChild(node,char))
                nodes = newNodes

            nodes = [node for node in nodes if(checkEnd(node))]
            if(len(nodes) == 0):
                return(False)
            return(nodes)

        # prunes the tree to only represent letters present in the hand and row
        # this allows a simpler approach to finding the plays that work for the row
        # idea from: https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
        def pruneTree(self, letters, ordered = 0):
            newNodes = copy.copy(self._rootNode)

            # initialises the stack with the copy of the rootNode and the letters used
            stack = [[newNodes,letters]]

            # only stops when it fully empties the stack
            while(len(stack) != 0):

                # pops the first frame off of the stack
                frame = stack.pop(0)

                # processes it and adds the new frames returned to the
                newFrames = self.processFrame(frame, ordered)
                stack.extend(newFrames)

            return(newNodes)


        # processes a single frame from pruneTree
        def processFrame(self, frame, ordered):

            # defines the parts of the frame being processed
            [node, letters] = frame

            # if the letters are supposed to be removed in order
            if(ordered):

                # only the first letter is processed
                letters = letters[0]

            # removes all duplicates from the letters
            letters = list(set(letters))

            # initiates the new frames to be added to the stack, to be filled later
            frames = []
            for letter in letters:

                # creates a shallow copy
                # this prevents it from interfering with the list from the frame
                cLetters = copy.copy(letters)
                cLetters.remove(letter)

                # gets all the nodes with the correct letter(s) associated to it
                nodes = findChild(node,letter)

                # checks if there are any nodes to follow
                if(nodes):

                    # and creates a new frame for each one
                    newFrames = [[node,cLetters] for node in nodes]
                    frames.extend(newFrames)

            # replaces the children of the current node
            # used in order to prune the tree
            children = [frame[0] for frame in frames]
            node.children = children

            # returns the, filled, new frames
            return(frames)

        # removes parts of the tree which do not represent full words
        def clipTree(self, node):

            # iterates through children, if there are any
            for child in children:
                self.clipTree(child)

            # if there isn't a continuation to the word, or an end to it
            if(len(node.children) == 0):

                # it'll delete the node
                del node

            pass


        def fitRow(self, Row, Hand = ".e.ar.."):

            # defines the node to be constructed from
            node = self._rootNode

            # prunes the tree using the player's hand
            node = self.pruneTree(node, Hand)

            # prunes the tree using the row on the board
            node = self.pruneTree(node, Row, ordered = 1)

            self.clipTree(node)

            # retrieves all the possible words from this new tree
            Solutions = self.retrieveWords(node)

            return(Solutions)

if(__name__ == "__main__"):
    # testing code here

    pass
