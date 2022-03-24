from cryptography.fernet import Fernet
def encrypt(file):
  key = Fernet.generate_key()
  with open('data/session.key', 'wb') as filekey:
    filekey.write(key)
  with open('data/session.key', 'rb') as filekey:
      key = filekey.read()
  fernet = Fernet(key)
  with open(file, 'rb') as f:
      original = f.read()
  encrypted = fernet.encrypt(original)
  with open(file, 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
def decrypt(file):
  with open('data/session.key', 'rb') as filekey:
      key = filekey.read()
  fernet = Fernet(key)
  with open(file, 'rb') as enc_file:
      encrypted = enc_file.read()
  decrypted = fernet.decrypt(encrypted)
  with open(file, 'wb') as dec_file:
      dec_file.write(decrypted)