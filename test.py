def btc2satoshi(btc: float) -> int:
  return int(btc * 10**8)
print(btc2satoshi(0.000013))