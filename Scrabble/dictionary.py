'''
A trie based mathod of storing a dictionary.
This allows it to be more compact and allow for faster searching
'''

class dictionary:
    def __init__(self):
        Trie = self._retrive_dict()
        pass

    def _retrive_dict(self):
        # retreives the trie for use in the program
        trieCheck = self._check_for_trie()
        wordCheck = self._check_for_words()
        if(trieCheck):
            self._read_trie(trieCheck)
        elif(wordCheck):
            self._convert_words(wordCheck)
        else:
            raise Exception("No dictionary found upon initialisation")
        pass

    def _check_for_trie(self):
        # checks if there is a pre-existing trie from which it can load the dictionary
        pass

    def _check_for_words(self):
        # checks if there is a word list available to convert into a trie
        pass

    def _convert_words(self,words):
        # converts a list of words to a trie
        pass

    def _read_trie(self,trie):
        # uses pickle to open a pre-existing trie object
        pass

    def _store_trie(self,trie):
        # uses pickle to store the trie once converted
        pass
