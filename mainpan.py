import os

import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# ‪C:\Program Files\Tesseract-OCR\tesseract.exe

per = 25
roi = [[(278, 234), (490, 280), 'text', 'pan_no'],
       [(54, 332), (298, 360), 'text', 'Name'],
       [(48, 406), (404, 434), 'text', 'fathers_name'],
       [(46, 498), (180, 524), 'text', 'DOB']]

imgQ = cv2.imread('C:\\Users\\Nitish\\PycharmProjects\\scandocs\\venv\\img2.PNG')
h, w, c = imgQ.shape
imgQ = cv2.resize(imgQ, (w // 1, h // 1))

orb = cv2.ORB_create(8000)
kp1, des1 = orb.detectAndCompute(imgQ, None)
imkp1 = cv2.drawKeypoints(imgQ, kp1, None)

path = 'C:\\Users\\Nitish\\PycharmProjects\\scandocs\\UserFormpan'
myPicList = os.listdir(path)
print(myPicList)
for j, y in enumerate(myPicList):
    img = cv2.imread(path + "/" + y)
    # cv2.imshow(y,img)
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des2, des1)
    matches = sorted(matches, key=lambda x: x.distance)
    good = matches[:int(len(matches) * (per / 100))]
    imgMatch = cv2.drawMatches(img, kp2, imgQ, kp1, good[:100], None, flags=2)
    imgMatch = cv2.resize(imgMatch, (w // 3, h // 3))
    # cv2.imshow(y,imgMatch)

    ###Resizing#################

    srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
    imgScan = cv2.warpPerspective(img, M, (w, h))

    # cv2.imshow(y, imgScan)

    imgShow = imgScan.copy()
    imgMask = np.zeros_like(imgShow)

    myData = []
    print(f'Extracting data from PAN Card')

    for x, r in enumerate(roi):

        cv2.rectangle(imgMask, ((r[0][0]), r[0][1]), ((r[1][0]), r[1][1]), (0, 0, 255), cv2.FILLED)
        # imgShow = cv2.addWeighted(imgShow,0.99,imgMask,0.1  ,0)

        imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        imgShow = cv2.resize(imgQ, (w // 3, h // 3))
        #      cv2.imshow(y+ "2",imgShow)

        # cv2.imshow(str(x), imgCrop)

        if r[2] == 'text':
            print('{} :{}'.format(r[3], pytesseract.image_to_string(imgCrop)))

            myData.append(pytesseract.image_to_string(imgCrop))

    with open('dataop.csv', 'a+') as f:
        for data in myData:
            f.write((str(data) + ','))
        f.write('\n')

        imgShow = cv2.resize(imgShow, (w // 1, h // 1))
#   cv2.imshow(y, imgShow)


# cv2.imshow("KeyPointsQuery",imkp1)
# cv2.imshow("Output",imgQ)
cv2.waitKey(0)
