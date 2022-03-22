from cryptography.fernet import Fernet
import os
if os.path.exists("secrets/wallet.key"):
  print("Wallet loading...")
else:
  print("No Wallet Yet")
def encrypt(file):
  key = Fernet.generate_key()
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
  with open("walletdata.txt", 'wb') as decrypted_file:
      decrypted_file.write(decrypt_file)
  df=open("walletdata.txt")
  decfile=df.read()
  df.close()
  return decfile