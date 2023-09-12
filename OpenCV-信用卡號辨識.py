import cv2
import numpy as np

# 圖片顯示
def cvshow(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 1.數字模板圖片處理
img = cv2.imread("creditcard-photo/numfont.png") # 讀入數字模板圖片
ref = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) # 轉灰階圖
ref = cv2.threshold(ref,50,255,cv2.THRESH_BINARY)[1] # 二值化
cnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 找出邊緣
boxs = [cv2.boundingRect(c) for c in cnts] # 儲存所有邊緣的框框

# 依序長寬比剔除掉不合適的邊框
# k = 0
# for box in boxs:
#     x,y,w,h = box
#     if w<30 or w>100:
#         pass
#     else:
#         print(k)
#     k+=1

# 從boxs中刪除不合適的邊框
for k in [0,2,3,4,4,6]:
    del boxs[k]

# 將數字邊框由左到右依序排列
# 取每個邊框的X座標
def takefirst(elem):
    return elem[0]

boxs.sort(key=takefirst) # 排序

# 擷取每個數字的圖片並存入digit字典中 以便做後續模板匹配
digits = {}
for i in range(len(boxs)):
    x,y,w,h =boxs[i]
    roi = img[boxs[i][1]:boxs[i][1]+boxs[i][3],boxs[i][0]:boxs[i][0]+boxs[i][2]]
    digits[i+1] = roi # dict_keys([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# digits[1].shape (63,37,3)
digits[0] = digits.pop(10)


# 2.信用卡圖片處理
og_card = cv2.imread("creditcard-photo/20180708150254_47.jpg")
og_card = cv2.resize(og_card,(0,0),fx=0.6,fy=0.6)
card = cv2.cvtColor(og_card,cv2.COLOR_BGR2GRAY)
result = cv2.threshold(card,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]

# 多形化處理
kernel = np.ones([11,11])
tophat = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)

# 找出所有的邊緣並變成邊框座標存入card_boxes
cnts2, hierarchy2 = cv2.findContours(tophat.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cur_image = og_card.copy()
cv2.drawContours(cur_image,cnts2,-1,(0,255,0),2)
card_boxes = [cv2.boundingRect(c) for c in cnts2]
card_boxes.sort(key=takefirst)

# 篩選邊框 並存進card_digits字典
p = 0
card_digits = {}
card = og_card.copy()
for i in range(len(card_boxes)):
    x,y,w,h = card_boxes[i]
    if card_boxes[i][2]/card_boxes[i][3]<2.9 and card_boxes[i][2]/card_boxes[i][3]>2.8:
        x,y,w,h = card_boxes[i]
        cv2.rectangle(card,(x,y),(x+w,y+h),(0,255,0),2)
        # cvshow("card",card)
        rbi = og_card[y-5:y+h+5,x-5:x+w+5]
        card_digits[p+1] = rbi
        p+=1
    else:
        pass

# 找出第一個方框的數字
group_out_put = []
for i in range(len(card_digits)):
    #找出方框中的數字
    group_num = card_digits[i+1]
    group_num = cv2.cvtColor(group_num,cv2.COLOR_BGR2GRAY)
    group_num = cv2.threshold(group_num,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    cnts3 = cv2.findContours(group_num.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    box3 = [cv2.boundingRect(c) for c in cnts3]
    box3.sort(key=takefirst)

    # 框出數字並將截圖存到final字典中
    count = 1
    final = {}
    temp = card_digits[i+1].copy()
    for num in box3:
        x,y,w,h = num
        cv2.rectangle(temp ,(x,y),(x+w,y+h),(0,0,255),2)
        rou = card_digits[i+1][y-2:y+h+2,x-2:x+w+2] # 邊緣加寬
        rou = cv2.resize(rou,(37,63)) # 跟數字模板一樣大小
        final[count] = rou
        count +=1


    # 進行模板匹配 將配對正確的數字放進group_out_put串列
    for j in range(len(final)):
        scores = []
        number =final[j+1] 
        for k, v in digits.items():
            
            result = cv2.matchTemplate(number,v,cv2.TM_CCOEFF)
            (_,score,_,_) = cv2.minMaxLoc(result)
            scores.append(abs(score))
        
        if int(np.argmax(scores))>8: # 第0~8位是數字1~9
            group_out_put.append(str(np.argmax(scores)-9))
        else:
            group_out_put.append(str(np.argmax(scores)+1))


# 卡號辨識結果
card_number = ""
card_number = card_number.join(group_out_put)
print("此張信用卡卡號:",card_number)