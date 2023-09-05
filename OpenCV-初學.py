import cv2
import numpy as np


def show(img):
    cv2.imshow('oxox',img)
    cv2.waitKey(0)

# img=cv2.imread("4.jpg")

# #重新制定圖片大小
# img=cv2.resize(img,(500,500))

# #倍數放大
# img=cv2.resize(img,(0,0),fx=2,fy=3)

# cv2.imshow('img',img)
# cv2.waitKey(0)

#讀取影片
# cap=cv2.VideoCapture('2.mp4')

#回傳有沒有抓取成功 是一個布林值 ret
#fram抓取的每一偵圖片
# ret, frame=cap.read()
# if ret:
#     cv2.imshow("xoxo",frame)
# cv2.waitKey(0)

#改用影片的模式撥放 使用迴圈
# while True:
#     ret, frame=cap.read()
#     frame=cv2.resize(frame,(500,400)) #透過改變每一偵圖片大小來達到修改影片大小的目的
#     if ret:
#         cv2.imshow("xoxo",frame)
#     else:
#         break #取不到下一偵就跳出迴圈
#     cv2.waitKey(50)

# #取得攝像鏡頭畫面
# #攝像頭預設編號為0
# cap=cv2.VideoCapture(0) 

# while True:
#     ret, frame=cap.read()
#     if ret:
#         cv2.imshow("xoxo",frame)
#     else:
#         break #取不到下一偵就跳出迴圈
    
#     #按下q鍵退出
#     if cv2.waitKey(1)==ord("q"):
#         break

img=cv2.imread("4.jpg")
img20=cv2.imread("1.jpg")

#印出img的維度大小
# print(img.shape)

#創造圖片的概念
# img1=np.empty((300,300,3),np.uint8)

# for row in range(300):
#     for col in range(300):
#         img1[row][col]=[255,0,0]

#切割圖片
#以圖片左上角為原點
# new_4=img[100:332,200:500]

#轉換灰階圖片
img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img20=cv2.resize(img20,(0,0),fx=0.3,fy=0.3)
#高斯模糊圖片
blur=cv2.GaussianBlur(img20,(7,7),10)
#平均值模糊法(計算範圍內的色彩值平均)
mean_blur=cv2.blur(img20,(20,20))
#中值模糊法將處理範圍內的色彩做排序 取順序在中間的
central=cv2.medianBlur(img20,35)
# cv2.imshow("ff",blur)
# cv2.imshow("fa",mean_blur)
# cv2.imshow('aa',central)
# cv2.waitKey(0)



#canny邊緣檢測
#利用跟周圍象數點的差異來打分數 低於100的全部過濾掉  高於200的全部保留
canny=cv2.Canny(img,300,500)

#dilate膨脹(把邊緣線條做膨脹色彩值高的會侵蝕低的)
dilate=cv2.dilate(img, np.ones((0,0)))

#erode侵蝕(色彩值低的會侵蝕高的)
erode=cv2.erode(img,np.ones((10,10)))
canny_e=cv2.erode(canny,np.ones((15,10)),iterations=1)
canny_d=cv2.dilate(canny_e,np.ones((15,10)),iterations=1)
# canny_e=cv2.erode(canny_d,np.ones((15,10)),iterations=1)
# cv2.imshow("ll",canny_e)
# cv2.imshow("dd",canny_d)
# cv2.imshow("de",canny)
# cv2.waitKey(0)


#圖片等比例縮放
# img
# w=300
# h=int(img.shape[0]/img.shape[1]/w)
# img2=cv2.resize(img, (200,400))
# cv2.imshow('oxox',img)
# cv2.imshow('sda',img2)


#翻轉圖片 1,0,-1
img_flip=cv2.flip(img,1)

#旋轉圖片                                       #旋轉中心  旋轉角度 縮放比率  輸出的圖像大小
img_rotation=cv2.warpAffine(img, cv2.getRotationMatrix2D((500,250), 90, 0.2), (800,450))

#圖片的複製貼上
    #底圖要貼上的位置 大小要跟要貼上的圖片一致
# img[100:400,200:700]=img20[600:900,300:800]
#浮水印 第三個參數 間隔取值
# img[100:400,200:700:3]=img20[600:900,300:800:3]

# print(img20.shape)

#取bgr三種亮度
img19=img[:,:,2]


