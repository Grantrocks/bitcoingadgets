import time
import os
from colorama import Style,Fore,Back, init
init(autoreset=True)
from mnemonic import Mnemonic
from bs4 import BeautifulSoup
import bip32utils
import requests
mnemon = Mnemonic('english')
def getlucky():
  message = '''
  =========================[CRYPTOANDPI]==============================
  |         This tool is free to use and we charge no fees.           |
  |    Because of this we are asking for donations to support us.     |
  |         If you get lucky and get a wallet please check to make    |
  |                   sure that its not active.                       |
  =========================[CRYPTOANDPI]==============================
  = Athur : Crypto And Pi
  = Email : owner@cryptoandpi.cf
  = Web : https://cryptoandpi.cf
  =========================[CRYPTOANDPI]==============================
  || Donate =   Bitcoin bc1q7d0ycqy5wfvnq3dhe4s77qa4g37a3zpngsan5a   ||
  =========================[CRYTPOANDPI]==============================
          '''
  
  print(message)
  print('===[Make sure to check out website for updates and other tools]===')
  time.sleep(2)
  z = 1
  while True:
      words = mnemon.generate(256)
      mnemon.check(words)
      seed = mnemon.to_seed(words)
      root_key = bip32utils.BIP32Key.fromEntropy(seed)
      child_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0) 
      btcaddr1 = child_key.Address()
      privatekey = child_key.PublicKey().hex()
      URL = ('https://bitcoin.atomicwallet.io/address/' + btcaddr1)
      markup = "<h1></h1>"
      HEADERS = {
          "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537'}
      page = requests.get(URL, headers=HEADERS)
      soup = BeautifulSoup(page.content, 'html.parser')
      small = soup.find("small", {"class": 'text-muted'}).get_text()
      rnd = str(small)[:2]
      print(str(z), 'ADDRESS=', str(btcaddr1), str(rnd), '[ CRYPTOANDPI ]')
      z += 1
      if int(rnd) > 0:
          print('=======================[ CRYPTO AND PI ]=======================')
          print('Saved information, privatekey and balance, on the btcWallet.txt ')
          print('=======================[ CRYPTO AND PI ]=======================')
          f = open("btcWallet.txt", "a")
          f.write(privatekey + '\n')
          f.write(btcaddr1 + '  BAL= ' + str(rnd) + '\n')
          f.close()
          continue