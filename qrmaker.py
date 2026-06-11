from flask import Flask, render_template, request
from PIL import Image, ImageDraw
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
    link = "www.qrlin.kr/v?v=" + linknum
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=0,
    )

    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#000000", back_color="white")
    
    img.save(f"./static/qr.png")
    qr = Image.open("./static/qr.png")
    re_img = qr.resize((325, 325), Image.LANCZOS)  # Image.ANTIALIAS
    re_img.save(f"./static/qr.png")

    
    return render_template('index.html' , img=f"{folder_path}\\qr.png", linknum=linknum)
def stylize_qr(qr, center_logos):
    """와이파이 QR과 동일하게 원형 닷 + 중앙 로고 + 모서리 마커로 꾸민 뒤 static/qr.png 로 저장한다.

    center_logos: [(파일명, 중앙 비우는 원 반지름), ...] 순서대로 겹쳐 그린다.
    """
    # 기본 QR 코드 이미지 생성 (검정/흰색)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    w, h = qr_img.size

    # 흰 배경의 새 캔버스
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 검은 픽셀을 원형 닷 이미지로 치환
    pixels = qr_img.load()
    box_size = 10
    dot = Image.open(os.path.join(basedir, "static", "dot.png")).convert("RGBA")
    dot = dot.resize((10, 10), Image.LANCZOS)
    for x in range(0, w, box_size):
        for y in range(0, h, box_size):
            if pixels[x, y][:3] == (0, 0, 0):
                img.paste(dot, (x, y), mask=dot)

    # 중앙 로고 추가 (해당 영역의 닷을 지운 뒤 로고 삽입)
    for logo_file, radius in center_logos:
        logo_path = os.path.join(basedir, "static", logo_file)
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo_size = w // 5  # QR 크기의 약 1/5
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            logo_pos = ((w - logo_size) // 2, (h - logo_size) // 2)

            # 로고가 들어갈 영역의 닷을 흰색으로 지움 (로고보다 작지 않게 보정)
            center_x = w // 2
            center_y = w // 2
            radius = max(radius, logo_size // 2 + 3)
            left_up = (center_x - radius, center_y - radius)
            right_down = (center_x + radius, center_y + radius)
            draw.ellipse([left_up, right_down], outline=None, fill=(255, 255, 255, 255))

            img.paste(logo, logo_pos, mask=logo)

    # 모서리 3곳에 둥근 사각형 마커
    sqare_path = os.path.join(basedir, "static", "sqare.png")
    if os.path.exists(sqare_path):
        logo = Image.open(sqare_path).convert("RGBA")
        logo_size = 70
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        for i in range(3):
            if i == 0: logo_pos = (0, 0)
            elif i == 1: logo_pos = ((w - logo_size), 0)
            else: logo_pos = (0, (w - logo_size))

            draw.rectangle(
                [logo_pos, (logo_pos[0] + logo_size, logo_pos[1] + logo_size)],
                fill=(255, 255, 255, 255)
            )
            img.paste(logo, logo_pos, mask=logo)

    # 저장 및 고해상도 리사이즈
    img.save("./static/qr.png")
    re_img = Image.open("./static/qr.png").resize((1000, 1000), Image.LANCZOS)
    re_img.save("./static/qr.png")


@app.route('/link_qr')
def link_qr():
    link = request.args['link']

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # 와이파이 QR과 동일한 스타일 (원형 닷 + 모서리 마커), 중앙 로고는 없음
    stylize_qr(qr, [])

    return render_template('index.html', img=f"{folder_path}\\qr.png", link=link)

@app.route('/wifi_qr')
def wifi_qr():
    ssid = request.args['id']
    password = request.args['password']
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
    qr.add_data(f'WIFI:S:{ssid};T:WPA;P:{password};H:true;;')
    qr.make(fit=True)

    stylize_qr(qr, [("phone.png", 31), ("wifi.png", 35)])

    return render_template('index.html', img=f"{folder_path}\\qr.png", ssid=ssid, password=password)


webview.create_window('QR-Generator', app, width=1500, height=1000, min_size=[1400,1000], text_select=True)
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

