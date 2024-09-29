from flask import Flask, render_template, request, url_for, redirect, flash, jsonify  
from PIL import Image
# import threading   
import os, webview, qrcode

#  pyinstaller -w --add-data "templates;templates" --add-data "static;static"  --contents-directory "." --icon=.\static\favicon.ico  --noconfirm qrmaker.py

basedir = os.path.abspath(os.path.dirname(__file__))
folder_path = basedir + '\\qrimage'

app = Flask(__name__, static_folder='./static', template_folder='./templates')
app.secret_key = b'_5#y2L"F4Qs8z\n\xec]/'

# 이니셜 작업 해야 하는 것

@app.route('/')
def home():
    return render_template('index.html' )

@app.route('/qrlink_qr')
def qrlink_qr():
    linknum = request.args['link']
    link = "https://qrlinker.pythonanywhere.com/v?v=" + linknum
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=1,
    )

    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="GREEN", back_color="white")
    
    img.save(f"./static/qr.png")
    qr = Image.open("./static/qr.png")
    re_img = qr.resize((325, 325), Image.LANCZOS)  # Image.ANTIALIAS
    re_img.save(f"./static/qr.png")

    
    return render_template('index.html' , img=f"{folder_path}\\qr.png", linknum=linknum)
@app.route('/link_qr')
def link_qr():
    link = request.args['link']

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=1,
    )

    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    img.save(f"./static/qr.png")
    qr = Image.open("./static/qr.png")
    re_img = qr.resize((800, 800), Image.LANCZOS)  # Image.ANTIALIAS
    re_img.save(f"./static/qr.png")

    
    return render_template('index.html' , img=f"{folder_path}\\qr.png", link = link)

@app.route('/wifi_qr')
def wifi_qr():
    ssid = request.args['id']
    password = request.args['password']
    security = 'WPA'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=1,
    )
    qr.add_data(f'WIFI:S:{ssid};T:{security};P:{password};;')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    img.save(f"./static/qr.png")
    qr = Image.open("./static/qr.png")
    re_img = qr.resize((800, 800), Image.LANCZOS)  # Image.ANTIALIAS
    re_img.save(f"./static/qr.png")

    
    return render_template('index.html' , img=f"{folder_path}\\qr.png", ssid = ssid, password = password)
webview.create_window('QR-Generator', app, width=1400, height=1000, min_size=[1400,1000], text_select=True)
if __name__ == '__main__':
    webview.start() 
    
    
# def start_server():
#     app.run(host='0.0.0.0', port=5000)

# if __name__ == '__main__':
#     import threading
#     t = threading.Thread(target=start_server)
#     t.daemon = True
#     t.start()

#     webview.create_window('Margin Guide', url="http://localhost:5000/", min_size=(1400, 1000), text_select=True, )
#     webview.start()

