import cv2
import numpy as np

#讀取影片
cap=cv2.VideoCapture('h3.mp4')

# 回傳有沒有抓取成功 是一個布林值 ret
# fram抓取的每一偵圖片
# 改用影片的模式撥放 使用迴圈
while True:
    ret, frame=cap.read()
    frame2=frame.copy()
    # frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # frame2=cv2.cvtColor(frame2, cv2.COLOR_GRAY2BGR)
    # hsv=cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
    lower=np.array([54,0,0])
    upper=np.array([187,101,64])
    frame2=cv2.inRange(frame2,lower,upper)
    frame2=cv2.dilate(frame2,np.ones((7,7)))
    # frame2=cv2.erode(frame2,np.ones((7,7)))
    
    contours, hierarchy=cv2.findContours(frame2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        # print(cv2.contourArea(cnt))
        peri=cv2.arcLength(cnt,True)
        vertices=cv2.approxPolyDP(cnt,peri*0.02,True)
        corner=len(vertices)
        x, y, w, h=cv2.boundingRect(vertices)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    

    
    if ret:
        cv2.imshow("xoxo",frame)
    else:
        break #取不到下一偵就跳出迴圈
    cv2.waitKey(50)


#使用hsv的作法
    # while True:
    # ret, frame=cap.read()
    # frame2=frame.copy()
    # hsv=cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
    # lower=np.array([98,0,44])
    # upper=np.array([179,255,232])
    # frame3=cv2.inRange(hsv,lower,upper)
    
    # contours, hierarchy=cv2.findContours(frame3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    # for cnt in contours:
    #     # print(cv2.contourArea(cnt))
    #     peri=cv2.arcLength(cnt,True)
    #     vertices=cv2.approxPolyDP(cnt,peri*0.02,True)
    #     corner=len(vertices)
    #     x, y, w, h=cv2.boundingRect(vertices)
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    
    
    
    
    
    # if ret:
    #     cv2.imshow("xoxo",frame)
    # else:
    #     break #取不到下一偵就跳出迴圈
    # cv2.waitKey(50)