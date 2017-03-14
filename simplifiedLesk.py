import nltk
from nltk.corpus import wordnet

def simplifiedLesk(word, sentence):
    dictionary = {}
    senses = wordnet.synsets(word)
    best_sense = senses[0]
    max_overlap = 0
    i = 1
    for sense in senses:
        context = nltk.word_tokenize(sentence)
        print str(i)+'.',
        print sense.definition()
        signature = sense.definition().split()
        if(sense.examples() != []):
            print '\tExamples:'
        else:
            print '\tNo Examples present.'
        for x in sense.examples():
            print '\t\t'+x
            signature += x.split()
        overlap = set(signature).intersection(context)
        ##################################################
        ##  Area to print the tokens in a nice format.  ##
        ##################################################
        context = list(context)
        ## Any overlapping word will be seen in <word> format.
        for word in overlap:
            index = 0
            for words in signature:
                if words == word:
                    signature[index] = '<'+signature[index]+'>'
                index += 1
            index = 0
            for words in context:
                if words == word:
                    context[index] = '<'+context[index]+'>'
                index += 1
        ##################################################
        ##                Actual Printing               ##
        ##################################################
        print '\tWords in Gloss and Examples:'
        print '\t\t'+', '.join(list(signature))
        print '\tWords in Context:'
        print '\t\t'+', '.join(list(context))
        word = ' words' if len(overlap)!=1 else ' word'
        print '\t'+str(len(overlap))+word+' overlap found',
        if(len(overlap) != 0):
            if(len(overlap) == 1):
                x = 'which is'
            else:
                x = 'which are'
            print x,
            print "'"+"', '".join(overlap)+"'"
        ##################################################
        ##            End of formatting code            ##
        ##################################################
        if(len(overlap) > max_overlap):
            max_overlap = len(overlap)
            best_sense = sense
        i+=1;
        print ''
    return best_sense

sentence = 'The bank can guarantee deposits will eventually cover future tuition costs because it invests in adjustable-rate mortgage securities.'
word = 'bank'
x = simplifiedLesk(word,sentence)
print 'The best sense of the word bank is:'
print str(x)+": "+x.definition()
