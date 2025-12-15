import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands  # type: ignore
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils  # type: ignore

prevTime = currTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLm in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    cv2.putText(
        img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3
    )

    cv2.imshow("Image", img)
    cv2.waitKey(1)
