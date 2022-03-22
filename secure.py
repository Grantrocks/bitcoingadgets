from cryptography.fernet import Fernet
import os
if os.path.exists("secrets/wallet.key"):
  print("Wallet located")
else:
  os.mkdir("secrets")
def encrypt(file):
  key = Fernet.generate_key()
  # write the key in a file of .key extension
  with open('secrets/wallet.key', 'wb') as filekey:
      filekey.write(key)
  fernet = Fernet(key)
  with open("walletdata.txt", 'rb') as f:
      file = f.read()
  encrypt_file = fernet.encrypt(file)
  with open("walletdata.txt", 'wb') as encrypted_file:
    encrypted_file.write(encrypt_file)
def decrypt(file):
  with open('secrets/wallet.key', 'rb') as filekey:
    key = filekey.read()
  fernet = Fernet(key)
  with open("walletdata.txt", 'rb') as f:
    file = f.read()
  decrypt_file = fernet.decrypt(file)
  return decrypt_file