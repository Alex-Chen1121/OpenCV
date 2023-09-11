import cv2
import numpy as np
import math

# 1.定義物體追蹤方式
class EuclideanDistTracker:
  def __init__(self):
    # 儲存物體中心點座標
    self.center_points = {}
    # 累積計算物體id
    # 每次新偵測到物體id+1
    self.id_count = 0

  def update(self, object_rect):
    # 物體框框及id
    objects_bbs_ids = []

    # 取得物體中心座標
    for rect in object_rect:
      x,y,w,h = rect
      cx = (x+x+w)//2 # 整除
      cy = (y+y+h)//2

    # 確認此物體是否已存在 或是新偵測到
      same_object_detected = False
      for id, pt in self.center_points.items():
        # 歐式距離 hypot計算三角形斜邊距離
        dist = math.hypot(cx-pt[0], cy-pt[1])
        if dist<25:
          self.center_points[id] = (cx,cy)
          print(self.center_points)
          objects_bbs_ids.append([x,y,w,h,id])
          same_object_detected = True
          break
      if same_object_detected is False:
        self.center_points[self.id_count] =(cx, cy)
        objects_bbs_ids.append([x,y,w,h,self.id_count])
        self.id_count += 1

    new_center_points = {}
    for obj_bb_id in objects_bbs_ids:
      _,_,_,_, object_id = obj_bb_id
      center = self.center_points[object_id]
      new_center_points[object_id] = center

    # 更新id字典
    self.center_points = new_center_points.copy()
    return objects_bbs_ids

# 2.影片中偵測物體
# 創建追蹤物件
track = EuclideanDistTracker()

# 載入影片
cap = cv2.VideoCapture("71.mp4")

# 背景靜止呈現黑色 動態物體呈現白色
object_detector = cv2.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    shape = frame.shape
    # print(shape) (442, 788, 3)

    # 截出指定偵測區域
    roi = frame[250:440,350:770]
    
    # 1.物件偵測
    # 套用遮罩
    mask = object_detector.apply(roi)

    # 影像二值化 過濾雜訊
    mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones([7,7])
    mask = cv2.dilate(mask, kernel)
    mask = cv2.erode(mask, kernel)
    # 找出物體邊緣
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    detection = []
    for cnt in contours:
        # 計算邊緣面積 來找出物體
        area = cv2.contourArea(cnt)
        # 過濾體積過小的物體
        if area>1500:
            # cv2.drawContours(roi, [cnt], -1, (0,255,0),2)
            x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(roi, (x,y), (x+w,y+h), (0,255,0),3)
            detection.append([x,y,w,h])
            
    
    # 2.物件追蹤
    boxer_ids = track.update(detection)
    print(boxer_ids)
    for box_id in boxer_ids:
        x,y,w,h, id = box_id
        cv2.putText(roi, "obj"+str(id), (x,y-15), cv2.FONT_ITALIC, 0.7,(0,0,255),2)
        cv2.rectangle(roi, (x,y), (x+w,y+h), (0,255,0),3)
        # print(box_id)
    # print(detection)
    cv2.imshow("area",roi)
    cv2.imshow("monitor",frame)
    # cv2.imshow("mask",mask)
    key = cv2.waitKey(30)
    if key ==27: # esc鍵退出
        break
cap.release()
cv2.destroyAllWindows()