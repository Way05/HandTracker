import cv2
import threading
import time
import math
import HandTrackingModule as htm
import pyqtg as pqtg

cap = cv2.VideoCapture(0)

detector = htm.handDetector()

stopEvent = threading.Event()

graph = pqtg.Graph()


def runGraph(graph):
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

    # map dist from 0-xxx to 0-10
    dist = (dist - 0) * (10 - 0) / (300 - 0)
    return dist


def runOpenCV(event, graph):
    prevTime = 0
    currTime = 0
    while not event.is_set():
        _success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            scalar = calcDist(lmList)
            graph.updateScalar(scalar)

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
