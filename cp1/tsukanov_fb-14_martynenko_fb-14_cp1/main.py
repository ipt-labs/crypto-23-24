import math
no_target_symb='\n '

file_name = "res1.txt"

def counf_symb():
    with open(file_name, "r", encoding="cp1251") as f:
        count = 0
        while True:
            c = f.read(1).lower()
            if not c:
                break
            if c not in no_target_symb:
                count += 1
    return count
    

def count_c1():
    c1 = dict()
    with open(file_name, "r", encoding="cp1251") as f:
        while True:
            c = f.read(1).lower()
            if not c:
                break
            if c not in no_target_symb:
                if c not in c1.keys():
                    c1[c] = 0
                c1[c] += 1
    return c1
      

def count_c2():
    c2 = dict()
    with open(file_name, "r", encoding="cp1251") as f:
        a = f.read(1).lower()
        while True:
            b = f.read(1).lower()
            if not b:
                break
            if b not in no_target_symb:
                if a+b not in c2.keys():
                    c2[a+b] = 0
                c2[a+b] += 1
                a = b
    return c2
      
def count_h(p):
    res = 0
    for i in p.keys():
        res += p[i] * math.log2(p[i])
    return -res


count_of_symbols = counf_symb()
c1 = count_c1()
c2 = count_c2()
p1 = dict()
p2 = dict()

for i in c1.keys():
    p1[i] = c1[i] / count_of_symbols

for i in c2.keys():
    p2[i] = c2[i] / count_of_symbols

h1 = count_h(p1) / 1
h2 = count_h(p2) / 2

print("************h1************")
print(h1)
print("\n************h2************")
print(h2)
print(p1)
