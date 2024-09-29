from PIL import Image
# import threading   
import os, webview, qrcode
import pandas as pd

#  pyinstaller -w --add-data "templates;templates" --add-data "static;static"  --contents-directory "." --icon=.\static\favicon.ico  --noconfirm qrmaker.py

basedir = os.path.abspath(os.path.dirname(__file__))
folder_path = basedir + '\\qrimage'

excel_file = "C:\\Users\\JAEYEON\\Documents\\GitHub\\vcodelist.xlsx"
# get dataframe
df = pd.read_excel(excel_file,header=2, usecols=[0, 1])

# columns Name
df.columns = ['vcode', 'password']
for i,  row in df.iterrows():

    linknum = str(row['vcode'])
    if int(linknum) < 10020 or int(linknum) >10100:
        continue
    password = row['password']
    link = "https://qrlinker.pythonanywhere.com/v?v=" + linknum
    qr = qrcode.QRCode( version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=15, border=0, )
    qr.add_data(link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="white", back_color="black")
    
    img.save(f"./static/parking_qr/{linknum}-{password}.png")
    qr = Image.open(f"./static/parking_qr/{linknum}-{password}.png")
    qr = qr.convert("RGBA")
    data = qr.getdata()
    new_data = []
    for item in data:
    # 흰색을 투명하게 변경
        if item[:3] == (0, 0, 0):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    qr.putdata(new_data)
    re_img = qr.resize((307, 307), Image.LANCZOS)  # Image.ANTIALIAS
    re_img.save(f"./static/parking_qr/{linknum}-{password}.png")
