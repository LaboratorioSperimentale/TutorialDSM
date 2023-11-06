"""
Set of utilities for Tutorial on Distributional Semantic Models
"""
  
import collections
import numpy as np
import scipy as sp
import math

from typing import Callable, Iterable, Generator, Tuple, Any, List, Set, Dict, Union


def mk_reusable(fun: Callable) -> Generator[Any, None, None]:
    """
    Makes a reusable iterable out of generator by remembering its arguments

    Args:
        fun (Callable): _description_

    Returns:
        Generator[Any, None, None]: _description_
        
    """
    class MyIterable:
        def __init__(self, *args, **kwargs):
            self._args = args
            self._kwargs = kwargs

        def __iter__(self):
            yield from fun(*self._args, **self._kwargs)

    return MyIterable


@mk_reusable
def corpus_to_sentences(filename: str, 
                        token_shape: Tuple[str, ...] = ("form", "lemma", "pos") 
                        ) -> Generator[Iterable, None, None]:
    """
    The function turns corpus into sentences containing only the required info.
    How do we choose how much info we want to keep? One of the parameters of the
    function controls that for us.

    Args:
        filename (str): path to file containing parsed corpus in CoNLL format
        token_shape (Tuple[str,...], optional):tuple containing the info that we want to retain for each token.
            Possible values for 'token_shape' are:
            "s_id", "form", "lemma", "pos", "pos_fgrained",
            "morph", "synhead", "synrel",
            "_", "_", "mwe", "mwe2" 
            Defaults to ("form", "lemma", "pos").

    Yields:
        Generator[Iterable, None, None]: Sentences containin tokens represented as token_shape
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
def corpus_to_sentences_w2v(filename: str, 
                            token_shape: Tuple[str, ...] = ("form", "lemma", "pos")
                            ) -> Generator[Iterable[str], None, None]:
    """
    The function turns corpus into sentences containing only the required info.
    
    Similar to "corpus_to_sentences", but tokens are represented as strings
    rather than tuples, in order to work as input for the gensim library


    Args:
        filename (str): path to file containing parsed corpus in CoNLL format
        token_shape (Tuple[str, ...], optional): tuple containing the info that we want to retain for each token.
            Possible values for 'token_shape' are:
            "s_id", "form", "lemma", "pos", "pos_fgrained",
            "morph", "synhead", "synrel",
            "_", "_", "mwe", "mwe2" 
            Defaults to ("form", "lemma", "pos").

    Yields:
        Generator[Iterable[str], None, None]: Sentences containin tokens represented as strings
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
                    
                    token_str = "/".join(token)
                    sentence.append(token_str)

                else:
                    yield sentence
                    sentence = []

        yield sentence


def compute_frequencies (filename: str, 
                         token_shape: Tuple[str, ...] = ("form", "lemma", "pos")
                         ) -> List[Tuple[Tuple[str,...], int]]:
    """
    Given a corpus, the function computes the list of frequencies of its token, sorted in decreasing order

    Args:
        filename (str): path to file containing parsed corpus in CoNLL format
        token_shape (Tuple[str, ...], optional): tuple containing the info that we want to retain for each token.
                                                Possible values for 'token_shape' are:
                                                "s_id", "form", "lemma", "pos", "pos_fgrained",
                                                "morph", "synhead", "synrel",
                                                "_", "_", "mwe", "mwe2" 
                                                Defaults to ("form", "lemma", "pos").

    Returns:
        List[Tuple[Tuple[str,...], int]]: List of sorted frequencies
    """

    freqDict = collections.defaultdict(int)

    for sentence in corpus_to_sentences(filename, token_shape):

        for token in sentence:
            freqDict[token] += 1

    sorted_freqs = sorted(freqDict.items(), key= lambda x: (-x[1], x[0]))
    
    return list(sorted_freqs)


def filter_by_POS(sorted_freqs: List[Tuple[Tuple[str,...], Any]], 
                  poslist: Union[List[str], Set[str], Dict[str, Any]], 
                  position: int = 1 
                  ) -> List[Tuple[Tuple[str,...], Any]]:
    """
    Filters list of tokens only keeping those with accepted Parts of Speech

    Args:
        sorted_freqs (List[Tuple[Tuple[str,...], Any]]): List of tokens in some representation format
        poslist (Union[List[str], Set[str], Dict[str, Any]]): List of accepted Parts of Speech
        position (int, optional): Offset of Part of Speech info in token representation. Defaults to 1.

    Returns:
        List[Tuple[Tuple[str,...], Any]]: Same list as sorted_freqs but filtered
    """
    
    ret = []
    for token, freq in sorted_freqs:
        if token[position] in poslist:
            ret.append((token, freq))
            
    return ret


