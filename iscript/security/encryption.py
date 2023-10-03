from cryptography.fernet import Fernet


def encryptfile(key, file_data):
    fernet = Fernet(key)
    return fernet.encrypt(file_data)


def decryptfile(key, file_data):
    fernet = Fernet(key)
    return fernet.decrypt(file_data)
