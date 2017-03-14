## First approach
## training set
## calculate bigram of POS tags
## calculate probability of next tag
## calculate probability of previous tag
##
## test set
## find previous word POS tag
## find next word POS tag
## check which tag for current word has highest probability
## if tag is noun check for plurality
##
##
##
## Second approach
## Check the word sense max overlap using lesk algorithm
import nltk
from nltk.corpus import wordnet

def simplifiedLesk(word, sentence):
    '''
        Returns the max overlap with the gloss and examples.
    '''
    dictionary = {}
    senses = wordnet.synsets(word)
    best_sense = senses[0]
    max_overlap = 0
    i = 1
    for sense in senses:
        context = nltk.word_tokenize(sentence)
        signature = sense.definition().split()
        for x in sense.examples():
            signature += x.split()
        overlap = set(signature).intersection(context)
        context = list(context)
        if(len(overlap) > max_overlap):
            max_overlap = len(overlap)
            best_sense = sense
        i+=1;
        print ''
    return max_overlap
    
def tagset_corpus(sentence):
    sentence_new = sentence.replace(".","")
    context = nltk.word_tokenize(sentence_new)
    tags = nltk.pos_tag(context)
    bigram_tags = []
    final_tags = []
    count = []

    for i in range(0,len(context)-1):
        bigram_tags.append(tags[i][1] + tags[i+1][1])

    for j in range(0, len(bigram_tags)):
        flag = 'false'
        for k in range(0,len(final_tags)):
            if bigram_tags[j] == final_tags[k]:
                count[k] += 1
                flag = 'true'
        if flag == 'false':
            final_tags.append(bigram_tags[j])
            count.append(1)
            
    for m in range(0, len(final_tags)):
        count[m] = count[m] / len(bigram_tags)

    return final_tags, count

