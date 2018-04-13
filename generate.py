#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import random

from pysynth import pysynth
from data.dataLoader import *
from models.musicInfo import *
from models.unigramModel import *
from models.bigramModel import *
from models.trigramModel import *


# FIXME Add your team name
TEAM = 'The Spinners'
LYRICSDIRS = ['the_beatles']
TESTLYRICSDIRS = ['the_beatles_test']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'
keysig_list = [i for i in KEY_SIGNATURES.keys()]
KEY_SIG = random.choice(keysig_list)

###############################################################################
# Helper Functions
###############################################################################

def output_models(val, output_fn = None):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  outputs the dictionary val to the given filename. Used
              in Test mode. This function has been done for you.
    """
    from pprint import pprint
    if output_fn == None:
        print("No Filename Given")
        return
    with open('TEST_OUTPUT/' + output_fn, 'wt') as out:
        pprint(val, stream=out)

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length. This function has been done for
              you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]
    print("RANDOMLY GENERATED SONG by " + TEAM)
    print("*" * 40)
    print
    for verse in verses:
        for line in verse:
            print (' '.join(line)).capitalize()
        print

def trainLyricModels(lyricDirs, test=False):
    """
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.
              Returns the list of trained models.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    for ldir in lyricDirs:
        lyrics = loadLyrics(ldir)
        for model in models:
            model.trainModel(lyrics)
    return models

###############################################################################
# Core
###############################################################################

def trainMusicModels(musicDirs):
    """
    Requires: lyricDirs is a list of directories in data/midi/
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    # call dataLoader.loadMusic for each directory in musicDirs
    for mdir in musicDirs:
        music = loadMusic(mdir)
        for model in models:
            model.trainModel(music)
    return models


def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  returns the best possible model that can be used for the
              current sentence based on the n-grams that the models know.
              (Remember that you wrote a function that checks if a model can
              be used to pick a word for a sentence!)
    """
    if models[0].trainingDataHasNGram(sentence):

        # print("returning models[0]")
        return models[0]
    elif models[1].trainingDataHasNGram(sentence):
        # print("returning models[1]")
        return models[1]
    else:
        return models[2]

