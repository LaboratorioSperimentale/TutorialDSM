#


### corpus_to_sentences
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L36)
```python
.corpus_to_sentences(
   filename: str, token_shape: Tuple[str, ...] = ('form', 'lemma', 'pos')
)
```

---
The function turns corpus into sentences containing only the required info.
How do we choose how much info we want to keep? One of the parameters of the
function controls that for us.


**Args**

* **filename** (str) : path to file containing parsed corpus in CoNLL format
token_shape (Tuple[str,...], optional):tuple containing the info that we want to retain for each token.
    Possible values for 'token_shape' are:
    "s_id", "form", "lemma", "pos", "pos_fgrained",
    "morph", "synhead", "synrel",
    "_", "_", "mwe", "mwe2" 
    Defaults to ("form", "lemma", "pos").


**Yields**

* Sentences containin tokens represented as token_shape


----


### corpus_to_sentences_w2v
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L90)
```python
.corpus_to_sentences_w2v(
   filename: str, token_shape: Tuple[str, ...] = ('form', 'lemma', 'pos')
)
```

---
The function turns corpus into sentences containing only the required info.

Similar to "corpus_to_sentences", but tokens are represented as strings
rather than tuples, in order to work as input for the gensim library



**Args**

* **filename** (str) : path to file containing parsed corpus in CoNLL format
* **token_shape** (Tuple[str, ...], optional) : tuple containing the info that we want to retain for each token.
    Possible values for 'token_shape' are:
    "s_id", "form", "lemma", "pos", "pos_fgrained",
    "morph", "synhead", "synrel",
    "_", "_", "mwe", "mwe2" 
    Defaults to ("form", "lemma", "pos").


**Yields**

* Sentences containin tokens represented as strings


----


### compute_frequencies
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L144)
```python
.compute_frequencies(
   filename: str, token_shape: Tuple[str, ...] = ('form', 'lemma', 'pos')
)
```

---
Given a corpus, the function computes the list of frequencies of its token, sorted in decreasing order


**Args**

* **filename** (str) : path to file containing parsed corpus in CoNLL format
* **token_shape** (Tuple[str, ...], optional) : tuple containing the info that we want to retain for each token.
                                        Possible values for 'token_shape' are:
                                        "s_id", "form", "lemma", "pos", "pos_fgrained",
                                        "morph", "synhead", "synrel",
                                        "_", "_", "mwe", "mwe2" 
                                        Defaults to ("form", "lemma", "pos").


**Returns**

* List of sorted frequencies


----


### filter_by_POS
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L175)
```python
.filter_by_POS(
   sorted_freqs: List[Tuple[Tuple[str, ...], Any]], poslist: Union[List[str],
   Set[str], Dict[str, Any]], position: int = 1
)
```

---
Filters list of tokens only keeping those with accepted Parts of Speech


**Args**

* **sorted_freqs** (List[Tuple[Tuple[str,...], Any]]) : List of tokens in some representation format
* **poslist** (Union[List[str], Set[str], Dict[str, Any]]) : List of accepted Parts of Speech
* **position** (int, optional) : Offset of Part of Speech info in token representation. Defaults to 1.


**Returns**

* Same list as sorted_freqs but filtered


----


### filter_by_threshold
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L199)
```python
.filter_by_threshold(
   sorted_freqs: List[Tuple[Tuple[str, ...], int]], min_freq: int = 0
)
```

---
Filters list of tokens by minimum frequency


**Args**

* **sorted_freqs** (List[Tuple[Tuple[str,...], int]]) : List of tokens in some representation format with their frequency
* **min_freq** (int, optional) : Frequency threshold used for filtering. Defaults to 0.


**Returns**

* Same list as sorted_freqs but filtered


----


### load_from_file
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L221)
```python
.load_from_file(
   filename: str, sep: str = '\t'
)
```

---
Load tokens from file with their frequencies


**Args**

* **filename** (str) : path to file containing list of tokens
* **sep** (str, optional) : separator used to parse file into tokens. Defaults to '    '.


**Returns**

* Dictionary with tokens as keys and frequencies as values


----


### build_sparse_matrix
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L246)
```python
.build_sparse_matrix(
   filename: str, token_shape: Tuple[str, ...], nrows: int, ncols: int,
   sep: str = '\t'
)
```

---
_summary_


**Args**

