from PIL import Image, ImageDraw
import os, qrcode
import pandas as pd

# 프로젝트 디렉토리 설정
basedir = os.path.abspath(os.path.dirname(__file__))
output_folder = os.path.join(basedir, 'static', 'parking_qr')
os.makedirs(output_folder, exist_ok=True)  # 폴더가 없으면 생성

excel_file = "C:\\Users\\JAEYEON\\Documents\\GitHub\\vcodelist.xlsx"

# 엑셀 데이터 불러오기
df = pd.read_excel(excel_file, header=2, usecols=[0, 1])
df.columns = ['vcode', 'password']

# QR 코드 생성 루프
for i, row in df.iterrows():
    linknum = str(row['vcode'])
    if 10012 <= int(linknum) <= 10020 :
        password = row['password']
        link = "www.qrlin.kr/v?v=" + linknum

        # QR 코드 생성
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # 오류 보정 높임 (로고 추가 대비)
            box_size=10,
            border=0,
        )
        qr.add_data(link)
        qr.make(fit=True)

        # 기본 QR 코드 이미지 생성 (배경 투명)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
        w, h = qr_img.size

        # 새로운 캔버스 생성 (투명 배경)
        img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
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
                    img.paste(dot, (x,y), mask=dot)

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
            draw.ellipse([left_up, right_down], outline=None, fill=(255, 255, 255, 0))

            # 로고 삽입 (투명 배경 유지하며 삽입)
            # img.paste(logo, logo_pos, mask=logo)

        logo_path = os.path.join(basedir, "static", "sqare.png")  # 로고 파일 경로
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo_size = w // 4  # QR 코드 크기의 약 1/5 크기로 조정
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)  # 고품질 리사이징

            # 로고 삽입 위치 계산
            for i in range(3):
                if i == 0: logo_pos = (0, 0)
                elif i == 1:logo_pos = ((w - logo_size), 0)
                else:logo_pos = ( 0, (w - logo_size))

                # 🔥 로고가 들어갈 부분의 QR 코드 도트 삭제 (로고 영역을 투명하게 만듦)
                draw.rectangle(
                    [logo_pos, (logo_pos[0] + logo_size, logo_pos[1] + logo_size)],
                    fill=(255, 255, 255, 0)  # 투명하게 처리
                )

                # 로고 삽입 (투명 배경 유지하며 삽입)
                img.paste(logo, logo_pos, mask=logo)
        output_path = os.path.join(output_folder, f"{linknum}-{password}.png")
        new_size = (294, 294)  # 원하는 크기로 변경 가능
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)  # 고품질 리사이징

        # 크기 변경된 이미지를 저장
        resized_img.save(output_path, format="PNG", dpi=(300, 300))
