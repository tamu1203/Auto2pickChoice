import cv2
import json
import numpy as np
from glob import glob

screenshot = cv2.imread('pictures/pick/5.jpg')
candidated_cards = [None, None, None, None]
candidated_cards[0] = screenshot[200:700, 0:500]
candidated_cards[1] = screenshot[300:800, 300:800]
candidated_cards[2] = screenshot[300:800, 1100:1600]
candidated_cards[3] = screenshot[200:700, 1400:1900]

LATEST_PACK = 123
BASIC_PACK = 100
craft_path = 'B/'
neutral_path = 'Ne/'
img_card_pool = {}
HEIGHT = 270

json_open = open('json/all.json', 'r', encoding='utf-8')
json_cards = json.load(json_open)
cards = json_cards['cards']

# Create a card pool
for pack in range(LATEST_PACK, BASIC_PACK-1, -1):
    pack_path = 'pictures/cards/'+str(pack)+'/'
    img_paths = glob(pack_path+craft_path+'*') + \
        glob(pack_path+neutral_path+'*')
    for img_path in img_paths:
        img = cv2.imread(img_path)
        img = img[170:560, 110:420]
        h, w = img.shape[:2]
        width = round(w * (HEIGHT / h))
        img_card_pool[img_path[-13:-4]
                      ] = cv2.resize(img, dsize=(width, HEIGHT))
    if pack == LATEST_PACK-4:
        pack = BASIC_PACK

for candidated_card in candidated_cards:
    max_max_val = 0
    max_max_loc = []
    for card_id, card_img in img_card_pool.items():
        result = cv2.matchTemplate(
            candidated_card, card_img, cv2.TM_CCORR_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > max_max_val:
            max_max_val = max_val
            max_max_loc = max_loc
            max_card_id = card_id
            for card in cards:
                if card_id == str(card['card_id']):
                    card_name = card['card_name']
                    max_card_img = card_img
                    print(card_name)
                    print(max_max_val)
    tl = max_max_loc[0], max_max_loc[1]
    br = max_max_loc[0] + max_card_img.shape[1], max_max_loc[1] + \
        max_card_img.shape[0]
    dst = candidated_card.copy()
    cv2.rectangle(dst, tl, br, color=(0, 255, 0), thickness=2)
    cv2.imshow(max_card_id, dst)
    cv2.moveWindow(max_card_id, 0, 0)
    cv2.waitKey(0)
