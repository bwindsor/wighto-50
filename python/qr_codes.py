# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "qrcode[pil]",
# ]
# ///

# Run this file with uv run qr_codes.py
import qrcode


def create_qr_code(url, output_file):
  qr = qrcode.QRCode(
    box_size=30
  )
  qr.add_data(url)
  qr.make(fit=True)
  img = qr.make_image()
  img.save(output_file)


create_qr_code("https://racesignup.co.uk/entry/?eventid=5990", "entries.png")
