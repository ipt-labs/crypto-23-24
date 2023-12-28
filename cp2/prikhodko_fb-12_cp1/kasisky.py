from math import gcd
MIN_SEQ_LEN = 7

def gcd_list(numbers):
    result = numbers[0]
    for number in numbers:
        result = gcd(result,number)
    return result

def kasiskyExamination(ct):
    seq_loc = {}
    for i in range(len(ct) - MIN_SEQ_LEN + 1):
        seq = ct[i:i+MIN_SEQ_LEN]
        if seq in seq_loc:
            seq_loc[seq].append(i)
        else:
            seq_loc[seq] = [i]
    
    seq_dist = {}
    for seq, loc in seq_loc.items():
        if len(loc) > 1:
            dist = [loc[i] - loc[i-1] for i in range(1,len(loc))]
            g = gcd_list(dist)
            if g in seq_dist:
                seq_dist[g].append(seq)
            else:
                seq_dist[g] = [seq]
    print(seq_dist)

    if seq_dist:
        key_length = gcd_list(list(seq_dist.keys()))
        return key_length
    else:
        print('Text is too small or estimated seq len is too large')
        return None

