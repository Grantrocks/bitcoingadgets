import os
from getlucky import getlucky
from bit import Key
import requests
import satoshi
import pandas
from bip_utils import (
    Bip39EntropyBitLen, Bip39EntropyGenerator, Bip39WordsNum, Bip39Languages, Bip39MnemonicGenerator, Bip39MnemonicEncoder, Bip39SeedGenerator, Bip44Coins, Bip44, Bip44Changes, Bip44Levels
)
import random
from cryptos import *
c = Bitcoin(testnet=False)
from makeqr import gqr
def btc2satoshi(btc: float) -> int:
  return int(btc * 10**8)
def wallet(mnemonic):
  seed_bytes = Bip39SeedGenerator(str(mnemonic)).Generate()
  bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
  bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
  bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
  while True:
    print("1=View Balance | 2=Send BTC | 7=Receive BTC | 3=Danger Zone | 4=View Transactions | 5=Security | 6=Tools | 8=View All Addresses | c=credits")
    choice=input("Option: ")
    if choice=="5":
      print(f"Mnemonic: {mnemonic}")
    elif choice=="q":
      exit()
    elif choice=="1":
      total = 0
      request=[]
      for i in range(0,44):
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
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
      for i in range(44):
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
        rec_wif=bip44_addr_ctx.PrivateKey().ToWif()
        rec_address=bip44_addr_ctx.PublicKey().ToAddress()
        print(f"Wallet {i}: {rec_address} WIF: {rec_wif}")
      send_from=input("Address WIF to send from: ")
      pub = c.privtopub(send_from)
      priv=send_from
      addr=pubtoaddr(pub)
      inputs = c.unspent(addr)
      send_to=input("Address To Send To: ")
      send_from_key=Key(send_from)
      send_from_balance=float(send_from_key.get_balance('usd'))
      print(f"Balance in USD: ${send_from_balance}")
      send_qty=float(input("Amount to send in USD: $"))
      if send_from_balance>send_qty:
        send_qty=btc2satoshi(send_qty)
        outputs=[{'value': send_qty, 'address':send_to}]
        print(outputs)
        tx = c.mktx(inputs,outputs)
        print(tx)
      else:
        print("You cant send more than you have!")
    elif choice=="4":
      addr=input("Which Address To Check: ")
      transactions_url = 'https://blockchain.info/rawaddr/'+addr
      df = pandas.read_json(transactions_url)
      transactions = df['txs']
      for i in range(len(transactions)):
        print(transactions[i]['hash'])
    elif choice=="7":
      bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
      rk= bip44_chg_ctx.AddressIndex(random.randint(0,10))
      rec_address = rk.PublicKey().ToAddress()
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
      for i in range(44):
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
        rec_wif=bip44_addr_ctx.PrivateKey().ToWif()
        rec_address=bip44_addr_ctx.PublicKey().ToAddress()
        print(f"Wallet {i+1}: {rec_address} WIF: {rec_wif}")
    elif choice=="c":
      print("Bitcoin Gadgets is a bitcoin HD Wallet created by Grant McNamara or Grantrocks to help you securely store your cryptocurrency. It contains some helpful toos such as a lucky generator and more.")
      don=input("Donate to the creator? (y/n): ")
      if don=="y":
        print("Thank you for choosing to donate press q to cancel.")
        don_qty=input("Amount in USD:  ")
        fr_wif=input("Wallet WIF to send from: ")
        don_key=Key(fr_wif)
        if float(don_key.get_balance('usd'))>float(don_qty):
          confirm=input(f"Send ${don_qty} to the creator? (y/n): ")
          if confirm=="y":
            donate_tx=don_key.send([('bc1q7d0ycqy5wfvnq3dhe4s77qa4g37a3zpngsan5a',float(don_qty),'usd')],fee=1)
            print("Sent the donation. TX ID: ")
            print(donate_tx)
            print("Thank you for donating!")
          else:
            print("Cancelled")
        else:
          print("Not enough btc to send donation with the fee.")
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