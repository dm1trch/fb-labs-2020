import random
from math import gcd
from reverse import Reverse

def miller_rabin(p):
    if p == 2:
        return True
    elif p == 3:
        return True
    elif p % 2 == 0:
        return False
    else:
        s = 0
        d = p - 1
        while d % 2 == 0:
            d = d // 2
            s += 1

        for i in range(5):
            randprime = random.randrange(2, p - 1)
            x = pow(randprime, d, p)
            j = 0
            if x == 1:
                continue
            elif x == p - 1:
                continue
            while j < s - 1:
            #for j in range(s-1):
                x = pow(x, 2, p)
                if x == p - 1:
                    break
                j += 1
            else:
                return False
        return True

def primegenerator(size):
    a= open(r'C:\Users\funro\Desktop\univer\kripta\cryptolabs\fb-labs-2020\cp_4\miller_rabin.log','w+')
    while True:
        num = random.getrandbits(256)
        if miller_rabin(num):
            return num
        else:
            a.write(f'\n{num} not OK - this number failed Miller-Rabin test.')
            continue

def generatekeypairs(keysize):
    a_keys,b_keys = [],[]
    a_keys.append(primegenerator(keysize))
    a_keys.append(primegenerator(keysize))
    while True:
        b1,b2 = primegenerator(keysize),primegenerator(keysize)
        if b1 * b2 >= a_keys[0] * a_keys[1]:
            b_keys.append(b1)
            b_keys.append(b2)
            break
    return a_keys,b_keys

def findkeysets(p,q):
    n = p*q
    phi_n = (p-1)*(q-1)
    while True:
        e = random.randint(2,phi_n-1)
        if gcd(e,phi_n) == 1:
            break
    #n,e = findopenkeys(p,q,n,phi_n)
    d = Reverse().reverse(e,phi_n) 
    public_keys = [n,e]
    private_keys = [d,p,q]
    return public_keys,private_keys

def encrypt(n,e,M):
    return pow(M,e,n)

def decrypt(encrypted_message,d,n):
    return pow(encrypted_message,d,n)

def sign(d,decrypted_message,n):
    return pow(decrypted_message,d,n)

def verify(decrypted_message,signature,e,n):
    return pow(signature,e,n) == decrypted_message

def send_key(public_keys,public_keys1,private_keys,opentext):
    encrypted_message = encrypt(public_keys1[0],public_keys1[1],opentext)
    signature = sign(private_keys[0],random_opentext,public_keys[0])
    return encrypted_message,signature

def recieve_key(encrypted_message,signature,public_keys,public_keys1,private_keys1):
    verified = {}
    decrypted_message = decrypt(encrypted_message,private_keys1[0],public_keys1[0])
    if verify(decrypted_message,signature,public_keys[1],public_keys[0]):
        verified[signature] = decrypted_message
    return verified


keys = generatekeypairs(256)
p,q = keys[0][0],keys[0][1]
public_keys,private_keys = findkeysets(p,q)
p1,q1 = keys[1][0],keys[1][1]
public_keys1,private_keys1 = findkeysets(p1,q1)
random_opentext = random.randint(0,public_keys[0])
print(f'Open text: {random_opentext};')
ciphertext,signature = send_key(public_keys,public_keys1,private_keys,random_opentext)
print(f'Ciphertext text: {ciphertext};')
verified = recieve_key(ciphertext,signature,public_keys,public_keys1,private_keys1)
print(f'Decrypted text with verified signature: {verified};')
