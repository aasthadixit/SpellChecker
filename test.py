import SpellChk
from SpellChk import correct_one, correct, correct_sentence, baselineCorrector

correct_word = open('correct_small.dat')
wordfile = open('missp_small.dat')
count_base = 0
count_new = 0
correct_words = []
for word in correct_word.readlines():
    w = str(word.strip())
    correct_words += [w]
index = 0
for word in wordfile.readlines():
    w = str(word.strip())
    if(correct_words[index] == baselineCorrector(w)):
        count_base += 1
    if(correct_words[index] == correct(w)[0]):
        count_new += 1
    print count_base, count_new
    index+=1
print count_base, count_new
wordfile.close()
