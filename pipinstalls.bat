@ECHO OFF
echo "updating pip"
python -m pip install --upgrade pip
echo "installing bcrypt"
pip install bcrypt
echo "installing pathlib"
pip install pathlib
echo "installing cryptography"
pip install cryptography
echo "installing pywin"
pip install pywin32
echo "installing psutil"
pip install psutil
echo "installing argon2"
pip install pyargon2
echo "If you have anymore issues then create an issue on the github"
echo "The program will continue in 5 seconds"
