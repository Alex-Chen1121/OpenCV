import cv2
import mediapipe as mp
import random
import time

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands                    # mediapipe 偵測手掌方法

ptime = 0  # 計算運行起始時間
score = 0  # 計算方框變位次數


cap = cv2.VideoCapture(0)
# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    # max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    touched = True
    
    while True:
        ret, img = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
        results = hands.process(img2)                 # 偵測手掌
        
        imgheight = img.shape[0]
        imgwidth = img.shape[1]
        
        if touched: # 以物件狀態為條件
            touched = False    # 如果沒碰到 就保持flase
            rx = random.randint(50,imgwidth-50)    # 隨機 x 座標
            ry = random.randint(50,imgheight-100)   # 隨機 y 座標
            score+=1
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                x = hand_landmarks.landmark[7].x * imgwidth
                y = hand_landmarks.landmark[7].y * imgheight
                
                if x>rx and x<(rx+80) and y>ry and y<(ry+80):
                    run = True
                
                # 將節點和骨架繪製到影像中
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                    )
                
                # 繪製手指節點編號
                for i, lm in enumerate(hand_landmarks.landmark):
                    xpos = int(lm.x * imgwidth)
                    ypos = int(lm.y * imgheight)
                    cv2.putText(img, str(i), (xpos-25, ypos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 2)
        
        # 計算fps
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        
        # fps及score顯示
        cv2.putText(img, f"FPS:{int(fps)}", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
        cv2.putText(img, f"SCORE:{int(score)}", (30,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
        cv2.rectangle(img,(rx,ry),(rx+80,ry+80),(0,0,255),5)
        
        cv2.imshow('window', img)
        if cv2.waitKey(5) == ord('q'):
            break    # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()