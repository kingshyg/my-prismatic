
import sys
import re
import simplejson

from nltk.corpus import stopwords
from nltk.util import ngrams

def get_ngrams(title):

    # remove 's
    title = title.replace("'s", "")

    # remove punctuation and odd characters
    title = re.sub('([^a-zA-Z0-9\'\-_\s])','', title)

    # break up words by space and remove stopwords
    words = filter(lambda x: x not in stopwords.words(), title.split())

    # let's get bigrams
    bigrams = ngrams(words, n=2)
    for word in bigrams:
        words.append(' '.join(v for v in word))

    return words

def train(titles):
    word_weights = {}

    for title in titles:
        words = get_ngrams(title)

        # count unigrams
        for word in words:
            if len(word) == 1 and word != 'r' and word != 'c':
                continue

            word_weights.setdefault(word, 0)
            word_weights[word] += 1


    return filter(lambda y: y[1] > 1,
        sorted(word_weights.items(), key=lambda x:x[1]))

def predict(titles, weights):
    results = []
    for title in titles:
        words = get_ngrams(title)

        # let's score stuff
        tot_wt = sum(weights[w] for w in words if w in weights)
        results.append((title, tot_wt))

    return sorted(results, key=lambda x:x[1], reverse=True)

def main():

    if len(sys.argv) != 4:
        print "\nUsage:python learn.py <task> <datafile> <weights_file>"
        print "task: train/predict\n"
        return

    task = sys.argv[1]

    # get data, prismatic titles
    filename = sys.argv[2]
    titles = open(filename).read().lower().split('\n')

    if task == 'train':
        weights_file = sys.argv[3]
        weights = train(titles)
        if weights:
            print weights
            open(weights_file, 'w').write(simplejson.dumps(weights))

    elif task == 'predict':
        weights_file = sys.argv[3]
        data = simplejson.loads(open(weights_file, 'r').read())
        # convert into dict for easy reference
        weights = {}
        for val in data:
            weights[val[0]] = val[1]

        results = predict(titles, weights)
        for value in results:
            print value[1], value[0]

    else:
        print "Invalid task!!"
        


if __name__ == "__main__":
    main()
