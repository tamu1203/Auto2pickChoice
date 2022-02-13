import cv2
import json
import numpy as np
from glob import glob

screenshot = cv2.imread('pictures/pick.jpg')
pick_screens = [None, None, None, None]
pick_screens[0] = screenshot[200:700, 0:500]
pick_screens[1] = screenshot[300:800, 300:800]
pick_screens[2] = screenshot[300:800, 1100:1600]
pick_screens[3] = screenshot[200:700, 1500:2000]
# for pick_screen in pick_screens:
# cv2.imshow('', pick_screen)
# cv2.waitKey(0)
# exit()
# エルフだった場合の処理
latest_pack = 123
craft_path = 'E/'
neutral_path = 'Ne/'
img_card_pool = {}
HEIGHT = 270

json_open = open('json/all.json', 'r', encoding='utf-8')
json_cards = json.load(json_open)
cards = json_cards['cards']
# print(cards)
# exit()

# 最新4パックをカードプールに追加
for pack in range(latest_pack, latest_pack-4, -1):
    pack_path = 'pictures/cards/'+str(pack)+'/'
    imgs_path = glob(pack_path+craft_path+'*') + \
        glob(pack_path+neutral_path+'*')
    for img_path in imgs_path:
        img_card = cv2.imread(img_path)
        img = img_card[170:560, 110:420]
        h, w = img.shape[:2]
        width = round(w * (HEIGHT / h))
        img_card_pool[img_path[-13:-4]
                      ] = cv2.resize(img, dsize=(width, HEIGHT))

# ベーシックカードをカードプールに追加
img_paths = glob('pictures/cards/100/'+craft_path+'*') + \
    glob('pictures/cards/100/'+neutral_path+'*')
for img_path in img_paths:
    img_card = cv2.imread(img_path)
    img = img_card[170:560, 110:420]
    h, w = img.shape[:2]
    width = round(w * (HEIGHT / h))
    img_card_pool[img_path[-13:-4]] = cv2.resize(img, dsize=(width, HEIGHT))

for pick_screen in pick_screens:
    maxMaxVal = 0
    maxMaxLoc = []
    for cardId, value in img_card_pool.items():
        result = cv2.matchTemplate(pick_screen, value, cv2.TM_CCORR_NORMED)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
        if maxVal > maxMaxVal:
            maxMaxVal = maxVal
            maxMaxLoc = maxLoc
            for card in cards:
                if cardId == str(card['card_id']):
                    card_name = card['card_name']
                    print(card_name)
    tl = maxMaxLoc[0], maxMaxLoc[1]
    br = maxMaxLoc[0] + value.shape[1], maxMaxLoc[1] + \
        value.shape[0]
    dst = pick_screen.copy()
    cv2.rectangle(dst, tl, br, color=(0, 255, 0), thickness=2)
    # cv2.namedWindow('', cv2.WINDOW_NORMAL)
    # card_name = card_name.encode("shift-jis").decode("utf-8", errors="ignore")
    cv2.imshow(card_name, dst)
    cv2.moveWindow(card_name, 0, 0)
    cv2.waitKey(0)