def filter_by_threshold(sorted_freqs: List[Tuple[Tuple[str,...], int]], 
                        min_freq: int = 0
                        ) -> List[Tuple[Tuple[str,...], int]]:
    """
    Filters list of tokens by minimum frequency

    Args:
        sorted_freqs (List[Tuple[Tuple[str,...], int]]): List of tokens in some representation format with their frequency
        min_freq (int, optional): Frequency threshold used for filtering. Defaults to 0.

    Returns:
        List[Tuple[Tuple[str,...], int]]: Same list as sorted_freqs but filtered
    """
    
    ret = []
    for token, freq in sorted_freqs:
        if freq > min_freq:
            ret.append((token, freq))
    
    return ret


def load_from_file(filename: str, 
                   sep: str = "\t"
                   ) -> Dict[Tuple[str, ...], float]:
    """
    Load tokens from file with their frequencies

    Args:
        filename (str): path to file containing list of tokens
        sep (str, optional): separator used to parse file into tokens. Defaults to '\t'.

    Returns:
        Dict[Tuple[str, ...], float]: Dictionary with tokens as keys and frequencies as values
    """

    ret = {}

    with open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip().split(sep)

            ret[tuple(line[:-1])] = float(line[-1])

    return ret


def build_sparse_matrix(filename: str, 
                        token_shape: Tuple[str, ...], 
                        nrows: int, 
                        ncols: int, 
                        sep: str = "\t"
                        ) -> sp.sparse.spmatrix:
    """_summary_

    Args:
        filename (str): path to file containing matrix entries
        token_shape (Tuple[str, ...]): token representation used to load tokens from file
        nrows (int): number of rows
        ncols (int): number of columns
        sep (str, optional): separator used to parse file into tokens. Defaults to '\t'.

    Returns:
        sp.sparse.spmatrix: scipy sparse matrix in csr format
    """

    rows = []
    columns = []
    data = []

    targets_dict = {}
    contexts_dict = {}
    
    len_token_rep = len(token_shape)

    with open(filename, encoding="utf-8") as fin:
        for line in fin:
            linesplit = line.strip().split(sep)
            
            weight = float(linesplit[-1])
            
            row = linesplit[:len_token_rep+1]
            column = linesplit[len_token_rep+1:-1]
            
            row_id = int(row[0])
            column_id = int(column[0])
            
            row_token = tuple(row[1:])
            column_token = tuple(column[1:])          
            
            rows.append(row_id)
            columns.append(column_id)
            data.append(weight)

            targets_dict[row_token] = row_id
            contexts_dict[column_token] = column_id

    ret = sp.sparse.csr_matrix(
        (data, (rows, columns)), shape=(nrows, ncols), dtype=np.float32)
    return ret, targets_dict, contexts_dict


def write_to_file(filepath: str, 
                  matrix: Iterable[Iterable[Union[int, float]]], 
                  id_dict: Dict[Tuple[str, ...], int]
                  ) -> None:
    """
    Serialize vectors to file

    Args:
        filepath (str): path to location where file has to be created
        matrix (Iterable[Iterable[int  |  float]]): matrix (iterable of iterable)
        id_dict (Dict[Tuple[str, ...], int]): mapping from row id to token
    """
    
    sorted_dict = sorted(id_dict.items(), key=lambda x: x[1])
    
    with open(filepath, "w", encoding="utf-8") as fout:
        for row_id, row in enumerate(matrix):
            token_str = "\t".join(sorted_dict[row_id][0])
            vector_str = "\t".join(str(x) for x in row)
            print(f"{token_str}\t{vector_str}", file=fout)
            

