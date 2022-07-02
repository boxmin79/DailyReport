import cv2

arrow = cv2.imread("../Icon/right_arrow.png", cv2.IMREAD_UNCHANGED)
print(arrow.shape)

flip_arrow = cv2.flip(arrow, 1) # 1은 좌우 반전, 0은 상하 반전입니다.

cv2.imshow('RightArrow', arrow)
cv2.imshow('FlipArrow', flip_arrow)

cv2.imwrite('../Icon/left_arrow.png', flip_arrow)
cv2.waitKey(0)
cv2.destroyAllWindows()