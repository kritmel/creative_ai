import random
import sys
import json
from musicInfo import *

class NGramModel(object):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable.
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.
                  This function is done for you.
        """
        return self.__class__.__name__ + ':\n' +\
            json.dumps(
                       self.nGramCounts,
                       sort_keys=True,
                       indent=4,
                       separators=(',', ': ')
            )

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary.
                  It does not need to be modified here because you will
                  override it in the NGramModel child classes according
                  to the spec.
        """
        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns a bool indicating whether or not this n-gram model
                  can be used to choose the next token for the current
                  sentence. This function does not need to be modified because
                  you will override it in NGramModel child classes according
                  to the spec.
        """
        pass

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. This function does not need to be
                  modified because you will override it in the NGramModel child
                  classes according to the spec.
        """
        pass

    def weightedChoice(self, candidates):
        """
        Requires: candidates is a dictionary; the keys of candidates are items
                  you want to choose from and the values are integers
        Modifies: nothing
        Effects:  returns a candidate item (a key in the candidates dictionary)
                  based on the algorithm described in the spec.
        """
        # Make some lists
        key_list = []
        value_list = []
        
        # Extract key and values and append to respective lists
        for i in candidates:
            key_list.append(i)
            value_list.append(candidates[i])
        
        # create a cumulative list
        cumulative_list = []
        total = 0
        for i in value_list:
            total += i
            cumulative_list.append(total)
        
        # Create a dictionary where {token: cumulative number}
        new_dict = {}
        temp_idx = 0
        for i in cumulative_list:
            new_dict[i] = key_list[temp_idx]
            temp_idx += 1
        
        # pick a random number from 0 to whatever total was
        index_key = random.randrange(0, total)
        
        # loop through the dictionary you made two steps ago and 
        # wherever the key is <= to the random number, spit out the value of dictionary
        for i in new_dict:
            if index_key <= i:
                return new_dict[i]
            else: pass

    def getNextToken(self, sentence):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: nothing
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  For more information on how to put all these functions
                  together, see the spec.
        """
        return weightedChoice(getCandidateDictionary(sentence))

    def getNextNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from getNextToken, see the spec.
        """
        allCandidates = getCandidateDictionary(musicalSentence)
        constrainedCandidates = {}
        
        # Walk through the allCandidates dictionary and examine each key
        for i in allCandidates:
            if i[0][0] is in possiblePitches:
                constrainedCandidates[i] = allCandidates[i]
            elif i == "$:::$" :
                constrainedCandidates[i] = allCandidates[i]
        
        if constrainedCandidates != {}:
            return weightedChoice(constrainedCandidates)
        else:
            note = str(random.choice(possiblePitches)) + '4'
            duration = random.choice(NOTE_DURATIONS)
            return (note, duration)

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your tests here
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    choices = { 'the': 2, 'quick': 1, 'brown': 1 }
    nGramModel = NGramModel()
    print(nGramModel)
