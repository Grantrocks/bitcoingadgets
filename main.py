import os
import pandas
from getlucky import getlucky
from bit import Key
import requests
from bip_utils import (
    Bip39EntropyBitLen, Bip39EntropyGenerator, Bip39WordsNum, Bip39Languages, Bip39MnemonicGenerator, Bip39MnemonicEncoder, Bip39SeedGenerator, Bip44Coins, Bip44, Bip44Changes, Bip44Levels
)
import random
from makeqr import gqr
def wallet(mnemonic):
  seed_bytes = Bip39SeedGenerator(str(mnemonic)).Generate()
  bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
  bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
  bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
  while True:
    print("1=View Balance | 2=Send BTC | 7=Receive BTC | 3=Danger Zone | 4=View Transactions | 5=Security | 6=Tools | 8=View All Addresses")
    choice=input("Option: ")
    if choice=="5":
      print(f"Mnemonic: {mnemonic}")
    elif choice=="q":
      exit()
    elif choice=="1":
      total = 0
      request=[]
      for i in range(0,50):
        rec_key = bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
        rec_address = bip44_addr_ctx.PublicKey().ToAddress()
        request +=[rec_address]
      addresses="|".join(request)
      url = "https://blockchain.info/balance?active="+addresses
      response = requests.get(url)
      balance = response.json()
      for i in request:
        addr=balance[i]
        final=addr["final_balance"]
        total+=final
      print("BTC Balance: "+str(total))
    elif choice=="6":
      print("1=Get Lucky")
      tool=input("Option: ")
      if tool=="1":
        getlucky()
    elif choice=="2":
      print("Enter q to cancel")
      sendkey=Key(input("Address WIF to Send From: "))
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
      addr=input("Which Address To Check: ")
      transactions_url = 'https://blockchain.info/rawaddr/'+addr
      df = pandas.read_json(transactions_url)
      transactions = df['txs']
      for i in range(len(transactions)):
        print(transactions[i]['hash'])
    elif choice=="7":
      bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(random.randint(0,50))
      rec_address = rec_key.Address()
      print("Receiving Address: "+rec_address)
      gqr(rec_address)
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
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
        rec_wif=bip44_addr_ctx.PrivateKey().ToWif()
        rec_address=bip44_addr_ctx.PublicKey().ToAddress()
        print(f"Wallet {i}: {rec_address} WIF: {rec_wif}")
    wallet(mnemonic)
def main():
  os.system("clear")
  if os.path.exists("walletdata.txt"):
    f=open("walletdata.txt")
    mnemo=f.read()
    f.close()
    wallet(mnemo)
  else:
    options=input("1=Create Wallet | 2=Import Wallet: ")
    if options=="1":
      words= Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)
      f=open('walletdata.txt',"a")
      f.write(f"{words}")
      f.close()
      wallet(words)
      print("Write down these words. If you lose them you wont be able to recover your wallet!")
      print()
      print(words)
      print()
      wallet(words)
    elif options=="2":
      words=input("Mnemonic Seed: ")
      f=open('walletdata.txt',"a")
      f.write(f"{words}")
      f.close()
      wallet(words)
main()