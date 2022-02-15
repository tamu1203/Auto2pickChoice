import cv2
import json
import numpy as np
from glob import glob


BASIC_PACK = 100
LATEST_PACK = 123
RESIZE_WIDTH = 500
CARDS_PATH = 'pictures\card_imgs\C_'

json_open = open('json/all.json', 'r', encoding='utf-8')
json_cards = json.load(json_open)
cards = json_cards['cards']
ALL_CARD_IMG = {}
for card in cards:
    ALL_CARD_IMG[str(card['card_id'])] = card
AKAZE = cv2.AKAZE_create()


def get_trim_screens(screen):
    trim_screens = []
    height_three_part = screen.shape[0]//3
    width_fifth_part = screen.shape[1]//5
    trim_screens.append(
        screen[height_three_part:height_three_part*2, :width_fifth_part])
    trim_screens.append(
        screen[height_three_part:height_three_part*2, width_fifth_part:width_fifth_part*2])
    trim_screens.append(
        screen[height_three_part:height_three_part*2, width_fifth_part*3:width_fifth_part*4])
    trim_screens.append(
        screen[height_three_part:height_three_part*2, width_fifth_part*4:width_fifth_part*5])
    for i, trim_screen in enumerate(trim_screens):
        h, w = trim_screen.shape[:2]
        height = round(h * (RESIZE_WIDTH / w))
        trim_screens[i] = cv2.resize(
            trim_screen, dsize=(RESIZE_WIDTH, height))
    return trim_screens


def get_card_pool_img(craft):
    card_pool_img = {}
    for pack in [BASIC_PACK] + list(range(LATEST_PACK, LATEST_PACK-4, -1)):
        img_paths = glob(CARDS_PATH+str(pack)+craft+'*') + \
            glob(CARDS_PATH+str(pack)+'0*')
        for img_path in img_paths:
            img = cv2.imread(img_path)
            card_pool_img[img_path[-13:-4]] = img[170:560, 110:420]
    return card_pool_img


def get_good(comp_img, ref_img):
    gray_comp_img = cv2.cvtColor(
        comp_img, cv2.COLOR_BGR2GRAY)
    gray_ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    _, des1 = AKAZE.detectAndCompute(gray_comp_img, None)
    _, des2 = AKAZE.detectAndCompute(gray_ref_img, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)
    ratio = 0.5
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append(m)
    return good

def get_present_cards(screen, craft):
    present_cards = []
    trim_screens = get_trim_screens(screen)
    card_pool_img = get_card_pool_img(craft)
    for trim_screen in trim_screens:
        max_good_len = 0
        present_card_id = ''
        for card_id, card_img in card_pool_img.items():
            good = get_good(trim_screen, card_img)
            if (good_len := len(good)) > max_good_len:
                max_good_len = good_len
                present_card_id = card_id
        present_cards.append(ALL_CARD_IMG[present_card_id])
    return present_cards


def main():
    screen = cv2.imread('pictures/pick/10.jpg')
    present_cards = get_present_cards(screen, '7')
    for i, present_card in enumerate(present_cards):
        print(str(i+1)+'th card : '+present_card['card_name'])


if __name__ == '__main__':
    main()
