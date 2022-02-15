import cv2
import json
import numpy as np
from glob import glob


BASIC_PACK = 100
LATEST_PACK = 123


def get_candidated_cards(screenshot):
    candidated_cards = []
    height = screenshot.shape[0]
    width_fifth_part = screenshot.shape[1]//5
    candidated_cards.append(screenshot[0:height, 0:width_fifth_part])
    candidated_cards.append(
        screenshot[0:height, width_fifth_part:width_fifth_part*2])
    candidated_cards.append(
        screenshot[0:height, width_fifth_part*3:width_fifth_part*4])
    candidated_cards.append(
        screenshot[0:height, width_fifth_part*4:width_fifth_part*5])
    return candidated_cards


def get_card_pool_img(craft):
    card_pool_img = {}
    for pack in [BASIC_PACK] + list(range(LATEST_PACK, LATEST_PACK-4, -1)):
        pack_path = 'pictures/cards/'+str(pack)+'/'
        img_paths = glob(pack_path+craft+'/*') + \
            glob(pack_path+'Ne/*')
        for img_path in img_paths:
            img = cv2.imread(img_path)
            card_pool_img[img_path[-13:-4]] = img[170:560, 110:420]
    return card_pool_img


screenshot = cv2.imread('pictures/pick/s3.jpg')
candidated_cards = get_candidated_cards(screenshot)

# for candidated_card in candidated_cards:
#     cv2.imshow('Result', candidated_card)
#     cv2.waitKey(0)
# exit()

card_pool_img = get_card_pool_img('B')
json_open = open('json/all.json', 'r', encoding='utf-8')
json_cards = json.load(json_open)
cards = json_cards['cards']
akaze = cv2.AKAZE_create()

for candidated_card in candidated_cards:
    max_good_len = 0
    for card_id, card_img in card_pool_img.items():
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
        if (good_len := len(good)) > max_good_len:
            max_good_len = good_len
            match_card_id = card_id
            result_img = cv2.drawMatches(
                candidated_card, kp1, card_img, kp2, good, None, flags=2)
            cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
            cv2.imshow('Result', result_img)
            cv2.waitKey(0)
            for card in cards:
                if match_card_id == str(card['card_id']):
                    match_card_name = card['card_name']
    print(match_card_name)
