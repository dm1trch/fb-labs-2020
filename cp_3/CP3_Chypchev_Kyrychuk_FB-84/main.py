#ЗАПУСТИ КОД

import os
from collections import Counter,OrderedDict
import itertools

cyrillic = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 
    'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
    'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 
    'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я'
]

class Text:
    def __init__(self,path):
        self.path = path

    def getcleartext(self):
        with open(self.path,'r',encoding='utf-8') as cryptofile:
            text = cryptofile.read().lower().rstrip().replace('ъ','ь').replace('ё','е').replace('\n','')
            #удаляем переносы строк
        return text

class Bigramms:
    def __init__(self,text):
        self.text = text
        self.bigramms_amount = 0
        self.bigramms_intersect_amount = 0
        self.bigramms = {}
        self.bi_no_intersect = {}


    def break_into_bigramms(self):
        n = 2
        bigramms_list = []
        for i in range(0,len(self.text),n):
            bigramms_list.append(self.text[i:i+n])
        self.bigramms_amount = len(bigramms_list)
        self.bigramms = OrderedDict(dict(Counter(bigramms_list)))

    def bigramms_no_intersect(self):
        n = 2
        bigramms_list = []
        for i in range(0,len(self.text),n):
            bigramms_list.append(self.text[i:i+n])
        self.bi_no_intersect = bigramms_list

    def frequency(self,dictionary,bigramms_amount):
        freq = {}
        for char in dictionary.items():
            freq[char[0]] = char[1]/bigramms_amount
            # print(
            #     char[0],
            #     '{:.12f}'.format(freq[char[0]])
            # )
        return freq

#возвращает нсд и обратное число в кольце по модулю
#а - число, b - модуль

class Reverse:
    def ensd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            nsd, x, y = self.ensd(b % a, a)
            return (nsd, y - (b//a) * x,x)

    def reverse(self, b, n):
        self.nsd, x, y = self.ensd(b, n)
        #print(g,x,y)
        if self.nsd == 1:
            return x % n
        
def find_a_key(lang1,lang2,bgrm1,bgrm2,alpha,m):
    x1 = cyrillic.index(lang1[0]) * m + cyrillic.index(lang1[1])
    x2 = cyrillic.index(lang2[0]) * m + cyrillic.index(lang2[1])   
    #популярные биграммы в шифротексте
    y1 = cyrillic.index(bgrm1[0]) * m + cyrillic.index(bgrm1[1])
    y2 = cyrillic.index(bgrm2[0]) * m + cyrillic.index(bgrm2[1])

    rev = Reverse()
    nsd = rev.ensd(abs(x1 - x2), m**2)
    solution = []
    if nsd[0] == 1:
        solution = rev.reverse(abs(x1-x2),m**2)
    elif nsd[0] > 1:
        a = abs(x1 - x2) // nsd[0]
        
        if a == 0:
            solution = None
        elif a > 0:
            a1 = (y1-y2) // nsd[0]
            a2 = (m**2) // nsd[0]
            a_reversed = rev.reverse(a,a2)
            res = 0
            #число, которое мы добавляем инкрементом
            incremented = a2
            while incremented <= m**2:
                res = (a_reversed + incremented) % (m**2)
                solution.append(res)
                incremented += a2

                
    final_a = []
    #когда одно решение
    if type(solution) == int:
        final_a.append(((y1-y2)*(solution)) % m**2)
    else:
        if solution != None:
            for sol in solution:
                final_a.append((a1*(sol))%m**2)
    return final_a

def find_b_key(l_bigram,ci_bigram,a,m,cyrillic):
    x = cyrillic.index(l_bigram[0]) * m + cyrillic.index(l_bigram[1])  
    y = cyrillic.index(ci_bigram[0]) * m + cyrillic.index(ci_bigram[1])  
    b = (x - y * a) % m**2
    return b

def correspondance_index(text):
    result = 0
    length = len(text)
    frequency = dict(Counter(text))
    for freq in frequency.values():
        result += freq * (freq - 1)
    return result / (length * (length - 1))  
    
#даём на вход биграмму, получаем число
def decrypt(a_reversed,b,bigramm,m,cyrillic):
    def num_to_bgrm(x):
        x1 = x // m
        x2 = x - x1 * m 
        return x1,x2
    decrypted_bigramm = ''
    y = cyrillic.index(bigramm[0]) * m + cyrillic.index(bigramm[1])
    x = (a_reversed * (y - b)) % m**2
    x1,x2 = num_to_bgrm(x)
    decrypted_bigramm = cyrillic[x1] + cyrillic[x2]
    return decrypted_bigramm

filename = 'lab3_var11.txt'
abs_path = os.path.dirname(__file__)
full_path = os.path.join(abs_path,filename)

ready_text = Text(full_path).getcleartext()

bigramms = Bigramms(ready_text)
bigramms.break_into_bigramms()
bigramms.bigramms_no_intersect()
frequency = bigramms.frequency(bigramms.bigramms,bigramms.bigramms_amount)
lang_popular_bigrams = ['ст','но','то','на','ен']
top = sorted(frequency.items(), key=lambda x:-x[1])[:5]
cipher_popular_bigrams = [i[0] for i in top]

# for sym in cyrillic:
#     sol = find_a_key('ст',f'н{sym}',top[0][0],top[1][0],cyrillic,31)
#     if sol != None:
#         print(sol)
a_result = []
b_result = []
l_double_combos = [i for i in itertools.permutations(lang_popular_bigrams,2)]
ci_double_combos = [i for i in itertools.permutations(cipher_popular_bigrams,2)]
for la_pair in l_double_combos:
    for ci_pair in ci_double_combos:
        a_result.append(find_a_key(la_pair[0],la_pair[1],ci_pair[0],ci_pair[1],cyrillic,31))

for lst in a_result:
    for a in lst:
        for la_bgrm in lang_popular_bigrams:
            for ci_bgrm in cipher_popular_bigrams:
                b_result.append(find_b_key(la_bgrm,ci_bgrm,a,31,cyrillic))

reverse = Reverse()
decrypted_texts = []
for lst in a_result:
    for a_key in list(set(lst)):
        for b_key in list(set(b_result)):
            text = ''
            for bigram in bigramms.bi_no_intersect:
                a_key_reversed = reverse.reverse(a,31)
                text += decrypt(a_key_reversed,b_key,bigram,31,cyrillic)
                #print(decrypt(a_key,b_key,bigram,31,cyrillic))
            index = correspondance_index(text)
            if index > 0.040:
                print(index,a_key,b_key)

