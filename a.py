import py5
# マウスの位置を保持する変数
mx, my = 0, 0
# 追加された画像とその位置を保持するリスト
displayed_images = []
# グローバル変数の宣言
img = None
monitor_image = None
monitor2_image = None
monitor3_image = None
chair_image = None
chair2_image = None
chair3_image = None
clock_image = None
clock2_image = None
clock3_image = None
keybord_image = None
keybord2_image = None
keybord3_image = None
mouse_image = None
mouse2_image = None
mouse3_image = None
speker_image = None
speker2_image = None
speker3_image = None
microphone_image = None
microphone2_image = None
microphone3_image = None
def setup():
    global img, monitor_image, monitor2_image, monitor3_image, chair_image, chair2_image, chair3_image
    global clock_image, clock2_image, clock3_image, keybord_image, keybord2_image, keybord3_image
    global mouse_image, mouse2_image, mouse3_image, speker_image, speker2_image, speker3_image
    global microphone_image, microphone2_image, microphone3_image
    py5.size(800, 600, py5.P3D)  # ウィンドウのサイズを指定
    # 画像をロードします
    img = py5.load_image("./image/デスク.jpg")
    monitor_image = py5.load_image("./image/IMG_1343.PNG")
    monitor2_image = py5.load_image('./image/IMG_1361.PNG')
    monitor3_image = py5.load_image('./image/IMG_1374.PNG')
    chair_image = py5.load_image('./image/IMG_1357.PNG')
    chair2_image = py5.load_image('./image/IMG_1358.PNG')
    chair3_image = py5.load_image('./image/IMG_1360.PNG')
    clock_image = py5.load_image('./image/IMG_1362.PNG')
    clock2_image = py5.load_image('./image/IMG_1363.PNG')
    clock3_image = py5.load_image('./image/IMG_1364.PNG')
    keybord_image = py5.load_image('./image/IMG_1365.PNG')
    keybord2_image = py5.load_image('./image/IMG_1366.PNG')
    keybord3_image = py5.load_image('./image/IMG_1367.PNG')
    mouse_image = py5.load_image('./image/IMG_1368.PNG')
    mouse2_image = py5.load_image('./image/IMG_1369.PNG')
    mouse3_image = py5.load_image('./image/IMG_1370.PNG')
    speker_image = py5.load_image('./image/IMG_1381.PNG')
    speker2_image = py5.load_image('./image/IMG_1382.PNG')
    speker3_image = py5.load_image('./image/IMG_1383.PNG')
    microphone_image = py5.load_image('./image/IMG_1384.PNG')
    microphone2_image = py5.load_image('./image/IMG_1385.PNG')
    microphone3_image = py5.load_image('./image/IMG_1386.PNG')
def draw():
    global mx, my, img
    if img is not None:
        py5.image(img, 0, 0, py5.width, py5.height)  # 画像を背景として描画
    mx, my = py5.mouse_x, py5.mouse_y  # マウスの現在位置を取得
    # リストに保持している画像を描画
    for img_info in displayed_images:
        image, x, y, dx, dy = img_info
        py5.image(image, x, y, dx, dy)
def key_pressed():
    global mx, my, displayed_images
    if py5.key == '1':
        displayed_images.append((monitor_image, mx, my, 300, 300))
    elif py5.key == '2':
        displayed_images.append((monitor2_image, mx, my, 300, 300))
    elif py5.key == '3':
        displayed_images.append((monitor3_image, mx, my, 300, 300))
    elif py5.key == '4':
        displayed_images.append((chair_image, mx, my, 500, 500))
    elif py5.key == '5':
        displayed_images.append((chair2_image, mx, my, 500, 500))
    elif py5.key == '6':
        displayed_images.append((chair3_image, mx, my, 500, 500))
    elif py5.key == '7':
        displayed_images.append((clock_image, mx, my, 100, 100))
    elif py5.key == '8':
        displayed_images.append((clock2_image, mx, my, 100, 100))
    elif py5.key == '9':
        displayed_images.append((clock3_image, mx, my, 100, 100))
    elif py5.key == '0':
        displayed_images.append((keybord_image, mx, my, 200, 200))
    elif py5.key == 'q':
        displayed_images.append((keybord2_image, mx, my, 200, 200))
    elif py5.key == 'w':
        displayed_images.append((keybord3_image, mx, my, 200, 200))
    elif py5.key == 'e':
        displayed_images.append((mouse_image, mx, my, 100, 100))
    elif py5.key == 'r':
        displayed_images.append((mouse2_image, mx, my, 100, 100))
    elif py5.key == 't':
        displayed_images.append((mouse3_image, mx, my, 100, 100))
    elif py5.key == 'y':
        displayed_images.append((speker_image, mx, my, 100, 100))
    elif py5.key == 'u':
        displayed_images.append((speker2_image, mx, my, 100, 100))
    elif py5.key == 'i':
        displayed_images.append((speker3_image, mx, my, 100, 100))
    elif py5.key == 'o':
        displayed_images.append((microphone_image, mx, my, 100, 100))
    elif py5.key == 'p':
        displayed_images.append((microphone2_image, mx, my, 100, 100))
    elif py5.key == 'a':
        displayed_images.append((microphone3_image, mx, my, 100, 100))
    elif py5.key == 'z' and displayed_images:
        displayed_images.pop()  # 最後の画像をリストから削除する
    else:
        py5.background(255)  # 他のキーを押したら白色に
py5.run_sketch()