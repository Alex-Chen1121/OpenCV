import cv2
import numpy as np

imga = cv2.imread("testa.png") 
imga = cv2.resize(imga,(0,0),fx=0.5,fy=0.5)
imgb = cv2.imread("testb.png") 
imgb = cv2.resize(imgb,(400,502))

print(imga.shape)
print(imgb.shape)

diff = imga - imgb
# diff = cv2.absdiff(imga,imgb)
# diff_gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
# _, result = cv2.threshold(diff_gray,40,255,cv2.THRESH_BINARY)
# kernel = np.ones([3,3])
# result = cv2.dilate(result,kernel)
# cv2.imshow("a",imga)
# cv2.imshow("b",imgb)
# cv2.imshow("diff",result)
cv2.imshow("l",diff)
cv2.waitKey(0)