import collections
import numpy as np
import scipy as sp

from sklearn.metrics.pairwise import cosine_similarity

def mk_reusable(f):
    """
    Makes a reusable iterable out of generator by remembering its arguments
    """

    class MyIterable:
        def __init__(self, *args, **kwargs):
            self._args = args
            self._kwargs = kwargs

        def __iter__(self):
            yield from f(*self._args, **self._kwargs)

    return MyIterable


def corpus_to_sentences(filename):
  
  with open(filename) as fin:
    sentence = []        
  
    for line_n, line in enumerate(fin):
    
      if not line.startswith("<"):     
        line = line.strip()

        if len(line):

          linesplit = line.split("\t")

          s_id, form, lemma, pos, *IGNORED = linesplit

          token = (form, lemma, pos) 
          
          sentence.append(token)

        else:                      
          yield sentence
          sentence = []
    
    yield sentence

@mk_reusable
def corpus_to_sentences_w2v(filename):
  
  with open(filename) as fin:
    sentence = []        
  
    for line_n, line in enumerate(fin):
    
      if not line.startswith("<"):     
        line = line.strip()

        if len(line):

          linesplit = line.split("\t")

          s_id, form, lemma, pos, *IGNORED = linesplit
          
          if not pos == "F":
            sentence.append(f"{lemma}/{pos}")

        else:                      
          yield sentence
          sentence = []
    
    yield sentence


def compute_frequencies (filename, accepted_pos=[]):
  
  freqDict = collections.defaultdict(int)

  for sentence in corpus_to_sentences(filename):

    for form, lemma, pos in sentence:
      if not len(accepted_pos) or pos in accepted_pos:
        freqDict[f"{lemma}/{pos}"] += 1
  
  sorted_freqs = sorted(freqDict.items(), key= lambda x: (-x[1], x[0]))
  return list(sorted_freqs)


def load_from_file(filename, sep="\t"):

  ret = {}

  with open(filename) as fin:
    for line in fin:
      line = line.strip().split(sep)

      ret[line[0]] = int(line[1])

  return ret



def load_sparse_matrix(filename, nrows, ncols, sep="\t"):
  
  rows = []
  columns = []
  data = []

  targets_dict = {}
  contexts_dict = {}

  

  with open(filename) as fin:
    for line in fin:
      linestrip = line.strip().split(sep)
      row_id, row_name, column_id, column_name, w = linestrip
      row_id, column_id = int(row_id), int(column_id)
      w = float(w)

      rows.append(row_id)
      columns.append(column_id)
      data.append(w)

      targets_dict[row_name] = row_id
      contexts_dict[column_name] = column_id

  ret = sp.sparse.csr_matrix((data, (rows, columns)), shape=(nrows, ncols), dtype=np.float32)
  return ret, targets_dict, contexts_dict


def cosine(vector_1, vector2):
  return cosine_similarity(vector_1, vector2)[0][0]