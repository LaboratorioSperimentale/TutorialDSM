"""
Set of utilities for Tutorial on Distributional Semantic Models
"""
  
import collections
import numpy as np
import scipy as sp

from sklearn.metrics.pairwise import cosine_similarity


def mk_reusable(fun):
    """
    Makes a reusable iterable out of generator by remembering its arguments
    """
    class MyIterable:
        def __init__(self, *args, **kwargs):
            self._args = args
            self._kwargs = kwargs

        def __iter__(self):
            yield from fun(*self._args, **self._kwargs)

    return MyIterable


@mk_reusable
def corpus_to_sentences(filename, token_shape=("form", "lemma", "pos")):
    """
    The function turns corpus into sentences containing only the required info.
    How do we choose how much info we want to keep? One of the parameters of the
    function controls that for us.
    Possible values for 'token_shape' are:
    "s_id", "form", "lemma", "pos", "pos_fgrained",
    "morph", "synhead", "synrel",
    "_", "_", "mwe", "mwe2"
    """

    with open(filename, encoding="utf-8") as fin:
        sentence = []

        for _, line in enumerate(fin):

            if not line.startswith("<"):
                line = line.strip()

                if len(line):

                    linesplit = line.split("\t")

                    CoNLL_columns = ["s_id", "form", "lemma",
                                     "pos", "pos_fgrained",
                                     "morph",
                                     "synhead", "synrel",
                                     "_", "_", "mwe", "mwe2"]
                    full_token = dict(zip(CoNLL_columns, linesplit))
                    token = tuple(full_token[col_name]
                                  for col_name in token_shape)

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


def compute_frequencies (filename, token_shape=["form", "lemma", "pos"]):

  freqDict = collections.defaultdict(int)

  for sentence in corpus_to_sentences(filename, token_shape):

    for token in sentence:
      freqDict[token] += 1

  sorted_freqs = sorted(freqDict.items(), key= lambda x: (-x[1], x[0]))
  return list(sorted_freqs)


def filter_by_POS(sorted_freqs, poslist, position=1):
    ret = []
    for token, freq in sorted_freqs:
        if token[position] in poslist:
            ret.append((token, freq))
    return ret

def filter_by_threshold(sorted_freqs, min_freq=0):
    ret = []
    for token, freq in sorted_freqs:
        if freq > min_freq:
            ret.append((token, freq))
    return ret

def load_from_file(filename, sep="\t"):

    ret = {}

    with open(filename) as fin:
        for line in fin:
            line = line.strip().split(sep)

            ret[tuple(line[:-1])] = float(line[-1])

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

    ret = sp.sparse.csr_matrix(
        (data, (rows, columns)), shape=(nrows, ncols), dtype=np.float32)
    return ret, targets_dict, contexts_dict


def cosine(vector_1, vector2):
    return cosine_similarity(vector_1, vector2)[0][0]
