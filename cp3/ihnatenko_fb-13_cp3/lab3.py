alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

def btn(bigram, m):
    return alphabet.index(bigram[0]) * m + alphabet.index(bigram[1])

lookup = {btn((ax, bx), len(alphabet)):ax+bx for ax in alphabet for bx in alphabet}

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def solve(x, y, m):
    gcd, u = egcd(x, m)[:2]

    if gcd == 1:
        return [u * y % m]
    elif y % gcd != 0:
        return []
    x1, y1, m1 = x // gcd, y // gcd, m // gcd
    return [solve(x1, y1, m1)[0] + m1 * d for d in range(gcd)]

def count_bigram_fq(contents):
    bigram_fq_no_ovp = {}
    
    for i in range(len(contents) // 2):
        bigram_no_ovp = "".join((contents[i*2], contents[i*2 + 1]))

        if bigram_no_ovp in bigram_fq_no_ovp.keys():
            bigram_fq_no_ovp[bigram_no_ovp] += 1
        else:
            bigram_fq_no_ovp[bigram_no_ovp] = 1
    
    for bigram in bigram_fq_no_ovp.keys():
        bigram_fq_no_ovp[bigram] /= len(contents) // 2

    return bigram_fq_no_ovp

def count_letter_fq(contents):
    letter_fq = {}

    for letter in contents:
        if letter in letter_fq.keys():
            letter_fq[letter] += 1
        else:
            letter_fq[letter] = 1
    
    for letter in letter_fq.keys():
        letter_fq[letter] /= len(contents)

    return letter_fq

def aenc(sourcefile, destfile, key, m):
    src = open(sourcefile, encoding='utf8')

    pt = src.read().replace('\n', '')
    ct = ''

    src.close()

    for i in range(len(pt) // 2):
        x = btn((pt[i*2], pt[i*2 + 1]), m)
        y = (key[0]*x + key[1]) % m ** 2
        ct += lookup[y]
    
    dst = open(destfile, 'w+', encoding='utf8')
    dst.write(ct)
    dst.close()

def adec(sourcefile, destfile, key, m):
    src = open(sourcefile, encoding='utf8')
    
    ct = src.read().replace('\n', '')
    pt = ''

    src.close()

    for i in range(len(ct) // 2):
        y = btn((ct[i*2], ct[i*2 + 1]), m)
        x = solve(key[0], y - key[1], m ** 2)
        if len(x) == 0:
            src.close()
            return 0
        pt += lookup[x[0]]
    
    if isvalid(pt):
        dst = open(destfile, 'w+', encoding='utf8')
        dst.write(pt)
        dst.close()
        return 1

    return 0

badbg = [a+b for a in 'аеийоуьыэюя' for b in 'ьы']
fqlt = 'оаеи'
statlfq = count_letter_fq(open('stat.txt', encoding='utf8').read().replace('\n', ''))
statbfq = count_bigram_fq(open('stat.txt', encoding='utf8').read().replace('\n', ''))

def isvalid(txt):
    for bbg in [bg[0] for bg in sorted(count_bigram_fq(txt).items(), key = lambda x:x[1], reverse = True)]:
        if bbg in badbg:
            return 0

    ctlfq = count_letter_fq(txt)
    if abs(statlfq['о'] - ctlfq['о']) > 0.0152 or\
    abs(statlfq['а'] - ctlfq['а']) > 0.0309 or\
    abs(statlfq['е'] - ctlfq['е']) > 0.0199 or\
    abs(statlfq['и'] - ctlfq['и']) > 0.022:
        return 0

    return 1

def massdec(sourcefile, ptfq, ctfq, m):
    i = j = 0
    while i < len(ptfq)-1:
        j = min(j+1, len(ptfq)-1)
        k = l = 0
        while k < len(ctfq)-1:
            l = min(l+1, len(ctfq)-1)

            x1 = ptfq[i]
            x2 = ptfq[j]
            y1 = ctfq[k]
            y2 = ctfq[l]

            x = btn(x1, m) - btn(x2, m)
            y = btn(y1, m) - btn(y2, m)

            a = solve(x, y, m ** 2)
            if len(a) != 0:
                b = [(btn(y1, m) - ax * btn(x1, m)) % m ** 2 for ax in a]

                if adec(sourcefile, 'dec_{}_({}, {}).txt'.format(sourcefile[-6:-4], a[0], b[0]), (a[0], b[0]), m):
                    return a, b

            if l == len(ctfq)-1:
                l = k = k + 1
        if j == len(ptfq)-1:
            j = i = i + 1

def main():
    ct = open('05.txt', encoding='utf8').read().replace('\n', '')
    ctfq = [bg[0] for bg in sorted(count_bigram_fq(ct).items(), key = lambda x:x[1], reverse = True)]
    print('Найчастіші біграми шифротексту')
    print(ctfq[:5], '\n')

    pt =  open('stat.txt', encoding='utf8').read().replace('\n', '')
    ptfq = [bg[0] for bg in sorted(count_bigram_fq(pt).items(), key = lambda x:x[1], reverse = True)]
    print('Найчастіші біграми мови (на основі лаб1)')
    print(ptfq[:5], '\n')

    key = massdec('05.txt', ptfq[:5], ctfq[:5], len(alphabet))
    print('Ключі розшифрування')
    for i in range(len(key[0])):
        print('a = {}, b = {}\n'.format(key[0][i], key[1][i]))

if __name__ == '__main__':
    main()