import cv2
import numpy as np


#圖片顏色偵測
image=cv2.imread("kobe.jpg")
image=cv2.resize(image,(0,0),fx=0.3,fy=0.3)


def empty():
    pass
#動態控制條
#創建視窗
cv2.namedWindow("tracker")
cv2.resizeWindow("tracker",763,504)

#控制條HSV有三個值
cv2.createTrackbar("HueMin","tracker",0,255,empty)
cv2.createTrackbar("HueMax","tracker",255,255,empty)
cv2.createTrackbar("SatMin","tracker",0,255,empty)
cv2.createTrackbar("SatMax","tracker",255,255,empty)
cv2.createTrackbar("ValMin","tracker",0,255,empty)
cv2.createTrackbar("ValMax","tracker",255,255,empty)



#轉換顏色成hsv
# hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

while True:
    h_min=cv2.getTrackbarPos("HueMin","tracker")
    h_max=cv2.getTrackbarPos("HueMax","tracker")
    s_min=cv2.getTrackbarPos("SatMin","tracker")
    s_max=cv2.getTrackbarPos("SatMax","tracker")
    v_min=cv2.getTrackbarPos("ValMin","tracker")
    v_max=cv2.getTrackbarPos("ValMax","tracker")
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    
    mask=cv2.inRange(image,lower,upper)
    result=cv2.bitwise_and(image,image,mask=mask)
    cv2.imshow("gg",image)
    cv2.imshow('ss',image)
    cv2.imshow("gk",mask)
    cv2.imshow("re",result)
    cv2.waitKey(1)