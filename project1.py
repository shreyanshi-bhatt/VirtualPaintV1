# Paint with Markers

import cv2
import numpy as np

# For using Web Cam
cam = cv2.VideoCapture(0)  # 0 means the 1st web cam is selected
cam.set(3, 640)  # 3 is for width
cam.set(4, 480)  # 4 is for height
cam.set(10, 150)  # to set full brightness

myColors = [[5, 107, 0, 19, 255, 255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255]]

myColorValues = [[51, 153, 255], [255, 0, 255], [0, 255, 0]]  # BGR codes for orange, purple and green

myPoints = []  # x, y, colorID


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return newPoints


def getContours(img):
    global objType
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)  # for the outer corner contours
    x, y, width, height = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, width, height = cv2.boundingRect(approx)
    return x + width // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, image_frame = cam.read()
    if not success:
        print("Failed to read from camera")
        break
    imgResult = image_frame.copy()
    newPoints = findColor(image_frame, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
