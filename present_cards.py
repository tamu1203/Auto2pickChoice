import cv2
import json
import pickle
import os
from glob import glob
from tqdm import tqdm

BASIC_PACK = 100
LATEST_PACK = 123
RESIZE_WIDTH = 500
CARDS_PATH = 'pictures\\card_imgs\\'

json_open = open('json_ja\\all.json', 'r', encoding='utf-8')
json_cards = json.load(json_open)
cards = json_cards['cards']
ALL_CARD_IMG = {}
for card in cards:
    ALL_CARD_IMG[str(card['card_id'])] = card
AKAZE = cv2.AKAZE_create()
if os.path.isdir('pickle'):
    ref_des = pickle.load(open('pickle\\descripter.pickle', mode="rb"))


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


def get_img(img_paths):
    card_pool_img = {}
    for img_path in tqdm(img_paths):
        img = cv2.imread(img_path)
        card_pool_img[img_path[-13:-4]] = img[170:560, 110:420]
    return card_pool_img


def get_card_pool(craft):
    crafts = ['forest', 'sword', 'rune', 'dragon',
              'shasow', 'blood', 'haven', 'portal']
    craft_num = str(crafts.index(craft)+1)
    high_rarity_paths = []
    craft_b_paths = []
    craft_s_paths = []
    neutral_bsg_paths = []
    for pack in [BASIC_PACK] + list(range(LATEST_PACK, LATEST_PACK-4, -1)):
        pack_path = CARDS_PATH+'C_'+str(pack)
        high_rarity_paths += glob(pack_path+craft_num+'3*')+glob(
            pack_path+craft_num+'4*')+glob(pack_path+'04*')
        craft_b_paths.extend(glob(pack_path+craft_num+'1*'))
        craft_s_paths.extend(glob(pack_path+craft_num+'2*'))
        neutral_bsg_paths += glob(pack_path+'01*') + \
            glob(pack_path+'02*')+glob(pack_path+'03*')
    high_rarity = get_img(high_rarity_paths)
    craft_b = get_img(craft_b_paths)
    craft_s = get_img(craft_s_paths)
    neutral_bsg = get_img(neutral_bsg_paths)
    return high_rarity, craft_b, craft_s, neutral_bsg


def get_descriptor(img, card_id=None):
    if card_id is not None:
        des = ref_des[card_id]
    else:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, des = AKAZE.detectAndCompute(gray_img, None)
    return des


def get_good(comp_img, ref_img, card_id=None):
    comp_des = get_descriptor(comp_img)
    ref_des = get_descriptor(ref_img, card_id)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(comp_des, ref_des, k=2)
    ratio = 0.5
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append(m)
    return good


def get_present_cards(screen, card_pool_img):
    present_cards = []
    trim_screens = get_trim_screens(screen)
    for trim_screen in trim_screens:
        max_good_len = 0
        present_card_id = ''
        for card_id, card_img in card_pool_img.items():
            good = get_good(trim_screen, card_img, card_id)
            if (good_len := len(good)) > max_good_len:
                max_good_len = good_len
                present_card_id = card_id
        present_cards.append(ALL_CARD_IMG[present_card_id])
    return present_cards


def main():
    high_rarity, craft_b, craft_s, neutral_bsg = get_card_pool('portal')
    for i in range(1, 16):
        screen = cv2.imread('pictures/portal_craft/'+str(i)+'.jpg')
        if i in (1, 8, 15):
            present_cards = get_present_cards(screen, high_rarity)
        elif i in (2, 4, 7, 9, 11, 13):
            present_cards = get_present_cards(screen, craft_b)
        elif i in (3, 6, 12, 14):
            present_cards = get_present_cards(screen, craft_s)
        else:
            present_cards = get_present_cards(screen, neutral_bsg)

        print(str(i)+'th screen')
        t = ('st', 'nd', 'rd', 'th')
        for i, present_card in enumerate(present_cards):
            print(str(i+1)+t[i]+' card : '+present_card['card_name'])


if __name__ == '__main__':
    main()
