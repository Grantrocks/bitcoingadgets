from mnemonic import Mnemonic
import bip32utils
from encrypt import encrypt,decrypt
import os
import pandas
from getlucky import getlucky
from bit import Key
mnemon = Mnemonic('english')
print("Make sure you type quit in the app or your files cant be accesed anymore!!!")
def wallet(mnemonic):
  seed=mnemon.to_seed(mnemonic)
  root_key = bip32utils.BIP32Key.fromEntropy(seed)
  child_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
  child_address = child_key.Address()
  child_public_hex = child_key.PublicKey().hex()
  child_private_wif = child_key.WalletImportFormat()
  sendkey=Key(child_private_wif)
  print(child_address)
  while True:
    print("1=View Balance | 2=Send BTC | 3=Danger Zone | 4=View Transactions | 5=Security | 6=Tools")
    choice=input("Option: ")
    encrypt("walletdata.txt")
    if choice=="5":
      print(f"Private Key WIF: {child_private_wif}")
      print(f"Public Key HEX: {child_public_hex}")
      print(f"Mnemonic: {mnemonic}")
    elif choice=="1":
      print("BTC Balance: "+sendkey.get_balance())
    elif choice=="6":
      print("1=Get Lucky")
      tool=input("Option: ")
      if tool=="1":
        encrypt("walletdata.txt")
        getlucky()
    elif choice=="2":
      print("Enter q to cancel")
      recip=input("Address To Send To: ")
      qty=float(input("Amount To Send: "))
      if float(sendkey.get_balance())<=qty:
        print("You tried to send more than you have!")
      elif recip=="q" or qty=="q":
        print("Cancelled")
      else:
        tx_hash = sendkey.send([(recip, qty, 'btc')])
        print("Your transactions hash: "+str(tx_hash))
    elif choice=="4":
      transactions_url = 'https://blockchain.info/rawaddr/'+child_address
      df = pandas.read_json(transactions_url)
      transactions = df['txs']
      for i in range(len(transactions)):
        print(transactions[i]['hash'])
    wallet(mnemonic)
def main():
  if os.path.exists("walletdata.txt"):
    df=decrypt("walletdata.txt")
    wallet(df,)
  else:
    options=input("1=Create Wallet | 2=Import Wallet: ")
    if options=="1":
      words = mnemon.generate(256)
      seed = mnemon.to_seed(words)
      root_key = bip32utils.BIP32Key.fromEntropy(seed)
      child_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0) 
      child_private_wif = child_key.WalletImportFormat()
      child_address = child_key.Address()
      print(f"Mnemonic: {words}")
      print(f'Address: {child_address}')
      print(f'Private: {child_private_wif}\n')
      f=open('walletdata.txt',"a")
      f.write(words)
      f.close()
      wallet(words)
    elif options=="2":
      words=input("Mnemonic Seed: ")
      seed = mnemon.too_seed(words)
      root_key = bip32utils.BIP32Key.fromEntropy(seed)
      child_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0) 
      child_private_wif = child_key.WalletImportFormat()
      child_address = child_key.Address()
      print(f"Mnemonic: {words}")
      print(f'Address: {child_address}')
      print(f'Private: {child_private_wif}\n')
      f=open('walletdata.txt',"a")
      f.write(words)
      f.close()
      wallet(words)
main()