import cv2
import mediapipe as mp
import time
from handModule import *

pTime = cTime = 0
cap = cv2.VideoCapture(0)
detector=handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) !=0:
        print(lmList[4])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

    cv2.imshow("image", img)
    cv2.waitKey(5)