* **filename** (str) : path to file containing matrix entries
* **token_shape** (Tuple[str, ...]) : tuple containing the info that we want to retain for each token.
    Possible values for 'token_shape' are:
    "s_id", "form", "lemma", "pos", "pos_fgrained",
    "morph", "synhead", "synrel",
    "_", "_", "mwe", "mwe2" 
* **nrows** (int) : number of rows
* **ncols** (int) : number of columns
* **sep** (str, optional) : separator used to parse file into tokens. Defaults to '    '.


**Returns**

* **spmatrix**  : scipy sparse matrix in csr format


----


### write_to_file
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L305)
```python
.write_to_file(
   filepath: str, matrix: Iterable[Iterable[Union[int, float]]],
   id_dict: Dict[Tuple[str, ...], int]
)
```

---
Serialize vectors to file


**Args**

* **filepath** (str) : path to location where file has to be created
* **matrix** (Iterable[Iterable[int  |  float]]) : matrix (iterable of iterable)
* **id_dict** (Dict[Tuple[str, ...], int]) : mapping from row id to token


----


### get_nearest_neighbors
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L327)
```python
.get_nearest_neighbors(
   matrix: Iterable[Iterable[Union[int, float]]], id_dict: Dict[Tuple[str, ...],
   int], topk: int = 10
)
```

---
Get nearest neighbors from matrix containing cosine similarities


**Args**

* **matrix** (Iterable[Iterable[Union[int, float]]]) : dense matrix containing cosine similarities
* **id_dict** (Dict[Tuple[str, ...], int]) : mapping from row or column id to token
* **topk** (int, optional) : Number of neighbors to return. Defaults to 10.


**Returns**

* Dictionary containing, for each token, its top neighbors and their cosine similarity


----


### extract_cooccurrences
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L357)
```python
.extract_cooccurrences(
   filepath: str, token_shape: Tuple[str, ...], targets: Union[Dict, Set, List],
   contexts: Union[Dict, Set, List], window_size: int = 5
)
```

---
Extracts co-occurrences between given targets and contexts (given as parameters)


**Args**

* **filepath** (str) : path to file containing data (i.e., corpora)
* **token_shape** (Tuple[str, ...]) : tuple containing the info that we want to retain for each token.
    Possible values for 'token_shape' are:
    "s_id", "form", "lemma", "pos", "pos_fgrained",
    "morph", "synhead", "synrel",
    "_", "_", "mwe", "mwe2"
* **targets** (Union[Dict, Set, List]) : data structure containing list of lexemes to be considered as targets
* **contexts** (Union[Dict, Set, List]) : data structure containing list of lexemes to be considered as contexts
* **window_size** (int, optional) : size of context to be considered. 
    Note, the window is considered both to the left and to the right of the target.
    Defaults to 5.


**Returns**

* Dictionary of co-occurrences


----


### apply_ppmi
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L411)
```python
.apply_ppmi(
   co_occurrences: Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]],
   targets_frequencies_dict: Dict[Tuple[str, ...], int],
   contexts_frequencies_dict: Dict[Tuple[str, ...], int], corpus_size: int
)
```

---
Apply PPMI (Positive Pointwise Mutual Information) to a dictionary registering co-occurrences.


**Args**

* **co_occurrences** (Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]]) : Dictionary of co-occurrences
* **targets_frequencies_dict** (Dict[Tuple[str, ...], int]) : Dictionary of frequencies for target items
* **contexts_frequencies_dict** (Dict[Tuple[str, ...], int]) : Dictionary of frequencies for context items
* **corpus_size** (int) : Overall size of corpus.


**Returns**

* Weighted matrix.


----


### load_vectors
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L448)
```python
.load_vectors(
   filename: str
)
```

---
Load vectors from file.

The file is expected to be formatted with one vector per line (the first line contains the overall dimension of the matrix), as follows:
163473 300
say_VERB -0.008861 0.097097 0.100236 0.070044 -0.079279 0.000923 -0.012829 0.064301 ...
go_VERB 0.010490 0.094733 0.143699 0.040344 -0.103710 -0.000016 -0.014351 0.019653 ...
make_VERB -0.013029 0.038892 0.008581 0.056925 -0.100181 0.011566 -0.072478 0.156239 ...


**Args**

* **filename** (str) : path to txt file containing vectors.


**Returns**

* Dictionary containing with lexemes as indexes and vectors as values.

