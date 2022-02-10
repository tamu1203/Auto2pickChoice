import cv2  # OpenCVをインポート

image = cv2.imread('pictures/pick.jpg')  # 検索先画像のファイルパスを指定
tem = cv2.imread('pictures/C_123131020.png')
template = tem[170:560, 110:420]
cv2.imshow('test.jpg', template)
cv2.waitKey(0)
result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

if maxVal > 0.8:
    tl = maxLoc[0], maxLoc[1]
    br = maxLoc[0] + template.shape[1], maxLoc[1] + template.shape[0]

    dst = image.copy()
    cv2.rectangle(dst, tl, br, color=(0, 255, 0), thickness=2)

    cv2.imshow('', dst)
    cv2.waitKey(0)
