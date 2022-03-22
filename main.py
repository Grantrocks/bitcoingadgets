from mnemonic import Mnemonic
import bip32utils
import os
import secure
import pandas
from getlucky import getlucky
from bit import Key
import random
mnemon = Mnemonic('english')
def wallet(mnemonic):
  seed=mnemon.to_seed(mnemonic)
  root_key = bip32utils.BIP32Key.fromEntropy(seed)
  child_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
  child_address = child_key.Address()
  child_public_hex = child_key.PublicKey().hex()
  child_private_wif = child_key.WalletImportFormat()
  sendkey=Key(child_private_wif)
  while True:
    print("1=View Balance | 2=Send BTC | 7=Receive BTC | 3=Danger Zone | 4=View Transactions | 5=Security | 6=Tools | 8=View All Addresses")
    choice=input("Option: ")
    if choice=="5":
      print(f"Private Key WIF: {child_private_wif}")
      print(f"Public Key HEX: {child_public_hex}")
      print(f"Mnemonic: {mnemonic}")
    elif choice=="q":
      secure.encrypt("walletdata.txt")
      exit()
    elif choice=="1":
      print("BTC Balance: "+sendkey.get_balance())
    elif choice=="6":
      print("1=Get Lucky")
      tool=input("Option: ")
      if tool=="1":
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
    elif choice=="7":
      rec_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(random.randint(1,50))
      rec_address = rec_key.Address()
      print("Receiving Address: "+rec_address)
    elif choice=="3":
      print("You are in the danger zone. Actions here can be permanent.")
      dangerchoice=input("1=Remove Wallet")
      if dangerchoice=="1":
        print("Removing wallet...")
        os.unlink("walletdata.txt")
        os.unlink("secrets/wallet.key")
        os.rmdir("secrets")
        print("Wallet Removed")
        print("You can restore it with this word phrase\n "+mnemonic)
        exit()
    elif choice=="8":
      for i in range(51):
        rec_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i)
        rec_address = rec_key.Address()
        print(f"Wallet {i}: {rec_address}")
    wallet(mnemonic)
def main():
  os.system("clear")
  if os.path.exists("secrets/wallet.key"):
    df=secure.decrypt("walletdata.txt")
    secure.encrypt("walletdata.txt")
    wallet(df)
  else:
    os.mkdir("secrets")
    options=input("1=Create Wallet | 2=Import Wallet: ")
    if options=="1":
      words = mnemon.generate(256)
      f=open('walletdata.txt',"a")
      f.write(words)
      f.close()
      print("Write down these words. If you lose them you wont be able to recover your wallet!")
      print()
      print(words)
      print()
      secure.encrypt("walletdata.txt")
      wallet(words)
    elif options=="2":
      words=input("Mnemonic Seed: ")
      f=open('walletdata.txt',"a")
      f.write(words)
      f.close()
      secure.encrypt("walletdata.txt")
      wallet(words)
class MainWindow(object):
  def start():
    try:
        main()
    except KeyboardInterrupt:
        MainWindow.stop()
  def stop():
    print("Securing Wallet...")
    print("Secured")
MainWindow.start()