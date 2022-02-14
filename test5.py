import cv2
import json
import numpy as np
from glob import glob

screenshot = cv2.imread('pictures/pick/0.jpg')
candidated_cards = [None, None, None, None]
candidated_cards[0] = screenshot[200:700, 0:500]
candidated_cards[1] = screenshot[300:800, 300:800]
candidated_cards[2] = screenshot[300:800, 1100:1600]
candidated_cards[3] = screenshot[200:700, 1400:1900]

BASIC_PACK = 100
LATEST_PACK = 123
HEIGHT = 270
craft_path = 'B/'
neutral_path = 'Ne/'
img_card_pool = {}

json_open = open('json/all.json', 'r', encoding='utf-8')
json_cards = json.load(json_open)
cards = json_cards['cards']

# Create a card pool
for pack in range(LATEST_PACK, BASIC_PACK-1, -1):
    pack_path = 'pictures/cards/'+str(pack)+'/'
    img_paths = glob(pack_path+craft_path+'*') + \
        glob(pack_path+neutral_path+'*')
    for img_path in img_paths:
        img_card_pool[img_path[-13:-4]
                      ] = cv2.imread(img_path)

    if pack == LATEST_PACK-4:
        pack = BASIC_PACK

akaze = cv2.AKAZE_create()
for candidated_card in candidated_cards:
    max_good_len = 0
    for card_id, card_img in img_card_pool.items():
        gray_candidated_card = cv2.cvtColor(
            candidated_card, cv2.COLOR_BGR2GRAY)
        gray_card_img = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)

        kp1, des1 = akaze.detectAndCompute(gray_candidated_card, None)
        kp2, des2 = akaze.detectAndCompute(gray_card_img, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

        matches = bf.knnMatch(des1, des2, k=2)
        ratio = 0.5
        good = []
        for m, n in matches:
            if m.distance < ratio * n.distance:
                good.append(m)
        if len(good) > max_good_len:
            max_good_len = len(good)
            match_card_id = card_id
            match_card_img = card_img
            for card in cards:
                if match_card_id == str(card['card_id']):
                    match_card_name = card['card_name']
    print(match_card_name)
    # cv2.imshow(match_card_id, match_card_img)
    # cv2.moveWindow(match_card_id, 0, 0)
    # cv2.waitKey(0)
