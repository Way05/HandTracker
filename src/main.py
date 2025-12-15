import cv2
import threading
import time
import math
import HandTrackingModule as htm
import pyqtg as pqtg
from pyqtg import Graph

cap = cv2.VideoCapture(0)

detector = htm.handDetector()

stopEvent = threading.Event()

graph: Graph = pqtg.Graph()


def runGraph(graph: Graph):
    graph.start_anim()


def linearMapRange(value, oldMin, oldMax, newMin, newMax):
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin


# dist for index to thumb
def calcDist(dataPoints, hand=0):
    lm1 = dataPoints[4]
    lm1_pos = (lm1[1], lm1[2])
    lm2 = dataPoints[8]
    lm2_pos = (lm2[1], lm2[2])
    dist = math.sqrt(((lm1_pos[1] - lm2_pos[1]) ** 2 + (lm1_pos[0] - lm2_pos[0]) ** 2))
    minThreshold = 20
    if dist <= minThreshold:
        dist = 0
    return dist


def runOpenCV(event, graph: Graph):
    prevTime = 0
    currTime = 0
    while not event.is_set():
        _success, img = cap.read()

        img = detector.findHands(img)
        handList = detector.findPosition(img)

        if len(handList) != 0:
            L_scalar = calcDist(handList[0])
            L_scalar = linearMapRange(L_scalar, 0, 300, 0, 10)
            graph.updateScalar(L_scalar)
        if len(handList) > 1:
            R_scalar = calcDist(handList[1], hand=1)
            R_scalar = linearMapRange(R_scalar, 0, 300, 20, 70)
            graph.updateCameraZoom(R_scalar)

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(
            img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3
        )

        cv2.imshow("Image", img)
        cv2.waitKey(1)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Exiting...")
            event.set()
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Cleanup complete.")


t1 = threading.Thread(target=runOpenCV, args=[stopEvent, graph])

t1.start()

runGraph(graph)

t1.join()
