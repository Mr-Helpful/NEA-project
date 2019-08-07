import time
from Scrabble import *
import os

filePrefix = os.getcwd() + "/"
fileName = filePrefix + files[0]
print(fileName)
dictFile = "DictTree"
dictionary = filePrefix + dictFile
dictionary = "/Users/acolby/OneDrive - The Perse School/NEA/Code/Scrabble checker/DictTree"
print(dictionary)

'''
lines = get_entries(fileName)

print("retrieving dictionary")
timeR1 = time.time()
dictionary = retrieve_dictionary(dictionary)
timeR2 = time.time()
print("done in {:.5f} seconds\n".format(timeR2-timeR1))

rootNode = Trie()

print("converting dictionary into a Trie")
timeT1 = time.time()
rootNode.store_words(dictionary)
# adds a self referential pointer to the root Tree object
# this allows for words to be found at any point in a row
rootNode.add_child(rootNode)
timeT2 = time.time()
print("done in {} seconds\n".format(timeT2-timeT1))

pattern = "..............."
hand = ""
hand = pick_tiles(hand)

print("")
print("find_words checking for " + pattern)
print("with a hand of " + hand)
timeM1 = time.time()
allMatches = rootNode.fit_Row(pattern,hand)
timeM2 = time.time()
print("{} matches found in {:.5f} seconds\n".format(len(allMatches),timeM2-timeM1))

row = pattern

print("finding the best possible play from matches")
timeX1 = time.time()
bestMatch = check_max_play(allMatches,row,pattern)
timeX2 = time.time()
print("The best match is {} with {} points scored after {:.5f} seconds\n".format(bestMatch[0],bestMatch[1],timeX2-timeX1))

print("checking split_pattern functionality\n")
splitPattern(pattern)

print("")
print("creating a new user")
player1 = Player("Edward")
password = "this_is_my_password"                    # of course wouldn't be physically included in the actual code
print("finding hash for {} with user {}".format(password,player1.get_name()))
player1.check_admin(password)
'''

dictionary = retrieve_dictionary(dictionary)
rootNode = dictionary._rootNode
rootNode = dictionary.find_child(rootNode,"x")[0]
rootNode = dictionary.find_child(rootNode,"u")[0]
dictionary.print_tree(CurNode=rootNode)

print("Done1")

solutions = dictionary.fit_Row(Row = "....e...r.q....")
print(solutions)

print("Done2")
