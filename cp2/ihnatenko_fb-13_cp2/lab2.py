alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def ctn(char): return alphabet.index(char)      # character to number

def ntc(num): return alphabet[num]              # number to character

def viz(src, dst, key, dec = False):
    srcfile = open(src, encoding='utf-8')
    dstfile = open(dst, 'w+', encoding='utf-8')
    srctext = srcfile.read()

    dsttext = ''
    for i in range(len(srctext)):
        dsttext += ntc(( ctn(srctext[i]) + (1 - 2*dec)*ctn(key[i % len(key)]) ) % len(alphabet))

    dstfile.write(dsttext)
    srcfile.close()
    dstfile.close()

def get_blocks(src, keylen):
    srcfile = open(src, encoding='utf-8')
    contents = srcfile.read()
    srcfile.close()

    blocks = ['' for _ in range(keylen)]
    for i in range(len(contents)):
        blocks[i%keylen] += contents[i]

    return blocks

def count_letters(block):
    letter_count = {letter:0 for letter in alphabet}

    for letter in block:
        letter_count[letter] += 1

    return letter_count

def count_index(block):
    return (sum(x * (x - 1) for x in count_letters(block).values())) / (len(block) * (len(block) - 1))


def main():
    outfiles = ['key2.txt', 'key3.txt', 'key4.txt', 'key5.txt', 'keylong.txt']
    keys = ['ио', 'осе', 'буер', 'зепар', 'рыбонуклеиновый']
    for i in range(5):
        viz('sample.txt', outfiles[i], keys[i])

    fulltext = open('fulltext.txt', encoding='utf-8')
    contents = fulltext.read()
    fulltext.close()
    lfq = count_letters(contents)
    for letter in lfq.keys(): lfq[letter] /= len(contents)

    mi = sum(x*x for x in lfq.values())
    print('Теоретичне значення індексу відповідності повного тексту: ', mi)

    sample = open('sample.txt', encoding='utf-8')
    contents = sample.read()
    sample.close()
    pri = count_index(contents)
    print('Практичне значення індексу відповідності зразка: ', pri)

    for i in range(5):
        ct = open(outfiles[i], encoding='utf-8')
        contents = ct.read()
        ct.close()
        print('Індекс відповідності шифротексту з ключем "{}": {}'.format(keys[i], count_index(contents)))
    
    print('\n')

    indices = {}
    for i in range(2, 31):
        blocks = get_blocks('ciphertext5.txt', i)
        index = sum(count_index(block) for block in blocks) / len(blocks)
        indices[i] = index
    
    print('Індекси відповідності шифротексту з припущенням довжини ключа\n')
    for item in indices.items():
        print(item)
    print('\n')
    
    for i in indices:
        if abs(mi - indices[i]) < abs(mi - pri)*3:
            print('Найімовірніша довжина ключа: ', i)
            keylen = i
            break

    blocks = get_blocks('ciphertext5.txt', keylen)
    possiblekey = [[] for _ in range(1, keylen + 1)]
    for i in range(keylen):
        lc = sorted(count_letters(blocks[i]).items(), key = lambda x:x[1], reverse = True)
        for _ in range(3):
            possiblekey[i].append( ntc((ctn(lc.pop(0)[0]) - ctn('о')) % len(alphabet)) )
    
    print('Варіанти найімовірніших літер для ключа\n')
    for i in range(len(possiblekey)):
        print(possiblekey[i])


if __name__ == '__main__':
    main()