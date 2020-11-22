import json
import requests
from requests import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

keysize = 256
response = requests.get(f'http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize={keysize}').text
response = json.loads(response)
n1 = int(response['modulus'],16)
e1 = int(response['publicExponent'],16)
#print(n1,e1)
response_encrypt = requests.get('http://asymcryptwebservice.appspot.com/rsa/encrypt',params={'modulus':n1,'publicExponent':e1, 'message':'12345678','type':'TEXT'}).text
ciphertext = int(json.loads(response_encrypt)['cipherText'],16)