def generateLyricalSentence(models, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']
    currentLength = 0

    # print("The models are: {}".format(models))
    while sentenceTooLong(desiredLength, currentLength) == False:
        modelType = selectNGramModel(models, sentence)
        newToken = modelType.getNextToken(sentence)
        if newToken == '$:::$':
            break
        else:
            sentence.append(newToken)
            currentLength += 1
            # print(newToken)
    return sentence[2:]


def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateLyricalSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """
    sentence = ['^::^', '^:::^']
    currentLength = 0
    while sentenceTooLong(desiredLength, currentLength) == False:
        modelType = selectNGramModel(models, sentence)
        newToken = modelType.getNextNote(sentence, possiblePitches)
        if newToken == '$:::$':
            break
        else:
            sentence.append(newToken)
            currentLength += 1
            # print (newToken)
    return sentence[2:]

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []
    
    #Generates a repeated phrase to be used in the lyrics
    repeatedPhrase = generateLyricalSentence(models, 3)
    
    #Generates the verses with an ABCB structure
    for i in range (0, 3):
        verseOne.append(generateLyricalSentence(models, 12))
        verseTwo.append(generateLyricalSentence(models, 12))
    verseOne.append(verseOne[1])
    verseTwo.append(verseTwo[1])

    #Generates the chorus with an ABAB structure
    for i in range (0, 2):
        chorus.append(generateLyricalSentence(models, 12))
        chorus[i] += repeatedPhrase
    chorus.append(chorus[0])
    chorus.append(chorus[1])

    printSongLyrics(verseOne, verseTwo, chorus)

def runMusicGeneratorBass(models, songName):
    print("key signature is: {}".format(KEY_SIG))
    possiblePitches = KEY_SIGNATURES[KEY_SIG]
    pentatonicScale = possiblePitches[0:2] + possiblePitches[4:5]
    tuplesList = generateMusicalSentence(models, 50, pentatonicScale)
    pysynth.make_wav(tuplesList, fn = songName)

def runMusicGeneratorMelody(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  uses models to generate a song and write it to the file
              named songName.wav
    """
    print("key signature is: {}".format(KEY_SIG))
    possiblePitches = KEY_SIGNATURES[KEY_SIG]
    tuplesList = generateMusicalSentence(models, 50, possiblePitches)
    pysynth.make_wav(tuplesList, fn = songName)
    
    """
    intro = generateMusicalSentence(models, 15, possiblePitches)
   
    #Generates verse with structure ABCB
    verseA = generateMusicalSentence(models, 10, possiblePitches)
    verseB = generateMusicalSentence(models, 15, possiblePitches)
    verseC = generateMusicalSentence(models, 10, possiblePitches)
    verse = verseA + verseB + verseC + verseB
    '''
    #print("verseA is: {}".format(verseA))
    #print("verseB is: {}".format(verseB))
    #print("verseC is: {}".format(verseC))
    #print("verse is: {}".format(verse))
    '''
   
    #Generates chorus with structure ABAB
    chorusA = generateMusicalSentence(models, 15, possiblePitches)
    chorusB = generateMusicalSentence(models, 15, possiblePitches)
    chorus = 2 * (chorusA + chorusB)
    
    '''
    print("chorusA is: {}".format(chorusA))
    print("chorusB is: {}".format(chorusB))
    print("chorus is: {}".format(chorus))
    '''

    
    bridge = generateMusicalSentence(models, 10, possiblePitches)
    outro = generateMusicalSentence(models, 10, possiblePitches)
  
    
    tuplesList = intro + verse + chorus + verse + chorus + bridge + chorus + outro
    pysynth.make_wav(tuplesList, fn = songName)
    #pysynth.make_wav(tuplesList, fn = "tuplesList.wav")
    
    '''
    pysynth.mix_files("pentatonicScale.wav", "tuplesList.wav", songName)
    # print("tuplesList: {}".format(tuplesList))
    #pysynth.make_wav(tuplesList, fn = songName)
    '''
    """

###############################################################################
# Reach
###############################################################################

PROMPT = """
(1) Generate song lyrics by The Beatles
(2) Generate a song using data from Nintendo Gamecube
(3) Quit the music generator
"""

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """
    # FIXME uncomment these lines when ready
    lyricsTrained = False
    musicTrained = False

    if len(sys.argv) == 2:
        if sys.argv[1] == "--test":
            print("TEST MODE")
            testLyricsModels = trainLyricModels(TESTLYRICSDIRS)
            trigram = testLyricsModels[0].nGramCounts
            bigram = testLyricsModels[1].nGramCounts
            unigram = testLyricsModels[2].nGramCounts
            output_models(unigram, output_fn = "unigram_student.txt")
            output_models(bigram, output_fn = "bigram_student.txt")
            output_models(trigram, output_fn = "trigram_student.txt")
            print('Student models have been written to the TEST_OUTPUT folder')

            print("Trying out that new shit")
            lyricsModels = trainLyricModels(TESTLYRICSDIRS)
            print("running runLyricsGenerator")
            runLyricsGenerator(lyricsModels)
            print("k its done")

            sys.exit()


    print('Welcome to the ' + TEAM + ' music generator!')
    while True:
        try:
            userInput = int(raw_input(PROMPT))
            if userInput == 1:
                # FIXME uncomment these lines when ready AND comment out "Under construction"
                if not lyricsTrained:
                    print('Starting lyrics generator and loading data...')
                    lyricsModels = trainLyricModels(LYRICSDIRS)
                    print('Data successfully loaded')
                    lyricsTrained = True

                runLyricsGenerator(lyricsModels)
        #print("Under construction")
            elif userInput == 2:
                # FIXME uncomment these lines when ready AND comment out "Under construction"
                if not musicTrained:
                    print('Starting music generator and loading data...')
                    musicModels = trainMusicModels(MUSICDIRS)
                    print('Data successfully loaded')
                    musicTrained = True

                songName = raw_input('What would you like to name your song? ')
                songNameBass = songName + "_Bass"
                songNameMelody = songName + "_Melody"
                runMusicGeneratorMelody(musicModels, WAVDIR + songNameMelody + '.wav')
                runMusicGeneratorBass(musicModels, WAVDIR + songNameBass + '.wav')
                pysynth.mix_files(WAVDIR + songNameMelody + '.wav', WAVDIR + songNameBass + '.wav', WAVDIR + songName + '.wav')
                
                #print("Under construction")
            elif userInput == 3:
                print('Thank you for using the ' + TEAM + ' music generator!')
                sys.exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number")

# This is how python tells if the file is being run as main
if __name__ == '__main__':
    main()
    #print("trainMusicModels output:\n{}".format(trainMusicModels(MUSICDIRS)))

# Test selectNGramModel
    test_models = [TrigramModel(), BigramModel(), UnigramModel()]
    test_sentence_unigram = ["^::^", "^:::^", "Hello", "$:::$"]
    test_sentence_bigram = ['^::^', '^:::^', "Hello", "World", "$:::$"]
    test_sentence_trigram = ['^::^', '^:::^', "Hello", "World", "extra", "$:::$"]
    testing_sentences = [test_sentence_unigram, test_sentence_bigram, test_sentence_trigram]
    for i in testing_sentences:
        print("testing sentence: {}\nOutput: {}".format(i, selectNGramModel(test_models, i)))
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!

