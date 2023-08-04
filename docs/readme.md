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
* **token_shape** (Tuple[str, ...]) : token representation used to load tokens from file
* **nrows** (int) : number of rows
* **ncols** (int) : number of columns
* **sep** (str, optional) : separator used to parse file into tokens. Defaults to '    '.


**Returns**

* **spmatrix**  : scipy sparse matrix in csr format


----


### write_to_file
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L301)
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
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L323)
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
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L353)
```python
.extract_cooccurrences(
   filepath: str, token_shape: Tuple[str, ...], targets: Union[Dict, Set, List],
   contexts: Union[Dict, Set, List], window_size: int = 5
)
```

---
_summary_


**Args**

* **filepath** (str) : _description_
* **token_shape** (Tuple[str, ...]) : _description_
* **targets** (Union[Dict, Set, List]) : _description_
* **contexts** (Union[Dict, Set, List]) : _description_
* **window_size** (int, optional) : _description_. Defaults to 5.


**Returns**

* _description_


----


### apply_ppmi
[source](https://github.com/LaboratorioSperimentale/TutorialDSM/blob/main/src/dsmagic.py/#L401)
```python
.apply_ppmi(
   co_occurrences: Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]],
   targets_frequencies_dict: Dict[Tuple[str, ...], int],
   contexts_frequencies_dict: Dict[Tuple[str, ...], int], corpus_size: int
)
```

---
_summary_


**Args**

* **co_occurrences** (Dict[Tuple[str, ...], Dict[Tuple[str, ...], int]]) : _description_
* **targets_frequencies_dict** (Dict[Tuple[str, ...], int]) : _description_
* **contexts_frequencies_dict** (Dict[Tuple[str, ...], int]) : _description_
* **corpus_size** (int) : _description_


**Returns**

* _description_

