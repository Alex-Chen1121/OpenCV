import cv2
import mediapipe as mp
from playsound import playsound
import numpy as np

face_mesh = mp.solutions.face_mesh.FaceMesh()

def EAR(landmarks):
    # np.linalg.norm() 算歐式距離的函式
    d1 = np.linalg.norm(landmarks[1]-landmarks[5])
    d2 = np.linalg.norm(landmarks[2]-landmarks[4])
    d3 = np.linalg.norm(landmarks[0]-landmarks[3])
    return (d1+d2)/d3*0.5

cap = cv2.VideoCapture(0)
sleep_frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret is False:
        break
    
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)
    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:
            right_eye_landmark_id = [362,385,387,263,373,380]
            left_eye_landmark_id = [33,160,158,133,153,144] 

            right_eye_landmark = []
            left_eye_landmark = []
            for id, landmark in enumerate(face.landmark):
                if id in  left_eye_landmark_id :
                    x = int(landmark.x*frame.shape[1])
                    y = int(landmark.y*frame.shape[0])
                    cv2.circle(frame, [x,y], 1, [0,255,0])
                    left_eye_landmark.append(np.array([x,y]))
                if  id in right_eye_landmark_id:
                    x = int(landmark.x*frame.shape[1])
                    y = int(landmark.y*frame.shape[0])
                    cv2.circle(frame, [x,y], 1, [0,255,0])
                    right_eye_landmark.append(np.array([x,y]))

            left_ear = EAR(left_eye_landmark)
            right_ear = EAR(right_eye_landmark)
            if (left_ear + right_ear)/2<0.85:
                sleep_frame_count+=1
            if sleep_frame_count>10:
                print("不要睡覺!") 
                sleep_frame_count = 0
    cv2.imshow("frame", frame)
    if cv2.waitKey(10) ==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
