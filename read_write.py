import sys
import gzip
import bz2
import numpy
import math

from collections import Counter
from operator import itemgetter

''' Read all the word vectors and normalize them '''
def read_word_vectors(filenames, word_vecs, words = None, lc_word_vecs = None, words_lc = None, file_proportions=None):
    if file_proportions is not None:
        word_weights = dict()
        lc_word_weights = dict()
    
    for i in range(len(filenames)):
        filename = filenames[i]
    
    if file_proportions is not None:
        file_proportion = file_proportions[i]
        
        if filename.endswith('.gz'): file_object = gzip.open(filename, 'r')
        elif filename.endswith('.bz2'): file_object = bz2.BZ2File(filename)
        else: file_object = open(filename, 'r')

        for line_num, line in enumerate(file_object):
            line = line.strip()
            e = line.split(" ", 1)
            word = e.pop(0)

            if words is None or word in words:
                if word not in word_vecs:
                    word_vecs[word] = []
                    
                    if file_proportions is not None:
                        word_weights[word] = []
                
                word_vecs[word].append(numpy.array([float(x) for x in e[0].split()]))

                if file_proportions is not None:
                    word_weights[word].append(file_proportion)
            elif (words_lc is not None and word.lower() in words_lc):
                lcw = word.lower()
                vec = [float(x) for x in e[0].split()]
                if lcw not in lc_word_vecs:
                    lc_word_vecs[lcw] = []
                    if file_proportions is not None:
                        lc_word_weights[lcw] = []

                lc_word_vecs[lcw].append(vec)

                if file_proportions is not None:
                    lc_word_weights[lcw].append(file_proportion)
        
        sys.stderr.write("Vectors read from: "+filename+" \n")
    
    for lcw in lc_word_vecs:
        if file_proportions is not None:
            sum_proportions = numpy.sum(lc_word_weights[lcw])
            v = numpy.dot(lc_word_weights[lcw], numpy.array(lc_word_vecs[lcw]))/sum_proportions
        # print lcw
        # for vv in lc_word_vecs[lcw]:
        #     print "\t",vv.shape
        else:
            v = numpy.array(lc_word_vecs[lcw]).mean(0)
        # print v.shape
        lc_word_vecs[lcw] = v

    for w in word_vecs:
        if file_proportions is not None:
            sum_proportions = numpy.sum(word_weights[w])
        # print w
        # for vv in lc_word_vecs[w]:
        #     print "\t",vv.shape
        
            v = numpy.dot(word_weights[w], numpy.array(word_vecs[w]))/sum_proportions
        else:
            v = numpy.array(word_vecs[w]).mean(0)
            
        # print v.shape
        word_vecs[w] = v

#    print 'computer',word_vecs['computer'][:10]
 #   sys.exit(-1)


#numpy.zeros(len(e), dtype=float)
#   for index, vec_val in enumerate(e):
#     word_vecs[word][index] = float(vec_val)      
#    print word,word_vecs[word]
#''' normalize weight vector '''
#    word_vecs[word] /= math.sqrt((word_vecs[word]**2).sum() + 1e-6)        
#    print word,word_vecs[word]
#    sys.exit(-1)

