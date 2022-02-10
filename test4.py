import cv2
import json
from glob import glob

pick_screen = cv2.imread('pictures/pick.jpg')
# エルフだった場合の処理
latest_pack = 123
craft_path = 'E/'
neutral_path = 'Ne/'
img_card_pool = {}

json_open = open('json_ja/all.json', 'r', encoding='utf-8')
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
        img_card_pool[img_path[-13:-5]] = img_card[170:560, 110:420]

# ベーシックカードをカードプールに追加
imgs_path = glob('pictures/cards/100/'+craft_path+'*') + \
    glob('pictures/cards/100/'+neutral_path+'*')
for img_path in imgs_path:
    img_card = cv2.imread(img_path)
    img_card_pool[img_path[-13:-4]] = img_card[170:560, 110:420]


# print(img_card_pool)
# exit()
for key, value in img_card_pool.items():
    result = cv2.matchTemplate(pick_screen, value, cv2.TM_CCORR_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal > 0.8:
        for card in cards:
            com = str(card['card_id'])
            if key == com:
                print(card['card_name'])
                cv2.imshow(key,value)
                cv2.waitKey(0)
        # tl = maxLoc[0], maxLoc[1]
        # br = maxLoc[0] + value.shape[1], maxLoc[1] + \
        #     value.shape[0]
        # dst = pick_screen.copy()
        # cv2.rectangle(dst, tl, br, color=(0, 255, 0), thickness=2)
        # cv2.imshow(key, dst)
        # cv2.waitKey(0)
