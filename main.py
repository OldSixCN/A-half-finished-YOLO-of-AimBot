import keyboard
import pynput.mouse
import torch
import mss
import numpy as np
import cv2
import win32con
import win32gui

model = torch.hub.load(r'D:\PYthonzimiao\sources\yolov5-master', 'custom',
                       path=r'D:\PYthonzimiao\sources\best.pt', source='local')

sct = mss.mss()
screen_width = 1920  # 屏幕的宽
screen_height = 1080  # 屏幕的高
GAME_LEFT, GAME_TOP, GAME_WIDTH, GAME_HEIGHT = screen_width // 3, screen_height // 3, screen_width // 3, screen_height // 3  # 游戏内截图区域
RESIZE_WIN_WIDTH, RESIZE_WIN_HEIGHT = screen_width // 4, screen_height // 4  # 显示窗口大小
monitor = {
    'left': GAME_LEFT,
    'top': GAME_TOP,
    'width': GAME_WIDTH,
    'height': GAME_HEIGHT
}
window_name = 'test'

# 加载鼠标驱动控制
mouse_controller = pynput.mouse.Controller()


def CalculateDistance(x, y):  # distance : (-100,100) -> "n,100,p,100*"
    if x < 0:
        x *= -1
        x_d = "n"
    else:
        x_d = "p"
    if y < 0:
        y *= -1
        y_d = "n"
    else:
        y_d = "p"

    x_v = int(x / 5)
    y_v = int(y / 5)
    code = x_d + "," + str(x_v) + "," + y_d + "," + str(y_v) + "*"
    return code


while True:
    img = np.array(sct.grab(monitor))
    results = model(img, size=640)
    df = results.pandas().xyxy[0]
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # cv2.WINDOW_NORMAL 根据窗口大小设置我们的图片大小
    cv2.resizeWindow(window_name, RESIZE_WIN_WIDTH, RESIZE_WIN_HEIGHT)
    hwnd = win32gui.FindWindow(None, window_name)
    # hwnd = win32gui.FindWindow('xx.exe', None)
    # 窗口需要正常大小且在后台，不能最小化
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    # 窗口需要最大化且在后台，不能最小化
    # ctypes.windll.user32.ShowWindow(hwnd, 3)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
    try:  # # 实现实时屏幕标记
        xmin = int(df.iloc[0, 0])
        ymin = int(df.iloc[0, 1])
        xmax = int(df.iloc[0, 2])
        ymax = int(df.iloc[0, 3])
        head_level = (int(xmin + (xmax - xmin) / 2), int(ymin + (ymax - ymin) / 8))
        cv2.circle(img, head_level, 4, (0, 255, 0), thickness=-1)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        distance = (head_level[0] - 320, head_level[1] - 320)

    except:
        print("", end="")

    cv2.imshow(window_name, img)
    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC
        cv2.destroyAllWindows()
        exit('ESC ...')
