import cv2
import numpy as np

screen = cv2.imread('pictures/pick.jpg')

mz = cv2.imread('pictures/piasi.png')

result = cv2.matchTemplate(screen, mz, cv2.TM_CCOEFF_NORMED)

xys = np.rot90(np.where(result > 0.9), -1)

for x, y in xys:
    cv2.rectangle(
        screen, (x, y), (x+mz.shape[0], y+mz.shape[1]), color=(255, 0, 0), thickness=10)

cv2.imshow('', cv2.resize(screen, (640, 480)))
cv2.waitKey(0)
