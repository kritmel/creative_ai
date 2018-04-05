import random
from nGramModel import *


class BigramModel(NGramModel):

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary. For examples
                  and pictures of the BigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.
        """
        len_text = len(text)
        i = 0
        while i > len_text:
            if i > 0:
                if text[i - 1] in self.nGramCounts:
                    self.nGramCounts[word] += 1
            if word in self.nGramCounts:
                self.nGramCounts[word] += 1
            elif (word != "^::^") or (word != "^:::^"):
                self.nGramCounts[word] = 1

        for sentence in text:
            for word in sentence:
                if word in self.nGramCounts:
                    self.nGramCounts[word] += 1
                elif (word != "^::^") or (word != "^:::^"):
                    self.nGramCounts[word] = 1


    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 1
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """
        pass

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  BigramModel sees as candidates, see the spec.
        """
        pass

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your test cases here
    pass
