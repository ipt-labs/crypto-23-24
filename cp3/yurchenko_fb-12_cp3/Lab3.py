Alph = "абвгдежзийклмнопрстуфхцчшщьыэюя"
num_chars = {i: char for i, char in enumerate(Alph)}
chars = {char: i for i, char in enumerate(Alph)}
bg4ban = ['аь','аы','еь','еы','иь','иы','оь','оы','уь','уы','ьь','ьы','ыь','ыы','эь','эы','юь','юы','яь','яы','жы']

def count_bigr_freq(lst, step=1):
    string = ''.join(lst)
    bigr_freq = {}
    for i in range(0, len(lst)-1, step):
        bigr = string[i:i+2]
        if bigr in bigr_freq:
            bigr_freq[bigr] += 1
        else:
            bigr_freq[bigr] = 1
    return bigr_freq

def print_table(freq):
    hor = '-'*38
    print(hor)
    print("|  Символ  |  Кількість  |  Частота  |")
    print(hor)
    total = sum(freq.values())
    for char, val in sorted(freq.items(), key=lambda i: i[1], reverse=True):
        q = val/total
        print(f"|{char:^10}|{val:^13}| {q:.7f} |")
    print(hor)

def ext_gcd(a,b):
    if a==0: 
        return b,0,1
    gcd,x,y = ext_gcd(b%a, a) 
    x,y = y-(b//a)*x,x
    return gcd,x,y

def bg2num(text):
    bgs = [text[i:i+2] for i in range(0, len(text), 2)]
    bgs_num = []
    for bg in bgs:
        n1 = chars[bg[0]]
        n2 = chars[bg[1]]
        s = n1*31+n2
        bgs_num.append(s)
    return bgs_num

def bg_combs(bg,ct_bg):
    combs = []
    for x0 in bg:
        for y0 in ct_bg:
            remX = [x for x in bg if x!=x0]
            remY = [y for y in ct_bg if y!=y0]
            for x1 in remX:
                for y1 in remY:
                    comb = (x0, y0, x1, y1)
                    combs.append(comb)
    return combs

def find_keys(combs):
    poss_a = []
    poss_b = []
    for comb in combs:
        x0, y0, x1, y1 = comb[0],comb[1],comb[2],comb[3]
        gcd,x,y = ext_gcd(31**2,x0-x1)
        if gcd == 1:
            a = ((y0-y1)*y) % 31**2
            b = (y0-a*x0) % 31**2
            if a not in poss_a:
                poss_a.append(a)
                poss_b.append(b)
        if gcd > 1:
            if (y0-y1) % gcd != 0:
                pass
            if (y0-y1) % gcd == 0:
                a1 = x0-x1//gcd
                b1 = y0-y1//gcd
                n1 = 31**2//gcd
                gcd1, _, y = ext_gcd(n1, a1)
                x = (b1*y) % n1
                for i in range(int(gcd1)):
                    a = x+i*n1
                    b = (y1-a*x1) % 31**2
                    if a not in poss_a:
                        poss_a.append(a)
                        poss_b.append(b)
    return poss_a, poss_b

def decrypt(a,b,ct):
    decr_num = []
    for num in bg2num(ct):
        _, _, y = ext_gcd(31**2, a)

        new_num = (y*(num-b)) % 31**2
        decr_num.append(new_num)
    return decr_num

def num2bg(decr_num):
    bgs = []
    for n in decr_num:
        a = n//31
        b = n%31
        bg = num_chars[a]+num_chars[b]
        bgs.append(bg)
    return bgs

def check_text(bgs):
    for bg in bgs:
        if bg in bg4ban:
            return False
    return True


with open("10.txt", encoding="utf-8") as f:
    ct = f.read()

#print_table(count_bigr_freq(text,2))
mfbg_num = bg2num('стнотонаен')
ct_mfbg_num = bg2num('сгжэямнгтм')
a,b = find_keys(bg_combs(mfbg_num,ct_mfbg_num))
#print(f"Можливі a:{a}\n\nМожливі b:{b}\n")

for i in range(len(a)):
    aa,bb = a[i],b[i]
    decr_num = decrypt(aa,bb,ct)
    bgs = num2bg(decr_num)
    if check_text(bgs):
        pt = ''.join(bgs)
        print(f"a={aa}, b={bb}\nЧастина розшифрованого тексту:{pt[:150]}")
        with open("pt_v10.txt", "w", encoding="utf-8") as f:
            f.write(pt)
        break
