from cryptography.fernet import Fernet
import os
if os.path.exists("filekey.key"):
  print()
else:
  key = Fernet.generate_key()
  with open('filekey.key', 'wb') as filekey:
    filekey.write(key)
def encrypt(file):
  with open('filekey.key', 'rb') as filekey:
  	key = filekey.read()
  fernet = Fernet(key)
  with open('walletdata.txt', 'rb') as file:
  	original = file.read()
  encrypted = fernet.encrypt(original)
  with open('walletdata.txt', 'wb') as encrypted_file:
  	encrypted_file.write(encrypted)
def decrypt(file):
  with open('filekey.key', 'rb') as filekey:
  	key = filekey.read()
  fernet = Fernet(key)
  # opening the encrypted file
  with open('walletdata.txt', 'rb') as enc_file:
  	encrypted = enc_file.read()
  # decrypting the file
  decrypted = fernet.decrypt(encrypted)
  # opening the file in write mode and
  # writing the decrypted data
  with open('walletdata.txt', 'wb') as dec_file:
  	dec_file.write(decrypted)
  wd=open("walletdata.txt")
  df=wd.read()
  return df