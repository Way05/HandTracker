import cv2
import mediapipe as mp
import time
import math
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
prevTime = currTime = 0

detector = htm.handDetector()

while True:
    _success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        lm1 = lmList[4]
        lm1_pos = (lm1[1], lm1[2])
        lm2 = lmList[8]
        lm2_pos = (lm2[1], lm2[2])
        dist = math.sqrt(
            ((lm1_pos[1] - lm2_pos[1]) ** 2 + (lm1_pos[0] - lm2_pos[0]) ** 2)
        )
    minThreshold = 20
    if dist <= minThreshold:
        dist = 0
    print(dist)

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    cv2.putText(
        img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3
    )

    cv2.imshow("Image", img)
    cv2.waitKey(1)
