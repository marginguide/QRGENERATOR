from PIL import Image, ImageDraw

# 1. 새 이미지 생성 (예: 400x400 크기, 흰색 배경)
width = 400
height = 400
img = Image.new('RGB', (width, height), 'white')

# 2. Draw 객체 생성
draw = ImageDraw.Draw(img)

# 3. 원의 중심과 반지름 설정
center_x = width // 2    # 이미지 너비의 절반
center_y = height // 2   # 이미지 높이의 절반
radius = 100             # 원의 반지름

# 4. 원 그리기
# (좌상단 x, 좌상단 y, 우하단 x, 우하단 y) 형태로 좌표 지정
left_up = (center_x - radius, center_y - radius)
right_down = (center_x + radius, center_y + radius)

# 원 그리기 (outline은 선 색상, fill은 채우기 색상)
draw.ellipse([left_up, right_down], outline='black', fill=None)
# 채우기 원을 원한다면 fill에 색상 지정 (예: fill='red')

# 5. 이미지 저장 또는 표시
img.save('circle_image.png')  # 파일로 저장
# 또는
img.show()  # 화면에 표시