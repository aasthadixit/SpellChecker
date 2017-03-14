import nltk
from nltk.corpus import wordnet as wn

##search for correct word
##finds the logical next in cases where the word is not found
def binary_search (arr, entered_word):
    low = 0
    high = len(arr) - 1
    while high >= low:
        mid = (low + high) // 2
        midval = arr[mid]
        if midval == entered_word:
            return mid
        elif high == low:
            if midval < entered_word:
                return mid + 1            
            else:
                return mid
        elif midval < entered_word:
            low = mid + 1
        elif midval > entered_word:
            high = mid - 1
                 
##main method that calls the binary_search method to find the next word
def baseline(entered_word):
    arr = sorted(nltk.corpus.words.words())
    mid = binary_search (arr, entered_word)
    return arr[mid]


    
