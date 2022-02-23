import cv2
import json
import pickle
import os
from glob import glob
from tqdm import tqdm
from screenshot import sv_screenshot
from dl_card_scores import dl_card_scores

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


def get_card_pool(craft_num):
    card_pool = {}
    # crafts = ['forest', 'sword', 'rune', 'dragon',
    #           'shadow', 'blood', 'haven', 'portal']
    # craft_num = str(crafts.index(craft)+1)
    img_paths = []
    for pack in [BASIC_PACK] + list(range(LATEST_PACK, LATEST_PACK-4, -1)):
        pack_path = CARDS_PATH+'C_'+str(pack)
        img_paths += glob(pack_path+'0*')+glob(pack_path+str(craft_num+1)+'*')
    for img_path in tqdm(img_paths):
        img = cv2.imread(img_path)
        card_pool[img_path[-13:-4]] = img[170:560, 110:420]
    return card_pool


def get_descriptor(img, card_id=None):
    if card_id is not None:
        des = ref_des[card_id]
    else:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, des = AKAZE.detectAndCompute(gray_img, None)
    return des


def get_good(comp_des, ref_img, card_id=None):
    ref_des = get_descriptor(ref_img, card_id)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(comp_des, ref_des, k=2)
    ratio = 0.5
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append(m)
    return good


def get_present_cards(trim_screens, card_pool_img):
    present_cards = []
    for trim_screen in trim_screens:
        max_good_len = 0
        present_card_id = ''
        comp_des = get_descriptor(trim_screen)
        for card_id, card_img in card_pool_img.items():
            good = get_good(comp_des, card_img, card_id)
            if (good_len := len(good)) > max_good_len:
                max_good_len = good_len
                present_card_id = card_id
        present_cards.append(ALL_CARD_IMG[present_card_id])
    return present_cards


def main():
    print('forest:0,sword:1,rune:2,dragon:3,shadow:4,blood:5,haven:6,portal:7')
    craft_num = int(input('input craft number>>> '))
    card_pool = get_card_pool(craft_num)
    card_scores = dl_card_scores(craft_num)

    while True:
        screen = sv_screenshot()
        trim_screens = get_trim_screens(screen)
        present_cards = get_present_cards(trim_screens, card_pool)
        left, right = 0, 0
        for i, present_card in enumerate(present_cards):
            try:
                card_score = card_scores[present_card['card_name']]
            except KeyError:
                card_score = 0
            print(present_card['card_name'], card_score)
            if i < 2:
                left += card_score
            else:
                right += card_score
        if right > left:
            print('Choice right')
        elif right < left:
            print('Choice left')
        else:
            print('Choice free')
        print(left, right)


if __name__ == '__main__':
    main()
