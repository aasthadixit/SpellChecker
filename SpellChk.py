import nltk
from nltk.corpus import words, brown, wordnet

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def baselineCorrector(word):
    arr = sorted(words.words())
    if word in arr:
        return word
    low = 0
    high = len(arr) - 1
    while True:
        mid = (low + high) / 2
        midval = arr[mid]
        if high <= low:
            return arr[mid+1] if midval < word else midval
        if midval < word:
            low = mid + 1
        elif midval > word:
            high = mid - 1

def train(words):
    tagging_model = dict()
    training_model = dict()
    for word,tag in words:
        try:
            tagging_model[word].add(tag)
        except:
            tagging_model[word] = set([tag])
        try:
            training_model[word] += 1
        except:
            training_model[word] = 1
    return training_model, tagging_model

known_good_words = list(wordnet.words())
known_words, known_tagged_words = train(brown.tagged_words())

def edit_distance_one(word):
   set_of_words = set()
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]

   inserts    = set([a + c + b for a, b in splits for c in alphabet])
   set_of_words = set_of_words.union(inserts)

   deletes    = set([a + b[1:] for a, b in splits if b!=[]])
   set_of_words = set_of_words.union(deletes)

   trans      = set([a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1])
   set_of_words = set_of_words.union(trans)

   replaces   = set([a + c + b[1:] for a, b in splits for c in alphabet if b!=[]])
   set_of_words = set_of_words.union(replaces)

   return set_of_words

def edit_distance_two(word):
    candidates = []
    for first in edit_distance_one(word):
        for second in edit_distance_one(first):
            if second in known_words:
                candidates += [second]
    return set(candidates)

def known(words):
    return set([word for word in words if word in known_words])

def corrected_list(word_list):
    return sorted(list(word_list), key=known_words.get, reverse=True)

def correct_one(word):
    distance_one = corrected_list(known(edit_distance_one(word)))
    return distance_one

def correct(word):
    candidates = []
    first_list = corrected_list(known([word]))
    for lemma in first_list:
        if lemma not in candidates:
            candidates += [lemma]
    distance_one = corrected_list(known(edit_distance_one(word)))
    for lemma in distance_one:
        if lemma not in candidates:
            #if length of candidates is 20, keep replacing the minimum element.
            if(len(candidates) >= 20):
                a = min(candidates, key=known_words.get)
                if (known_words.get(lemma) > known_words.get(a)):
                    candidates.remove(a)
                    candidates += [lemma]
            else:
                candidates += [lemma]
    x = edit_distance_two(word)
    y = known(x)
    distance_two = corrected_list(y)
    for lemma in distance_two:
        if lemma not in candidates:
            candidates += [lemma]

    if word not in candidates:
        candidates += [word]
    return candidates

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
## can be done using pos_tag method
##
## Second approach
## Check the word sense max overlap using lesk algorithm

def simpleLesk(word, sentence):
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
    return max_overlap

def correct_sentence(sentence):
    ignored_tags = ['.',':','$',"''",'(',')',',','--']
    context = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(context)
    dictionary = dict()
    for i in xrange(len(context)):
        if context[i] in known_good_words:
            continue
        elif tags[i] in known_tagged_words[context[i]]:
            continue
        else:
            candidates = correct(context[i])
            if tags[i][1] in ignored_tags:
                continue
            if tags[i][1].find('NN') != -1:
                lesk_score = map(lambda x:simpleLesk(x,sentence), candidates)
                if(len(lesk_score) > 10):
                    cutoff = sorted(lesk_score, reverse=True)[10]
                    for j in xrange(len(candidates)):
                        if lesk_score[j] > cutoff:
                            try:
                                dictionary[context[i]] += [candidates[j]]
                            except:
                                dictionary[context[i]] = []
                else:
                    dictionary[context[i]] = candidates
            else:
                known_score = map(known_words.get, candidates)
                if(len(known_score) > 10):
                    cutoff = sorted(known_score, reverse=True)[10]
                    for j in xrange(len(candidates)):
                        if known_score[j] > cutoff:
                            try:
                                dictionary[context[i]] += [candidates[j]]
                            except:
                                dictionary[context[i]] = []
                else:
                    dictionary[context[i]] = candidates
    return dictionary, tags

def tagset_corpus(sentence):
    '''
        Needs some correction
    '''
    context = nltk.word_tokenize(sentence)
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
