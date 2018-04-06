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

        # print(type(text))
        # print("text is: {}".format(text[0]))
        # print("text type is: {}".format(type(text)))
        # print("text type is: {}".format(type(text[0])))
        i = 1
        
        for each_row in text:
            # print(each_row[1])
            # print(each_row[0])
            counter = 1
            len_row = len(each_row)
            while counter < len_row:
                # print(each_row[counter])
                unigram_2 = each_row[counter]
                unigram_1 = each_row[counter - 1]
                if unigram_1 in self.nGramCounts:
                    if unigram_2 in self.nGramCounts[unigram_1]:
                        self.nGramCounts[unigram_1][unigram_2] += 1
                    else:
                        self.nGramCounts[unigram_1][unigram_2] = 1
                else:
                    self.nGramCounts[unigram_1] = {unigram_2 : 1}
                counter += 1
        
        # previous_token = text[each_row][i - 1]
        # current_token = text[0][i]

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 1
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """
        last_word = sentence[-1]
        
        if last_word in self.nGramCounts:
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
                  BigramModel sees as candidates, see the spec.
        """
        last_word = sentence[-1]
        return self.nGramCounts[last_word]

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your test cases here

    # An example trainModel test case
    bigram = BigramModel()
    text = [ ['the', 'quick', 'brown', 'fox'], ['jumped', 'over', 'the', 'quick'] ]
    bigram.trainModel(text)
    print("Should print the counts of all the bigrams, with 'the quick' happening twice")
    print(bigram)

    # An example trainingDataHasNGram test case
    bigram = BigramModel()
    sentence = ['The','sly','brown']
    print("Should be false\n{}".format(bigram.trainingDataHasNGram(sentence))) # should be False cuz nothing inside
    bigram.trainModel(text)
    print("should be true\n{}".format(bigram.trainingDataHasNGram(sentence)))
    print("")
    
    # getCandidateDictionary tset case
    bigram = BigramModel()
    bigram.trainModel(text)    
    print("This should just print out the value for 'brown'.\n{}" \
    .format(bigram.getCandidateDictionary(sentence)))
