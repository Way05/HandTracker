import cv2
import mediapipe as mp
import time


class handDetector:
    def __init__(
        self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5
    ):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands  # type: ignore
        self.hands = self.mpHands.Hands(
            self.mode,
            self.maxHands,
            self.modelComplexity,
            self.detectionCon,
            self.trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils  # type: ignore

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLm, self.mpHands.HAND_CONNECTIONS
                    )

        return img

    def findPosition(self, img, hand=0, draw=True):
        handList = []
        color = ()
        handCount = 0
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                # currHand = self.results.multi_hand_landmarks[hand]
                handList.append([])
                for id, lm in enumerate(hand.landmark):
                    h, w, _c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    handList[handCount].append([id, cx, cy])
                handCount += 1

            if len(handList) == 2:
                handList.reverse()

            handCount = 0
            for hand in self.results.multi_hand_landmarks:
                if handCount == 0:
                    color = (255, 0, 0)
                elif handCount == 1:
                    color = (0, 255, 0)
                if draw:
                    cv2.circle(
                        img,
                        (handList[handCount][4][1], handList[handCount][4][2]),
                        15,
                        color,
                        cv2.FILLED,
                    )
                    cv2.circle(
                        img,
                        (handList[handCount][8][1], handList[handCount][8][2]),
                        15,
                        color,
                        cv2.FILLED,
                    )
                    cv2.line(
                        img,
                        (handList[handCount][4][1], handList[handCount][4][2]),
                        (handList[handCount][8][1], handList[handCount][8][2]),
                        (255, 255, 255),
                        1,
                    )
                handCount += 1
        return handList


def main():
    cap = cv2.VideoCapture(0)
    prevTime = currTime = 0

    detector = handDetector()

    while True:
        _success, img = cap.read()

        img = detector.findHands(img)
        _handList = detector.findPosition(img)

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(
            img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3
        )

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
