import collections

def read_WS353(filename):
    
    ret = {}
    
    with open(filename) as fin:
        for line in fin:
            line = line.strip().split()
            
            w1, w2, score = line
            score = float(score)
            
            ret[(w1, w2)] = score
            
    return ret

def read_SimLex999(filename):
    ret = {}
    
    with open(filename) as fin:
        fin.readline()
        for line in fin:
            line = line.strip().split()
            
            w1, w2, pos, score, *rest = line
            score = float(score)
            
            ret[((w1, pos), (w2, pos))] = score
            
    return ret


def read_MEN(filename):
    ret = {}
    with open(filename) as fin:
        for line in fin:
            line = line.strip().split()
            
            w1, w2, score = line
            w1, pos1 = w1.split("-")
            w2, pos2 = w2.split("-")
            score = float(score)
            
            ret[((w1, pos1), (w2, pos2))] = score
            
    return ret


def read_TOEFL(filename):
    ret = {}
    
    with open(filename) as fin:
        for line in fin:
            line = line.strip().split()
            
            _, w1, w2, score = line
            w1, pos1 = w1.rsplit("-", 1)
            w2, pos2 = w2.rsplit("-", 1)
            score = 1 if score == "TRUE" else 0
            
            ret[((w1, pos1), (w2, pos2))] = score
            
    return ret

def read_BLESS(filename):
    ret = {}
    
    with open(filename) as fin:
        for line in fin:
            line = line.strip().split()
            w1, w2, rel = line
            
            ret [(w1, w2)] = rel 
    
    return ret

def read_Pado(filename):
    
    ret = {}
    
    
    with open(filename) as fin:
        for line in fin:
            line = line.strip()
            
            if line:
                line = line.split()
                verb, arg, role, score = line
                score = float(score)
                
                ret[(verb, "v"), (arg, role)] = score

    return ret


def read_DTFit(filename):
    ret = {}
    with open(filename) as fin:
        for line in fin:
            line = line.strip().split()
            *all, typical, nsubj, root, obj = line
            
            typical = True if typical == "T" else False
            w_nsubj, role1 = nsubj.split(":")
            w_root, role2 = root.split(":")
            w_obj, role3 = obj.split(":")

            ret[((w_nsubj, role1), (w_root, role2), (w_obj, role3))] = typical

    return ret


def read_RELPRON(filename):
    ret = collections.defaultdict(list)
    
    with open(filename) as fin:
        for line in fin:
            line = line.strip().split()
            role, target, headN, _, w1, w2 = line
            target, posT = target[:-1].split("_")
            headN, posH = headN.split("_")
            w1, pos1 = w1.split("_")
            w2, pos2 = w2.split("_")

            ret[(target, posT, role)].append(((headN, posH),(w1, pos1),(w2, pos2)))

    return ret


if __name__ == "__main__":
    ret = read_RELPRON("../datasets/RELPRON/relpron.all")
    print(ret)