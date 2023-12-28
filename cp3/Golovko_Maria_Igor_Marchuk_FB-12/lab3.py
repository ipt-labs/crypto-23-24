import math
input_file_path = 'D:\\uni year 3\\crypto labs\\crypto-23-24\\cp3\\igor_marchuk_maria_holovko_fb-12\\ciphertext_variant1.txt'
with open(input_file_path, 'r', encoding='UTF-8') as file:

    text = file.read()
def clean_text(text):

    text = ' '.join(text.split())
    text = text.lower()
    text = ''.join(char for char in text if (char.isalpha() and ord(char)>1071 and ord(char)<1106))
    return text
def decipher_bi(a,b,cipher_text=text):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    cipher_text=list(text)
    final_text=[]
    for i in range(0,int(len(text)),2):
        Y=get_Xi(convert_letter_to_number(cipher_text[i]),convert_letter_to_number(cipher_text[i+1]))
        X=(gcd(31*31,a)[1]*(Y-b))%(31*31)
        final_text.append(alphabet[X//31])
        final_text.append(alphabet[X%31])
    return ''.join(final_text)

def find_freq_without_overlap(formatted_text):
    letter_frequency = {}
    
    # Iterate through the text, taking every pair of non-overlapping letters
    for i in range(0, len(formatted_text) - 1, 2):
        pair = formatted_text[i:i+2]
        if len(pair) == 2:
            if pair in letter_frequency:
                letter_frequency[pair] += 1
            else:
                letter_frequency[pair] = 1
    return letter_frequency

def find_freq(formated_text):
    letter_frequency = {}
    for litera in formated_text:
        if litera in letter_frequency:
            letter_frequency[litera] += 1
        else:
            letter_frequency.update({litera: 1})
    return letter_frequency

def print_freq(let_freq,formated_text):
    print("загальна "," відсоток від ")
    print("кількість"," загального")
    for letter, frequency in sorted(let_freq.items(), key=lambda x:x[1], reverse=True):
        print(f"{letter}: {frequency},    %= {round(int(frequency)/(len(formated_text)/2)*100,3)}")
    return None
def get_top_five(let_freq,formated_text):
    top_5=[]
    i=0
    for letter, frequency in sorted(let_freq.items(), key=lambda x:x[1], reverse=True):
        top_5.append(letter)
        i=i+1
        if i==5:
            break
    return top_5
def convert_letter_to_number(letter):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    return alphabet.index(letter)
def get_Xi(a,b,m=31):
    return a*m+b
def top_5_to_Xi(pairs):
    result_list=[]
    for pair in pairs:
        pair=list(pair)
        result_list.append(get_Xi(convert_letter_to_number(pair[0]),convert_letter_to_number(pair[1])))
    return result_list
def gcd(a,b):
    dilene=a
    dilnik=b
    mnozhnik=[]
    ostatok=1

    u_0=0
    u_1=1
    while ostatok>0:
        mnozhnik=dilene//dilnik
        ostatok=dilene%dilnik
        #print("dilene",dilene,"dilnik",dilnik,"ostatok",ostatok,"mnozhnik",mnozhnik)
        dilene=dilnik
        gcd=dilnik
        dilnik=ostatok
        real_u=u_1
        temp=u_1
        u_1=u_0-mnozhnik*u_1
        u_0=temp
    if real_u<0:
        real_u=a+real_u
    if gcd!=1:
        real_u=None
    return gcd,real_u
# print(gcd(24,18))

def solve_expression(a,b,n):
    d=gcd(n,a)[0]
    if d==1:
        return (gcd(n,a)[1]*b)%n
    elif b%d!=0:
        # print("no solution")
        return None
    else:
        a_1=a/d
        b_1=b/d
        n_1=n/d
        result_list=[]
        x0=solve_expression(a_1,b_1,n_1)
        for i in range(0,d):
            result_list.append(x0+i*n_1)
        return result_list
def find_keys(top_5_plaintext_Xi,top_5_chiphered_Yi,X_astirisk,X_two_astirisk,Y_astirisk,Y_two_astirisk):
    X_true=top_5_plaintext_Xi[X_astirisk]-top_5_plaintext_Xi[X_two_astirisk]
    if X_true<0:
        X_true=31*31+X_true
    Y_true=top_5_chiphered_Yi[Y_astirisk]-top_5_chiphered_Yi[Y_two_astirisk]
    if Y_true<0:
        Y_true=31*31+Y_true
    a=solve_expression(X_true,Y_true,31*31)
    if a==None:
        return 999,999
    b=(top_5_chiphered_Yi[Y_astirisk]-a*top_5_plaintext_Xi[X_astirisk])%(31*31)
    
    return a,b
# print(solve_expression(328,20,96))

def get_combinations():
    from itertools import permutations
    list1 = [0, 1, 2, 3, 4]
    list2 = [0, 1, 2, 3, 4]
    all_combinations = []
    for perm1 in permutations(list1, 2):
        for perm2 in permutations(list2, 2):
            current_combination = list(perm1) + list(perm2)
            all_combinations.append(current_combination)
    return all_combinations
def entropy(original_text,letter_freq):
    entropy=float(0)
    for chastota in letter_freq.values():
        entropy+=(chastota/len(original_text))*math.log2(chastota/len(original_text))
    return -entropy 
text=clean_text(text)

# print_freq(find_freq_without_overlap(text),text)
top_5_chiphered=get_top_five(find_freq_without_overlap(text),text)
top_5_chiphered_Yi=top_5_to_Xi(top_5_chiphered)
top_5_plaintext_Xi=top_5_to_Xi(['ст','но','то','на','ен'])
# print(top_5_chiphered,"шифр текст",top_5_chiphered_Yi)
# print(['ст','но','то','на','ен'],"відкритий текст",top_5_plaintext_Xi)

all_combinations=get_combinations()
val_4_47_approx=1000
for x_0,x_1,y_0,y_1 in all_combinations:
    # print(top_5_plaintext_Xi[x_0],top_5_plaintext_Xi[x_1],top_5_chiphered_Yi[y_0],top_5_chiphered_Yi[y_1])
    a,b=find_keys(top_5_plaintext_Xi,top_5_chiphered_Yi,x_0,x_1,y_0,y_1)
    # print(a,b,decipher_bi(a,b)[:15])
    dec=decipher_bi(a,b)[:]
    entr=entropy(dec,find_freq(dec))
    temp=abs(4.471-entr)
    if temp<val_4_47_approx:
        val_4_47_approx=temp
        closest_a=a
        closest_b=b

print(decipher_bi(closest_a,closest_b)[:])
print(closest_a,closest_b)
    



