import pyautogui as pag
import cv2
import numpy as np
import pygetwindow as gw
import keyboard

# pillowをopencvに変換
# https://qiita.com/derodero24/items/f22c22b22451609908ee


def pil2cv(image):
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:
        pass
    elif new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def sv_screenshot():
    while True:
        if keyboard.read_key() == 'space':
            window = gw.getWindowsWithTitle('test.mp4')[0]
            # window = gw.getWindowsWithTitle('Shadowverse')[0]
            x, y = window.topleft
            width, height = window.size
            # pag.screenshot('pictures\\test.png', region=(x, y, width, height))
            return pil2cv(pag.screenshot(region=(x, y, width, height)))


def main():
    print(sv_screenshot())


if __name__ == '__main__':
    main()
