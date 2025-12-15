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
        lmList = []
        if self.results.multi_hand_landmarks:
            currHand = self.results.multi_hand_landmarks[hand]
            for id, lm in enumerate(currHand.landmark):
                h, w, _c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            if draw:
                cv2.circle(
                    img, (lmList[4][1], lmList[4][2]), 15, (255, 0, 0), cv2.FILLED
                )
                cv2.circle(
                    img, (lmList[8][1], lmList[8][2]), 15, (255, 0, 0), cv2.FILLED
                )
        return lmList


def main():
    cap = cv2.VideoCapture(0)
    prevTime = currTime = 0

    detector = handDetector()

    while True:
        _success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(
            img, str(int(fps)), (10, 10), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3
        )

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
