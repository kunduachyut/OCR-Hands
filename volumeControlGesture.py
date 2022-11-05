############################################################
import cv2
import time
import numpy as np
import Module.handModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
############################################################

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
previous = 0

detector = htm.handDetector(contradictionCon=.7)
#######################PYCAW############################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
#######################END##############################
minVolume = volRange[0]
maxVolume = volRange[1]

vol = 0
volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cordx, cordy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img,(x1,y1),3,(0, 255, 255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 3, (0, 255, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0, 255, 0),2)
        cv2.circle(img, (cordx, cordy), 5, (0, 255, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        vol = np.interp(length, [50, 300], [minVolume, maxVolume])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

    current = time.time()
    fps = 1 / (current - previous)
    previous = current
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()