def get_nearest_neighbors(matrix: Iterable[Iterable[Union[int, float]]], 
                          id_dict: Dict[Tuple[str, ...], int], 
                          topk: int = 10
                          ) -> Dict[Tuple[str, ...], List[Tuple[Tuple[str, ...], float]]]:
    """
    Get nearest neighbors from matrix containing cosine similarities

    Args:
        matrix (Iterable[Iterable[Union[int, float]]]): dense matrix containing cosine similarities
        id_dict (Dict[Tuple[str, ...], int]): mapping from row or column id to token
        topk (int, optional): Number of neighbors to return. Defaults to 10.

    Returns:
        Dict[Tuple[str, ...], List[Tuple[Tuple[str, ...], float]]]: Dictionary containing, for each token, its top neighbors and their cosine similarity
    """
    
    ret = {}
    sorted_dict = sorted(id_dict.items(), key=lambda x: x[1])
    sorted_dict = [x[0] for x in sorted_dict]
    
    for row_id, row in enumerate(matrix):

        row_with_labels = zip (row, sorted_dict)
        sorted_row = sorted(row_with_labels, reverse=True)
        
        ret[sorted_dict[row_id]] = sorted_row[:topk]
        
    return ret


def extract_cooccurrences(filepath: str, 
                          token_shape: Tuple[str, ...], 
                          targets: Union[Dict, Set, List], 
                          contexts: Union[Dict, Set, List], 
                          window_size: int = 5
                          ) -> Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]]:
    """_summary_

    Args:
        filepath (str): _description_
        token_shape (Tuple[str, ...]): _description_
        targets (Union[Dict, Set, List]): _description_
        contexts (Union[Dict, Set, List]): _description_
        window_size (int, optional): _description_. Defaults to 5.

    Returns:
        Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]]: _description_
    """

    co_occ = collections.defaultdict(lambda: collections.defaultdict(int))
    
    for sentence in corpus_to_sentences(filepath, token_shape):

        for token_id, token in enumerate(sentence):

            if token in targets:

                # build left and right window boundary
                # _ _ _ [_ _ _ _ _ X _ _ _ _ _] _ _ _
                left_boundary = max(0, token_id-window_size)
                right_boundary = min(len(sentence)-1, token_id+window_size)
                window = sentence[left_boundary:right_boundary+1]

                target_pos = token_id - left_boundary

                # check contexts in left window
                for ctx in window[0:target_pos]:
                    if ctx in contexts:
                        co_occ[token][ctx]+=1

                # check contexts in right window
                for ctx in window[target_pos+1:]:
                    if ctx in contexts:
                        co_occ[token][ctx]+=1
                
    return co_occ


def apply_ppmi(co_occurrences: Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]], 
               targets_frequencies_dict: Dict[Tuple[str, ...], int], 
               contexts_frequencies_dict: Dict[Tuple[str, ...], int], 
               corpus_size: int
               ) -> Dict[Tuple[str, ...], Dict[Tuple[str, ...], float]]:
    """_summary_

    Args:
        co_occurrences (Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]]): _description_
        targets_frequencies_dict (Dict[Tuple[str, ...], int]): _description_
        contexts_frequencies_dict (Dict[Tuple[str, ...], int]): _description_
        corpus_size (int): _description_

    Returns:
        Dict[Tuple[str, ...], Dict[Tuple[str, ...], float]]: _description_
    """

    weighted_coocc = collections.defaultdict(lambda: collections.defaultdict(int))

    for target in targets_frequencies_dict:
        target_frequency = targets_frequencies_dict[target]
        p_target = target_frequency/corpus_size

        for context in contexts_frequencies_dict:
            context_frequency = contexts_frequencies_dict[context]
            p_context = context_frequency/corpus_size

            coocc_frequency = co_occurrences[target][context]
            p_coocc = coocc_frequency/corpus_size

            if p_coocc > 0:
                pmi = math.log(p_coocc/(p_target*p_context), 2)
                weighted_coocc[target][context] = max(0, pmi)
        
    return weighted_coocc


def load_vectors(filename: str) -> Tuple[Dict[Tuple[str, str], int], np.ndarray]:
    
    matrix = []
    target_to_id = {}
    id_curr = 0
    
    with open(filename, encoding="utf-8") as fin:
        fin.readline()
        for line in fin:
            line = line.strip().split()
            lemma, pos = line[0].split("_")
            target_to_id[(lemma, pos)] = id_curr
            id_curr += 0
            matrix.append([float(x) for x in line [1:]])
    
    matrix = np.array(matrix)
    
    return target_to_id, matrix