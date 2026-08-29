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
create_qr_code("WIFI:T:nopass;S:wight50;;", "results_wifi.png")
create_qr_code("http://192.168.0.100", "local_wifi_results.png")
create_qr_code("https://www.wighto.org.uk/wp-content/uploads/2026/09/needles-and-knolls-results/day1/", "day1_online_results.png")
create_qr_code("https://www.wighto.org.uk/wp-content/uploads/2026/09/needles-and-knolls-results/day2/", "day2_online_results.png")
