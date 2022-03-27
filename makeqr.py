import qrcode
def gqr(address):
  qr_img = qrcode.make(address)  
  qr_img.save(f"qrcodes/{address}.jpg")
  print("QR Code saved in qr codes")