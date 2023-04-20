# IncVault
IncVault is a command line program that provides encrypted file storage on Windows. It creates a "locker" folder that securely stores your files.

## Features

- [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption using the [Fernet](https://cryptography.io/en/latest/fernet/) algorithm to encrypt your files
- Automatically decrypts files when you want to access them
- Provides a secure encrypted vault for storing sensitive files on Windows

IncVault uses the [Fernet](https://cryptography.io/en/latest/fernet/) [symmetric encryption](https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:online-data-security/xcae6f4a7ff015e7d:data-encryption-techniques/a/symmetric-encryption-techniques) algorithm to encrypt your files. All files added to the locker folder are automatically encrypted. Please note that you should only interact with files stored in your locker through IncVault, unless you are editing the file contents. If an Antivirus causes any issues, you may have to [create an exception](https://www.google.com/search?q=how+to+create+an+exception+in+%5Bantivirus%5D&sxsrf=APwXEdck3w8dJJN2pkH660RpQNwrCi0nNQ%3A1682017158274&source=hp&ei=hotBZIDyDJOR8gLKsYOQCw&iflsig=AOEireoAAAAAZEGZltTE6sDECenhHxi9NiJeOVL1udK-&ved=0ahUKEwiAzeKZkrn-AhWTiFwKHcrYALIQ4dUDCAo&uact=5&oq=how+to+create+an+exception+in+%5Bantivirus%5D&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIICAAQigUQhgM6BwgjEOoCECdQ1ARY1ARg6ghoAXAAeACAAW2IAW2SAQMwLjGYAQCgAQKgAQGwAQo&sclient=gws-wiz).

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



## Credits
Developer - Thomas Kerby
