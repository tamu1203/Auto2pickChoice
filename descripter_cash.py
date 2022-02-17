from present_cards import get_descriptor, get_img
from glob import glob
from tqdm import tqdm
import cv2
import pickle
import os

img_paths = glob('pictures\\card_imgs\\C_'+'*')
card_pool_img = get_img(img_paths)
d = {}
if not os.path.isdir('pickle'):
    os.makedirs('pickle')
for card_id, card_img in tqdm(card_pool_img.items()):
    d[card_id] = get_descriptor(card_img)
pickle.dump(d, open('pickle\\descripter.pickle', mode='wb'))
