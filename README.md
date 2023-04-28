# IncVault
IncVault is a command line program that provides encrypted file storage on Windows. It creates a "locker" folder that securely stores your files.

## Features

- [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption using the [Fernet](https://cryptography.io/en/latest/fernet/) algorithm to encrypt your files
- Automatically decrypts files when you want to access them
- Provides a secure encrypted vault for storing sensitive files on Windows

## Security

IncVault uses the [Fernet](https://cryptography.io/en/latest/fernet/) symmetric encryption, [Argon2](https://www.argon2.com/) and [Hashlib](https://docs.python.org/3/library/hashlib.html)

### [Fernet](https://cryptography.io/en/latest/fernet/)

IncVault uses the Fernet symmetric encryption algorithm to encrypt your files. All files added to the locker folder are automatically encrypted.

Fernet is a symmetric encryption algorithm that uses the AES algorithm in CBC mode with a 128-bit key for encryption and PKCS7 padding. The Fernet algorithm is provided by the Python cryptography library.

### [Hashing](https://en.wikipedia.org/wiki/Hash_function)

Passwords and keys are first hashed using the Argon2 algorithm, which is designed to be resistant to both GPU and ASIC attacks. Then, the output of Argon2 is hashed again using the hashlib library, providing an additional layer of security to the already-hashed password.

Hashing is a one-way function that takes an input data and generates a fixed-size output value, which is unique to the input data.

### Issues

Please note that you should only interact with files stored in your locker through IncVault, unless you are editing the file contents. If an Antivirus causes any issues, you may have to [create an exception](https://www.google.com/search?q=how+to+create+an+exception+in+%5Bantivirus%5D&sxsrf=APwXEdck3w8dJJN2pkH660RpQNwrCi0nNQ%3A1682017158274&source=hp&ei=hotBZIDyDJOR8gLKsYOQCw&iflsig=AOEireoAAAAAZEGZltTE6sDECenhHxi9NiJeOVL1udK-&ved=0ahUKEwiAzeKZkrn-AhWTiFwKHcrYALIQ4dUDCAo&uact=5&oq=how+to+create+an+exception+in+%5Bantivirus%5D&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIICAAQigUQhgM6BwgjEOoCECdQ1ARY1ARg6ghoAXAAeACAAW2IAW2SAQMwLjGYAQCgAQKgAQGwAQo&sclient=gws-wiz).




## Commands

Currently there are 10 commands. Type these commands into the interface to use them:
- add
- close
- delaccount
- exit
- help
- list
- open
- purge
- remove
- rename

## Requirements

- Python
- Microsoft C++ Build Tools
  - [Offical Website](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - [Automatic Install](https://aka.ms/vs/17/release/vs_BuildTools.exe)



## Credits
Developer - Thomas Kerby
