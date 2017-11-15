from __future__ import print_function
import sys
import os

from read_write import read_word_vectors
from ranking import *

if __name__=='__main__':  
  file_proportions = None
  
  if len(sys.argv) < 3:
      print ("Usage:",sys.argv[0],"<word vector files> <word similarity directory>")
      sys.exit(-1)
  elif len(sys.argv) > 3 and len(sys.argv[3]) > 0:
      file_proportions = [float(x) for x in sys.argv[3].split(",")]
  else:
      file_proportions = [1.0 for x in sys.argv[1].split(",")]
      
  word_vec_files = sys.argv[1]
  word_sim_dir = sys.argv[2] 
  
  word_vec_files = word_vec_files.split(",")

  words = dict()
  words_lc = dict()
  for i, filename in enumerate(os.listdir(word_sim_dir)):
    for line in open(os.path.join(word_sim_dir, filename),'r'):
      line = line.strip()
      [word1, word2, val] = line.split()
      words[word1] = None
      words[word2] = None
      words_lc[word1.lower()] = None
      words_lc[word2.lower()] = None

	
  word_vecs = dict()
  word_lc_vecs = dict()

  print("Reading",word_vec_files)
  read_word_vectors(word_vec_files, word_vecs, words, word_lc_vecs, words_lc, file_proportions)

  print ("Read",len(word_vecs),"vecs and",len(word_lc_vecs),"lc vecs")

  print ('=================================================================================')
  print ("%6s" %"Serial", "%20s" % "Dataset", "%50s" % "Num Pairs", "%15s" % "Not found", "%15s" % "Rho")
  print ('=================================================================================')

  for i, filename in enumerate(os.listdir(word_sim_dir)):
    manual_dict, auto_dict = ({}, {})
    not_found, total_size = (0, 0)
    for line in open(os.path.join(word_sim_dir, filename),'r'):
      line = line.strip()
      word1, word2, val = line.split()
      vec1 = vec2 = None
      if word1 in word_vecs:
          vec1 = word_vecs[word1]
      elif word1.lower() in word_lc_vecs:
          vec1 = word_lc_vecs[word1.lower()]

      if word2 in word_vecs:
          vec2 = word_vecs[word2]
      elif word2.lower() in word_lc_vecs:
          vec2 = word_lc_vecs[word2.lower()]
      
      if vec1 is not None and vec2 is not None:
          manual_dict[(word1, word2)] = float(val)
          auto_dict[(word1, word2)] = cosine_sim(vec1, vec2)
#	print word1,word_vecs[word1]
#	break
#	print word1,word2, manual_dict[(word1, word2)],auto_dict[(word1, word2)]
      else:
        not_found += 1
      total_size += 1    
    print ("%6s" % str(i+1), "%20s" % filename, "%50s" % str(total_size), "%15s" % str(not_found), "%15.4f" % spearmans_rho(assign_ranks(manual_dict), assign_ranks(auto_dict)))
