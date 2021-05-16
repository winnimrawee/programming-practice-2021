
##############################################      LIBRARY FILE     ##################################################################

import re
import string

def filter_word(sentence):    # Filter out punctuations, such as ',' '?' '!'
    global word_filtered
    word_filtered = []
    sentence_split = sentence.split(" ")
    for word in sentence_split:
        if word[-1] == "." or word[-1] == "?" or word[-1] == "!":
            word = word.replace(word[-1], "")
            word_filtered.append(word)
        else: 
            word_filtered.append(word)
    return word_filtered


def split_and_arrange(sentence):      # Cut out words with 1 letter and arrange besed on second letter
    filter_word(sentence)

    words_2_or_more_letters = []
    for i in word_filtered:
        if len(i) > 1:
            words_2_or_more_letters.append(i)        
    words_2_or_more_letters.sort(key = lambda c : c[1])
    print(words_2_or_more_letters)



def get_total_words(sentence):        # Print total words
    filter_word(sentence)
    print("The amount of words is: ",len(word_filtered))


def get_total_sentences(sentence):
    sentences = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", sentence)
    print("The amount of sentences is: ",len(sentences))




vowels = ['a','e','i','o','u']

def less_than_5(sentence): 
    filter_word(sentence)
    words_5letters = []
    for n in word_filtered:
        if len(n) < 5:
            words_5letters.append(n)
    print("The words with less than 5 letters are:", ', '.join(words_5letters))
        

def less_than_5_no_vowels(sentence):
    filter_word(sentence)
    words_no_vowels = []
    for n in word_filtered:
        x = n
        for letter in n:
            if letter in vowels:
                x = x.replace(letter, "")
        words_no_vowels.append(x)
        
    words_5letters_no_vowels = []
    for x,y in zip(word_filtered, words_no_vowels):
        if len(y) < 5:
            words_5letters_no_vowels.append(x)
    print("The words with less than 5 letters excluding vowels are:", ', '.join(words_5letters_no_vowels))


        
##############################################      MAIN FILE      ##################################################################

import exercise_3 as lib
import pickle as p

while True:
    global previous_input
    sentence = input("Please type in a sentence (Type stop to exit program): ")
    if sentence == "previous":
        try:
            previous_input = p.load(open('exercise_4_previous_input','rb'))
            print(previous_input)
        except:
            print("There is no previous input")
    elif sentence == 'stop':
        print('Program closed')
        break
    else:
        p.dump(sentence, open('exercise_4_previous_input','wb'))
        lib.split_and_arrange(sentence)
        lib.get_total_words(sentence)
        lib.get_total_sentences(sentence)
        lib.less_than_5(sentence)
        lib.less_than_5_no_vowels(sentence)

