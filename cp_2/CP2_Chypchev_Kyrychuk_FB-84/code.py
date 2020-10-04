import re
from itertools import cycle
class Text:
    def __init__(self,textpath,keyspath):
        self.rusalpha = r'[^а-яА-Я|\s]+'
        self.ready_text = ''
        self.keys = []
        self.textpath = textpath
        self.keyspath = keyspath
    
    def getcleartext(self):
        textfile = open(self.textpath,'r',encoding='utf-8')
        self.ready_text = textfile.read().lower().rstrip().replace(' ', '')
        self.ready_text = re.sub(self.rusalpha,'',self.ready_text).replace('\n','')

    def getkeys(self):
        with open(self.keyspath,'r',encoding='utf-8') as keyfile:
            for key in keyfile:
                self.keys.append(key.replace('\n',''))
            


class Vigenere:
    def __init__(self,alpha,text,key):
        self.alpha = alpha
        self.text = text
        self.key = key

    def encrypt(self):
        def calculate(a,b):
            num = (self.alpha.index(a) + self.alpha.index(b)) % 33
            #print(num)
            return self.alpha[num]

        encrypted = ''
        for symb,k in zip(self.text,cycle(self.key)):
            encrypted += calculate(symb,k)
        return encrypted


cyrillic = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 
    'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 
    'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 
    'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
]

text = Text(r'C:\Users\funro\Desktop\univer\kripta\cryptolabs\fb-labs-2020\cp_2\CP2_Chypchev_Kyrychuk_FB-84\crypto.txt',
    r'C:\Users\funro\Desktop\univer\kripta\cryptolabs\fb-labs-2020\cp_2\CP2_Chypchev_Kyrychuk_FB-84\keys.txt')
text.getcleartext()
text.getkeys()
# a = open(r'C:\Users\funro\Desktop\univer\kripta\cryptolabs\fb-labs-2020\cp_2\CP2_Chypchev_Kyrychuk_FB-84\a.txt','w+')
# a.write(text.ready_text)
#шифруем первым ключом
vig = Vigenere(cyrillic,text.ready_text,text.keys[14])
print(vig.encrypt())