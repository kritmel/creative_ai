import random
from nGramModel import *

class TrigramModel(NGramModel):

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.
        """
        
        for each_row in text:
            counter = 2
            len_row = len(each_row)
            while counter < len_row:
                # print(each_row[counter])
                unigram_3 = each_row[counter]
                unigram_2 = each_row[counter - 1]
                unigram_1 = each_row[counter - 2]
                if unigram_1 in self.nGramCounts:
                    if unigram_2 in self.nGramCounts[unigram_1]:
                        if unigram_3 in self.nGramCounts[unigram_1][unigram_2]:
                            self.nGramCounts[unigram_1][unigram_2][unigram_3] += 1
                        else:
                            self.nGramCounts[unigram_1][unigram_2][unigram_3] = 1
                    else:
                        self.nGramCounts[unigram_1][unigram_2] = {unigram_3: 1}
                else:
                    self.nGramCounts[unigram_1] = {unigram_2 : {unigram_3: 1}}
                counter += 1

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """
        last_word = sentence[-1]
        penultimate = sentence[-2]
        
        if penultimate in self.nGramCounts:
            if last_word in self.nGramCounts[penultimate]:
                return True
        else: 
            return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """
        last_word = sentence[-1]
        penultimate = sentence[-2]
        
        return self.nGramCounts[penultimate][last_word]

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your test cases here
    # An example trainModel test case
    elvis_lyrics = "Wise men say only fools rush in"
    elvis_chorus = "But I can't help falling in love with you"
    elvis_lyric_lst = elvis_lyrics.split(' ')
    elvis_chorus_lst = elvis_chorus.split(' ')
    elvis = [elvis_lyric_lst, elvis_chorus_lst]
    print(elvis)
    
    tri = TrigramModel()
    #text = [ ['the', 'quick', 'brown', 'fox'], ['jumped', 'over', 'the', 'quick'] ]
    tri.trainModel(elvis)
    print("Should print the counts of all the trigrams, with 'the quick' happening twice")
    print(tri)
    
    tri = TrigramModel()
    sentence = ['The','sly','brown']
    print("Should be false\n{}".format(bigram.trainingDataHasNGram(sentence))) # should be False cuz nothing inside
    bigram.trainModel(text)
    print("should be true\n{}".format(bigram.trainingDataHasNGram(sentence)))
    print("")
