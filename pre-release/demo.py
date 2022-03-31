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
file.write(str(encMessage))
file.close()
############################################################
#decrypting
file = open('message.ivf', 'r+')
message = file.read()
file.close()
file = open('passsalt.txt', 'r+')
salt = file.read()
file.close()
passwordnhash = str(password) + str(salt)
passwordnhash = passwordnhash.encode('utf-8')
hash = hashlib.sha256(passwordnhash).digest()
key = base64.urlsafe_b64encode(hash)
#fernet = Fernet(key)
decMessage = str(fernet.decrypt(bytes(message, 'utf-8')), 'utf-8')
print(decMessage)
