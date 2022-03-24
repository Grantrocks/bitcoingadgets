from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service
from forex_python.bitcoin import BtcConverter
from bitcoinlib.transactions import Transaction
import requests
import fastgen
import makeqr
import os
wn=input("Wallet Name: ")
try:
  w=Wallet(wn)
except:
  rtr=input("Restore from mnemonic? (y/n): ")
  if rtr=="y":
    mnem=input("Mnemonic Phrase: ")
    w=Wallet.create(wn,keys=mnem,network='bitcoin')
  else:
    w=Wallet.create(wn)
os.system("clear")
message="""

██████╗░██╗████████╗░█████╗░░█████╗░██╗███╗░░██╗  ░██████╗░░█████╗░██████╗░░██████╗░███████╗████████╗░██████╗
██╔══██╗██║╚══██╔══╝██╔══██╗██╔══██╗██║████╗░██║  ██╔════╝░██╔══██╗██╔══██╗██╔════╝░██╔════╝╚══██╔══╝██╔════╝
██████╦╝██║░░░██║░░░██║░░╚═╝██║░░██║██║██╔██╗██║  ██║░░██╗░███████║██║░░██║██║░░██╗░█████╗░░░░░██║░░░╚█████╗░
██╔══██╗██║░░░██║░░░██║░░██╗██║░░██║██║██║╚████║  ██║░░╚██╗██╔══██║██║░░██║██║░░╚██╗██╔══╝░░░░░██║░░░░╚═══██╗
██████╦╝██║░░░██║░░░╚█████╔╝╚█████╔╝██║██║░╚███║  ╚██████╔╝██║░░██║██████╔╝╚██████╔╝███████╗░░░██║░░░██████╔╝
╚═════╝░╚═╝░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝╚═╝░░╚══╝  ░╚═════╝░╚═╝░░╚═╝╚═════╝░░╚═════╝░╚══════╝░░░╚═╝░░░╚═════╝░
                            
                                    The Most Secure Bitcoin Wallet
                                            Version 1.0.0
"""
print(message)
print("Refreshing...")
w.scan()
def satoshi2bit(btc: float):
  return float(btc/10**8)
def main():
  print("1=View Balance | 2=Send BTC | 3=Recieve BTC | 4=View Transactions | 5=View Wallet Data | 6=Address WIF Lookup | 7=Gadgets | c=Credits/Donations")
  option=input("Option: ")
  if option=="1":
    bitcoin = BtcConverter()
    price = bitcoin.get_latest_price('USD')
    btc=satoshi2bit(w.balance())
    usd=btc*price
    print(f"USD ${usd:f}   BTC {btc:f}")
  elif option=="2":
    print("If you want to cancel the transaction say no to the confirmation")
    sending_to=input("Address To Send To: ")
    bitcoin = BtcConverter()
    price = bitcoin.get_latest_price('USD')
    btc=satoshi2bit(w.balance())
    usd=btc*price
    usd=f"{usd:f}"
    print(f"You have ${usd}")
    sending_qty=float(input("Amount to send USD: $"))
    print("Set the speed at which your transaction should be confirmed. Higher speeds means faster confirmation but a much higher fee. Enter the value exactly as you see it!")
    speed=input("low,normal,high: ")
    if sending_qty<float(usd):
      confirm=input("Send the transaction? (y/n): ")
      if confirm=="y":
        print("Sending $"+str(sending_qty))
        t = w.send([(sending_to,str(sending_qty)+" USD")], offline=True,fee=speed)
        print("Transaction hash")
        print(t)
      else:
        print("Cancelled the transaction")
    else:
      print("You cant send more than you have. Transaction fee included")
  elif option=="3":
    address=w.addresslist()[0]
    print("Send BTC here:  "+address)
    makeqr.gqr(address)
    print("Generated qrcode in the qrcodes folder")
  elif option=="4":
    txs=w.transactions_export()
    for i in txs:
      tx=i[1]
      print(tx)
  elif option=="5":
    print(w.info())
  elif option=="6":
    print("Main is 0. Others are 1,2,3,4,etc.")
    aid=int(input("Address Id For Lookup: "))
    wif=w.wif(is_private=True, account_id=aid)
    print(w.addresslist()[aid],wif)
  elif option=="c":
    print("Bitcoin Gadgets was created as a super secure and fast bitcoin wallet that anybody could use. It has some fun and useful tools to help you with your blockchain expereince. Bitcoin Gadgets was created by Grant McNamara")
    donate=input("Would you like to donate? (y/n): ")
    if donate=="y":
      print("Thank you for choosing to donate!")
      bitcoin = BtcConverter()
      price = bitcoin.get_latest_price('USD')
      btc=satoshi2bit(w.balance())
      usd=btc*price
      usd=f"{usd:f}"
      print(f"You have ${usd} USD")
      donate_qty=float(input("How much to donate: "))
      if donate_qty<float(usd):
        print(f"Sending transaction of ${donate_qty} USD")
        t = w.send([('bc1qh36prv8n03elj6n0zjv0wklezxstvdw75g0m3h', str(donate_qty)+" USD")], offline=True, fee="low")
        print("Donation tx hash")
        print(t)
    else:
      print("Thats ok maybe another time")
  elif option=="7":
    print("1=Time Till Next Block | 2=Address Luck")
    tool=input("Tool: ")
    if tool=="1":
      response=requests.get("https://blockchain.info/q/eta")
      data=response.json()
      time=data/60
      print(f"Time till next block in minutes    {time}")
    elif tool=="2":
      print("This tool uses the defaul account 0 address")
      addr=w.addresslist()[0]
      fastgen.fastgen(addr)
while True:
  main()
  '''try:
    main()
  except:
    print("Closing wallet...")
    exit()'''
