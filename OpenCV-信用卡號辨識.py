import cv2
import numpy as np

def cvshow(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread("creditcard-photo/numfont.png")
ref = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
ref = cv2.threshold(ref,50,255,cv2.THRESH_BINARY)[1]
cnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

box = [cv2.boundingRect(c) for c in cnts]
k = 0
# for i in box:
#     # area = cv2.contourArea(i)
#     # print(area)
#     x,y,w,h = i
#     if w<30 or w>100:
#         pass
#     else:
#         print(k)
#     k+=1
for k in [0,2,3,4,4,6]:
    del box[k]
# x,y,w,h = box[2]
# num_4 =box[0] 
# num_0 =box[1]
# num_9 =box[2]
def takefirst(elem):
    return elem[0]
box.sort(key=takefirst)
# print(box)

digits = {}
for i in range(len(box)):
    x,y,w,h =box[i]
    roi = img[box[i][1]:box[i][1]+box[i][3],box[i][0]:box[i][0]+box[i][2]]
    digits[i+1] = roi

cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255),3)
# for o in box:
#     x,y,w,h = o
#     cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255),3)
# cvshow("img",img)
# print(digits[1].shape) # (63,37,3)
og_card = cv2.imread("creditcard-photo/20180708150254_47.jpg")
og_card = cv2.resize(og_card,(0,0),fx=0.6,fy=0.6)
card = cv2.cvtColor(og_card,cv2.COLOR_BGR2GRAY)
# cvshow("card",card)
_, result = cv2.threshold(card,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
# cvshow("card",result)
# tophat = cv2.morphologyEx(result, cv2.MORPH_CLOSE, (7,7))
kernel = np.ones([11,11])
tophat = cv2.dilate(result,kernel)
# cvshow("card",tophat)

cnts2, hierarchy2 = cv2.findContours(tophat.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# print(cnts2)
cur_image = og_card.copy()
cv2.drawContours(cur_image,cnts2,-1,(0,255,0),2)
card_box = [cv2.boundingRect(c) for c in cnts2]
x,y,w,h = card_box[8]
cv2.rectangle(og_card,(x,y),(x+w,y+h),(0,255,0),2)
# cvshow("card",og_card)
# print(card_box[8][2]/card_box[8][3])
# print(card_box[7][2]/card_box[7][3])
p = 0
card_digits = {}
for i in range(len(card_box)):
    x,y,w,h = card_box[i]
    if card_box[i][2]/card_box[i][3]<2.5 and card_box[i][2]/card_box[i][3]>2.3:
        x,y,w,h = card_box[i]
        cv2.rectangle(og_card.copy(),(x,y),(x+w,y+h),(0,255,0),2)
        rbi = og_card[y-5:y+h+5,x-5:x+w+5]
        card_digits[p+1] = rbi
        p+=1
    else:
        pass
# print(card_digits)
# cvshow("card",og_card)
# cvshow("card_num",card_digits[3])
# print(card_digits[4].shape) #(47,98,3)

group_num = card_digits[2]
group_num = cv2.cvtColor(group_num,cv2.COLOR_BGR2GRAY)
group_num = cv2.threshold(group_num,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
cnts3 = cv2.findContours(group_num.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
cur = card_digits[2].copy()
next = card_digits[2].copy()
cv2.drawContours(cur,cnts3,-1,(0,0,255),2)
box3 = [cv2.boundingRect(c) for c in cnts3]
box3.sort(key=takefirst)
op = 1
final = {}
for u in box3:
    x,y,w,h = u
    cv2.rectangle(next,(x,y),(x+w,y+h),(0,0,255),2)
    rou = card_digits[2][y:y+h,x:x+w]
    rou = cv2.resize(rou,(37,63))
    final[op] = rou
    op+=1

cvshow("group_num",next)
# # cvshow("group_num",next)
# # cvshow("final",final[4])
# # cvshow("dinal",digits[5])


# # print(digits.keys())
# group_out_put = []

# for j in range(len(final)):
#     scores = []
#     kk =final[j+1] 
#     for k, v in digits.items():
#         result = cv2.matchTemplate(kk,v,cv2.TM_CCOEFF)
#         (_,score,_,_) = cv2.minMaxLoc(result)
#         scores.append(abs(score))
#     group_out_put.append(str(np.argmax(scores)+1))

# card_number = ""
# card_number = card_number.join(group_out_put)
# print(group_out_put)
# print("卡號:",card_number)
# cvshow("final",final[3])