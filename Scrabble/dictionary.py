'''
A trie based mathod of storing a dictionary.
This allows it to be more compact and allow for faster searching
'''

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

    def convertWords(self,words):
        # converts a list of words to a trie
        pass

    def readTrie(self,trie):
        # uses pickle to open a pre-existing trie object
        pass

    def storeTrie(self,trie):
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

            # iterates through words and calls store_word() on each one
            for word in words:
                self.storeWord(word)

        def retrieveWords(self, node = 0, string = ""):
            if(node == 0):
                node = self._rootNode
            wordList = []
            if(node.value == self.EOW):
                return(wordList.append(string))
            newString = string + node.value
            for child in node.children:
                wordList.extend(self.retrieveWords(child,newString))
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
        def pruneTree(self, letters):
            pass


        # tries to find all the possible matches for a row
        # uses a given hand
        # solutions are defaulted to empty on first execution
        # and are then built up over the execution of the function
        # and returned at the end
        # string is defaulted to empty upon initialisation
        # seperate solutions are then built up as string is passed down through the trie
        def fitRow(self, Row, Hand = ".e.ar..", StartString = ""):

            Node = self._rootNode

            PSolutions = [[Row,Hand,Node,StartString]]

            Solutions = []

            while(len(PSolutions) != 0):

                NextItem = PSolutions[0]

                Row = NextItem[0]

                print(NextItem)

                NextChar = Row[0]

                Hand = NextItem[1]

                Node = NextItem[2]

                String = NextItem[3]

                if(len(Row) != 0 and len(Hand) != 0):

                    if(Node.value == self.EOW):

                        print("Solution Found!")

                        Solutions.append(String)

                    if(NextChar == "."):

                        # if a word has not been started yet the tree is still on the root node
                        if(Node == self._rootNode):

                            # the word can be shifted across without playing anything
                            PSolutions.append([Row[1:],Hand,Node,String + Node.value])

                            # goes over every tile in the hand
                            # i.e. the tiles that can be played
                            for char in Hand:

                                # adds the next character from the hand
                                # as it doesn't matter what character this is
                                matches = self.findChild(Node,char)

                                # tests if there are matches on the tree
                                if(matches):

                                    try:

                                        # if there are goes over every item in matches
                                        # this may be multiple matches in the case of a blank tile
                                        for match in matches:
                                            PSolutions.append([Row[1:],Hand.replace(char,"",1),match,String + Node.value])

                                    except:
                                        PSolutions.append([Row[1:],Hand.replace(char,"",1),matches,String + Node.value])

                    # if the space in the row isn't blank, it must be a letter tile
                    else:

                        # there will only ever be one result from a letter char
                        # it will either be an EOW character or
                        match = self.findChild(Node,NextChar)

                        # if find_child returns an answer that is not false it has found a valid branch
                        if(match):

                            # therefore it just navigates down the node without playing anything
                            # as if a tile would be played from the hand it would be like overlapping them on the board
                            PSolutions.append([Row[1:],Hand,match,String + Node.value])

                PSolutions.remove(NextItem)

            # returns solutions
            return(Solutions)
