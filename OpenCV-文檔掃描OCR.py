import numpy as np
import cv2
'''
第一步:邊緣檢測
第二步:獲取輪廓
第三步:變換操作

'''
def resize(img,width=None,height=None,inter=cv2.INTER_AREA):
    dim = None
    (h,w) = img.shape[0:2]
    
    if width is None and height is None:
        return img
    
    if width is None:
        r = height/float(h)
        dim = (int(w*r), height)
    else:
        r = width/float(w)
        dim = (width, int(h*r))
    
    resize = cv2.resize(img, dim ,interpolation=inter)
    return resize

def order_points(pts):
    rect = np.zeros((4,2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_points_transform(img, pts):
    rect = order_points(pts)
    (tl,tr,br,bl) = rect

    widthA = np.sqrt(((br[0]-bl[0])**2) + ((br[1]-bl[1])**2))
    widthB = np.sqrt(((tr[0]-tl[0])**2) + ((tr[1]-tl[1])**2))
    maxWidth = max(int(widthA),int(widthB))

    heightA = np.sqrt(((tl[0]-bl[0])**2) + ((tl[1]-bl[1])**2))
    heightB = np.sqrt(((tr[0]-br[0])**2) + ((tr[1]-br[1])**2))
    maxHeight = max(int(heightA),int(heightB))

    dst = np.array([
        [0,0],
        [maxWidth-1,0],
        [maxWidth-1,maxHeight-1],
        [0,maxHeight-1]], 
        dtype="float32"
    )

    M = cv2.getPerspectiveTransform(rect, dst) # 傳入參數:1.輸入角點座標 2.輸出角點座標
    warped = cv2.warpPerspective(img, M, (maxWidth,maxHeight))
    
    return warped




img = cv2.imread("receipt.jpg")      # 讀取圖片
ratio = img.shape[0]/500        # 設置原圖比例
orig = img.copy()               # 複製原圖

img = resize(orig, height=500)

# 基礎操作
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
edge = cv2.Canny(gray, 75,200)

xx = np.ones((3,3))
edge = cv2.dilate(edge, kernel=xx)

# 檢測輪廓
cnts = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
cnts = sorted(cnts, key=lambda a : cv2.contourArea(a), reverse=True)[:5] # 針對輪廓排序
cv2.drawContours(gray, cnts, -1, (0,255,0), 3) # -1代表輪廓全畫

# 遍歷輪廓 找出最外的輪廓
for c in cnts:
    peri = cv2.arcLength(c, True)                 # 計算輪廓周長
    approx = cv2.approxPolyDP(c, 0.02*peri, True) # 輸出頂點
    if len(approx) == 4:    # 只選擇矩形輪廓
        screenCnt = approx
        break
# print(approx)

# 透視變換
warped = four_points_transform(orig, screenCnt.reshape(4,2)*ratio)
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(warped, 100, 255, cv2.THRESH_BINARY)[1] 
cv2.imwrite("scanded.jpg",ref)
# print(cnt)
# cc = np.array(edge)
# bb = np.array(gray)
# aa = np.hstack((cc,bb))

cv2.imshow("xx",resize(ref, height=650))
cv2.imshow("oo",resize(img, height=650))
# cv2.imshow("ox",cv2.resize(edge,(0,0),fx=0.3,fy=0.3))
cv2.waitKey(0)
cv2.destroyAllWindows()