import cv2
import threading
import time
import math
import pyqtgraph as pg
import HandTrackingModule as htm
import pyqtg as pqtg

cap = cv2.VideoCapture(0)

detector = htm.handDetector()

stopEvent = threading.Event()


def runGraph():
    graph = pqtg.Graph()
    graph.start_anim()


def calcDist(dataPoints):
    lm1 = dataPoints[4]
    lm1_pos = (lm1[1], lm1[2])
    lm2 = dataPoints[8]
    lm2_pos = (lm2[1], lm2[2])
    dist = math.sqrt(((lm1_pos[1] - lm2_pos[1]) ** 2 + (lm1_pos[0] - lm2_pos[0]) ** 2))
    minThreshold = 20
    if dist <= minThreshold:
        dist = 0
    # print(dist)


def runOpenCV():
    global lmList
    prevTime = 0
    currTime = 0
    while True:
        _success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            calcDist(lmList)

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(
            img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3
        )

        cv2.imshow("Image", img)
        cv2.waitKey(1)


t1 = threading.Thread(target=runGraph)
t2 = threading.Thread(target=runOpenCV)

t1.start()
t2.start()

try:
    while not stopEvent.set():
        time.sleep(0.1)
except KeyboardInterrupt:
    stopEvent.set()

t1.join()
t2.join()
