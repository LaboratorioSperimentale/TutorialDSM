"""
Set of utilities for loading datasets.
"""

import collections

from typing import Dict, Tuple, List, Any


def read_WS353(filename: str) -> Dict[Tuple[str, str], float]:
    """Load data for WordSimilarity-353.
    
    Data is expected in the following format:
        [LEXEME1]   [LEXEME2]   [SCORE]
        tiger	cat	7.35
        tiger	tiger	10.00
        plane	car	5.77
        train	car	6.31
        television	radio	6.77

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[str, str], float]: dataset dictionary
    """
    
    ret = {}
    
    with  open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip().split()
            
            w1, w2, score = line
            score = float(score)
            
            ret[(w1, w2)] = score
            
    return ret


def read_SimLex999(filename: str) -> Dict[Tuple[Tuple[str, str], Tuple[str, str]], float]:
    """Load data for SimLex-999.
    
    Data is expected in the following format:
        [LEXEME1]   [LEXEME2]   [PoS]   [SCORE] [...]
        old	new	A	1.58    ...
        smart	intelligent	A	9.2 ...
        hard	difficult	A	8.77    ...
        happy	cheerful	A	9.55    ...
        hard	easy	A	0.95    ...
        fast	rapid	A	8.75    ...

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[Tuple[str, str], Tuple[str, str]], float]: dataset dictionary
    """
    
    ret = {}
    
    with  open(filename, encoding="utf-8") as fin:
        fin.readline()
        for line in fin:
            line = line.strip().split()
            
            w1, w2, pos, score, *rest = line
            score = float(score)
            
            ret[((w1, pos), (w2, pos))] = score
            
    return ret


def read_MEN(filename: str) -> Dict[Tuple[Tuple[str, str], Tuple[str, str]], float]:
    """Load data for MEN.
    
    Data is expected in the following format:
        [LEXEME1-PoS]   [LEXEME2-PoS]   [SCORE]
        sun-n sunlight-n 50.000000
        automobile-n car-n 50.000000
        river-n water-n 49.000000
        stair-n staircase-n 49.000000
        morning-n sunrise-n 49.000000
    

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[Tuple[str, str], Tuple[str, str]], float]: dataset dictionary
    """
    
    ret = {}
    with  open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip().split()
            
            w1, w2, score = line
            w1, pos1 = w1.split("-")
            w2, pos2 = w2.split("-")
            score = float(score)
            
            ret[((w1, pos1), (w2, pos2))] = score
            
    return ret


def read_TOEFL(filename: str) -> Dict[Tuple[Tuple[str, str], Tuple[str, str]], int]:
    """Load data for TOEFL.
    
    Data is expected in the following format:
        [QuestionID]   [LEXEME1-PoS]   [LEXEME2-PoS]    [TRUE/FALSE]
        1	enormous-j	appropriate-j	FALSE
        1	enormous-j	unique-j	FALSE
        1	enormous-j	tremendous-j	TRUE
        1	enormous-j	decidedly-r	FALSE
        2	provision-n	stipulation-n	TRUE
        2	provision-n	interrelation-n	FALSE
        2	provision-n	jurisdiction-n	FALSE
        2	provision-n	interpretation-n	FALSE

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[Tuple[str, str], Tuple[str, str]], int]: dataset dictionary
    """
    ret = {}
    
    with  open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip().split()
            
            _, w1, w2, score = line
            w1, pos1 = w1.rsplit("-", 1)
            w2, pos2 = w2.rsplit("-", 1)
            score = 1 if score == "TRUE" else 0
            
            ret[((w1, pos1), (w2, pos2))] = score
            
    return ret


def read_BLESS(filename: str) -> Dict[Tuple[str, str], str]:
    """Load data for BLESS.
   
    Data is expected in the following format:
        [LEXEME1]   [LEXEME2]   [LABEL]
        alligator	aggressive	attri
        alligator	crocodile	coord
        alligator	chase	event
        alligator	carnivore	hyper
        alligator	mouth	mero    

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[str, str], str]: dataset dictionary
    """
    
    ret = {}
    
    with  open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip().split()
            w1, w2, rel = line
            
            ret [(w1, w2)] = rel 
    
    return ret


def read_Pado(filename: str) -> Dict[Tuple[Tuple[str, str], Tuple[str, str]], float]:
    """Load data for Pado-plausibility.

    Data is expected in the following format:
        [LEXEME1]   [LEXEME2]   [ARG0/ARG1] [SCORE]
        advise	banker	ARG0	6.0
        advise	banker	ARG1	5.0  
        advise	biologist	ARG0	4.2
        advise	biologist	ARG1	5.0      
        advise	business	ARG0	5.3
        advise	business	ARG1	5.8

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[Tuple[str, str], Tuple[str, str]], float]: dataset dictionary
    """
    
    ret = {}
    
    with  open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            
            if line:
                line = line.split()
                verb, arg, role, score = line
                score = float(score)
                
                ret[(verb, "v"), (arg, role)] = score

    return ret


def read_DTFit(filename: str) -> Dict[Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]], int]:
    """Load data for DTFit.
    
    Data is expected in the following format:
        [...]   [T/AT]  [LEXEME1:nsubj LEXEME2:root LEXEME3:obj]  
        ...	AT	actor:nsubj win:root battle:obj 
        ...	T	actor:nsubj win:root award:obj 
        ...	AT	anchorman:nsubj tell:root parable:obj 
        ...	T	anchorman:nsubj tell:root news:obj 
        ...	AT	animal:nsubj find:root map:obj 

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]], int]: dataset dictionary
    """
    
    ret = {}
    
    with  open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip().split()
            *all, typical, nsubj, root, obj = line
            
            typical = 1 if typical == "T" else 0
            w_nsubj, role1 = nsubj.split(":")
            w_root, role2 = root.split(":")
            w_obj, role3 = obj.split(":")

            ret[((w_nsubj, role1), (w_root, role2), (w_obj, role3))] = typical

    return ret


def read_RELPRON(filename: str) -> Dict[Tuple[str, str, str], List[Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]]]]:
    """Load data for RELPRON.
    
    Data is expected in the following format:
        [OBJ/SBJ]   [LEXEME1_PoS:]  [that]    [LEXEME2_PoS]  [LEXEME3_PoS]  
        OBJ garrison_N: organization_N that army_N install_V
        OBJ garrison_N: organization_N that fort_N house_V
        OBJ garrison_N: organization_N that barracks_N hold_V 
        SBJ garrison_N: organization_N that defend_V castle_N 
        SBJ garrison_N: organization_N that hold_V city_N  
    

    Args:
        filename (str): path to file

    Returns:
        Dict[Tuple[str, str, str], List[Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]]]]: dataset dictionary
    """
    
    ret = collections.defaultdict(list)
    
    with  open(filename, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip().split()
            role, target, headN, _, w1, w2 = line
            target, posT = target[:-1].split("_")
            headN, posH = headN.split("_")
            w1, pos1 = w1.split("_")
            w2, pos2 = w2.split("_")

            ret[(target, posT, role)].append(((headN, posH),(w1, pos1),(w2, pos2)))

    return ret


def pprint_dataset(dataset_dict: Dict[Any, Any], k: int = 5) -> None:
    """Prints dataset one entry per line.

    Args:
        dataset_dict (Dict[Any, Any]): Dataset dictionary
        k (int, optional): Number of elements to print. Defaults to 5.
    """
    
    keys = list(dataset_dict.keys())[:k]
    
    for k in keys:
        print(k, "\t", dataset_dict[k])
