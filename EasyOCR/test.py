import cv2

a = cv2.imread('D:/dr_img_backup/dr_2022-06-20_183326.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('test', a)

cv2.waitKey(0)
cv2.destroyAllWindows()