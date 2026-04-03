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
    security = request.args.get('security', 'WPA')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
    qr.add_data(f'WIFI:S:{ssid};T:{security};P:{password};H:true;;')
    qr.make(fit=True)





# 기본 QR 코드 이미지 생성 (배경 투명)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    w, h = qr_img.size

    # 새로운 캔버스 생성 (투명 배경)
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 원형 닷 적용
    pixels = qr_img.load()
    box_size = 10  # QR 닷 크기

    dot_img = os.path.join(basedir, "static", "dot.png") 
    dot_img = Image.open(dot_img).convert("RGBA")
    dot = dot_img.resize((10,10), Image.LANCZOS)
    for x in range(0, w, box_size):
        for y in range(0, h, box_size):
            if pixels[x, y][:3] == (0, 0, 0): 
                img.paste(dot, (x,y), mask=dot)# 검은색 픽셀일 경우 원형 그리기
                # draw.ellipse((x, y, x + box_size, y + box_size), fill="black")

    # 중앙 로고 추가
    logo_path = os.path.join(basedir, "static", "phone.png")  # 로고 파일 경로
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = w // 5  # QR 코드 크기의 약 1/5 크기로 조정
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)  # 고품질 리사이징

        # 로고 삽입 위치 계산
        logo_pos = ((w - logo_size) // 2, (h - logo_size) // 2)

        # 🔥 로고가 들어갈 부분의 QR 코드 도트 삭제 (로고 영역을 투명하게 만듦)
        center_x = w // 2    # 이미지 너비의 절반
        center_y = w // 2   # 이미지 높이의 절반
        radius = 31
        left_up = (center_x - radius, center_y - radius)
        right_down = (center_x + radius, center_y + radius)
        draw.ellipse([left_up, right_down], outline=None, fill=(255, 255, 255, 255))

        # 로고 삽입 (투명 배경 유지하며 삽입)
        img.paste(logo, logo_pos, mask=logo)

    # 중앙 로고 추가
    logo_path = os.path.join(basedir, "static", "wifi.png")  # 로고 파일 경로
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = w // 5  # QR 코드 크기의 약 1/5 크기로 조정
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)  # 고품질 리사이징

        # 로고 삽입 위치 계산
        logo_pos = ((w - logo_size) // 2, (h - logo_size) // 2)

        # 🔥 로고가 들어갈 부분의 QR 코드 도트 삭제 (로고 영역을 투명하게 만듦)
        center_x = w // 2    # 이미지 너비의 절반
        center_y = w // 2   # 이미지 높이의 절반
        radius = 35 
        left_up = (center_x - radius, center_y - radius)
        right_down = (center_x + radius, center_y + radius)
        draw.ellipse([left_up, right_down], outline=None, fill=(255, 255, 255, 255))

        # 로고 삽입 (투명 배경 유지하며 삽입)
        img.paste(logo, logo_pos, mask=logo)



    logo_path = os.path.join(basedir, "static", "sqare.png")  # 로고 파일 경로
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = 70  # QR 코드 크기의 약 1/5 크기로 조정
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)  # 고품질 리사이징

        # 로고 삽입 위치 계산
        for i in range(3):
            if i == 0: logo_pos = (0, 0)
            elif i == 1:logo_pos = ((w - logo_size), 0)
            else:logo_pos = ( 0, (w - logo_size))

            # 🔥 로고가 들어갈 부분의 QR 코드 도트 삭제 (로고 영역을 투명하게 만듦)
            draw.rectangle(
                [logo_pos, (logo_pos[0] + logo_size, logo_pos[1] + logo_size)],
                fill=(255, 255, 255, 255)  # 투명하게 처리
            )

            # 로고 삽입 (투명 배경 유지하며 삽입)
            img.paste(logo, logo_pos, mask=logo)






    
    img.save(f"./static/qr.png")
    qr = Image.open("./static/qr.png")
    re_img = qr.resize((1000, 1000), Image.LANCZOS)  # Image.ANTIALIAS
    re_img.save(f"./static/qr.png")

    return render_template('index.html' , img=f"{folder_path}\\qr.png", ssid = ssid, password = password, security=security)


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

