import hashlib
import bcrypt
from cryptography.fernet import Fernet
import base64

#encrypting
############################################################
file = open('message.txt', 'r+')
message = file.read()
file.close()
password = input("Enter password: ")
file = open('passsalt.txt', 'r+')
salt = file.read()
file.close()
passwordnhash = str(password) + str(salt)
passwordnhash = passwordnhash.encode('utf-8')
hash = hashlib.sha256(passwordnhash).digest()
key = base64.urlsafe_b64encode(hash)
fernet = Fernet(key)
encMessage = fernet.encrypt(message.encode())
file = open('message.ivf', 'w+')
encMessage = encMessage.decode('utf-8')
file.write(str(encMessage))
file.close()
############################################################
#decrypting
file = open('message.ivf', 'r+')
token = file.read()
file.close()
print(token)
token = token.encode('utf-8')
file = open('passsalt.txt', 'r+')
salt = file.read()
file.close()
passwordnhash = str(password) + str(salt)
passwordnhash = passwordnhash.encode('utf-8')
hash = hashlib.sha256(passwordnhash).digest()
key = base64.urlsafe_b64encode(hash)
fernet = Fernet(key)



#token = fernet.encrypt(message)
d = fernet.decrypt(token)
d = d.decode('utf-8')
print(d)