#白平衡
# m2=img.copy()
# avg=img[:,:,0].mean()+img[:,:,1].mean()+img[:,:,2].mean()
# m2[:,:,0]=cv2.multiply(img[:,:,0],(avg/(img[:,:,0].mean()*3)))
# m2[:,:,1]=cv2.multiply(img[:,:,1],(avg/(img[:,:,1].mean()*3)))
# m2[:,:,2]=cv2.multiply(img[:,:,2],(avg/(img[:,:,2].mean()*3)))

# cv2.imshow("bb",img)
# cv2.imshow("kk",m2)
# cv2.waitKey(0)


#影像二值化
# m3=img.copy()
# th , m3[:,:,0]=cv2.threshold(img[:,:,0], 50, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
# print(th)
# th , m3[:,:,1]=cv2.threshold(img[:,:,1], 50, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
# print(th)
# th , m3[:,:,2]=cv2.threshold(img[:,:,2], 50, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
# print(th)

# cv2.imshow("nn",img)
# cv2.imshow("ff",m3)
# cv2.waitKey(0)


#圖片輪廓檢測

# img_s=cv2.imread("555.jpg")
# img_s=cv2.resize(img_s,(0,0),fx=0.2,fy=0.2)
# img_contour=img_s.copy()
# # img_s=cv2.cvtColor(img_s,cv2.COLOR_BGR2GRAY)
# blank=np.full((362,512,3),(255,255,255),np.uint8)
# #先用大的門檻值檢測邊緣再用小的門檻值將檢測出來的結果線條連起來
# # canny2=cv2.Canny(img_s,200,150)
# canny2=cv2.inRange(img_s,(0,0,0),(220,220,255))

# contours, hierarchy=cv2.findContours(canny2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# # for cnt in contours:
# cv2.drawContours(blank, contours, -1, (0,0,0),1)

#     #框輪廓點
#     # peri=cv2.arcLength(contours,True)
#     # vertices=cv2.approxPolyDP(contours,peri*0.2,True)
# x, y, w, h =cv2.boundingRect(contours[4])
# cv2.rectangle(img_s, (x,y), (x+w,y+h), (0,0,255),3)

# cv2.imshow("ll",img_s)
# cv2.imshow("kk",canny2)
# cv2.imshow('rr',blank)
# cv2.waitKey(0)
# print(img_s.shape)

#圖片顏色偵測
image=cv2.imread("22231.png")
image=cv2.resize(image,(0,0),fx=0.3,fy=0.3)


def empty():
    pass
#動態控制條
#創建視窗
cv2.namedWindow("tracker")
cv2.resizeWindow("tracker",763,504)

#控制條HSV有三個值
cv2.createTrackbar("HueMin","tracker",0,179,empty)
cv2.createTrackbar("HueMax","tracker",179,179,empty)
cv2.createTrackbar("SatMin","tracker",0,255,empty)
cv2.createTrackbar("SatMax","tracker",255,255,empty)
cv2.createTrackbar("ValMin","tracker",0,255,empty)
cv2.createTrackbar("ValMax","tracker",255,255,empty)



#轉換顏色成hsv
hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

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
    
    mask=cv2.inRange(hsv,lower,upper)
    result=cv2.bitwise_and(image,image,mask=mask)
    cv2.imshow("gg",hsv)
    cv2.imshow('ss',image)
    cv2.imshow("gk",mask)
    cv2.imshow("re",result)
    cv2.waitKey(1)


# #輪廓檢測
# data=cv2.imread("download.png")
# data2=data.copy()
# #轉灰階圖片
# # data=cv2.cvtColor(data,cv2.COLOR_BGR2GRAY)
# # canny2=cv2.Canny(data,150,200)
# #另一種找邊界方法
# canny2=cv2.inRange(data,(220,220,220),(255,255,255))
# contours, hierarchy=cv2.findContours(canny2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
# # cv2.drawContours(data2,contours,-1,(0,0,255),3)
# for cnt in contours:
#     print(cv2.contourArea(cnt))
#     peri=cv2.arcLength(cnt,True)
#     vertices=cv2.approxPolyDP(cnt,peri*0.02,True)
#     corner=len(vertices)
#     x, y, w, h=cv2.boundingRect(vertices)
#     cv2.rectangle(data2,(x,y),(x+w,y+h),(0,255,0),2)
#     if corner==3:
#         cv2.putText(data2,"triangle",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
#     if corner==8:
#         cv2.putText(data2,"circle",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
#     if corner==4:
#         cv2.putText(data2,"retangle",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

# show(data2)









