import cv2

img1 = cv2.imread('pictures/type/follower.png')
img1 = img1[170:560, 110:420]
img2 = cv2.imread('pictures/type/amulet.png')
img2 = img2[169:561, 112:422]
img3 = cv2.imread('pictures/type/spell.png')
img3 = img3[169:561, 112:422]

cv2.imwrite('follower_sample.jpg', img1)
cv2.imwrite('amulet_sample.jpg', img2)
cv2.imwrite('spell_sample.jpg', img3)

