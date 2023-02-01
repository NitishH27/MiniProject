import cv2
import numpy as np
import pytesseract
import os


pytesseract.pytesseract.tesseract_cmd = '‪C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#‪C:\Program Files\Tesseract-OCR\tesseract.exe

per = 25



imgQ=cv2.imread('adhar.JPG')
h,w,c= imgQ.shape
#imgQ=cv2.resize(imgQ,(w//3,h//3))

orb = cv2.ORB_create(8000)
kp1, des1 = orb.detectAndCompute(imgQ,None)
#imkp1 = cv2.drawKeypoints(imgQ,kp1,None)

path='C:\\Users\\Nitish\\PycharmProjects\\scandocs\\UserForms'
myPicList = os.listdir(path)
print(myPicList)
for j,y in enumerate(myPicList):
    img = cv2.imread(path + "/" +y)
    cv2.imshow(y,img)
    kp2,des2 = orb.detectAndCompute(img,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des2,des1)
    matches = sorted(matches, key=lambda x: x.distance)
    good = matches[:int(len(matches)*(per/100))]
    imgMatch = cv2.drawMatches(img,kp2,imgQ,kp1,good[:100],None,flags=2)
    #cv2.imshow(y,imgMatch)

###Resizing#################

   # srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
   # dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1,1,2)

   # M, _ = cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
    #imgScan = cv2.warpPerspective(img,M,(w,h))
    #imgScan = cv2.resize(imgQ, (w // 3, h // 3))
    #cv2.imshow(y, imgScan)





#cv2.imshow("KeyPointsQuery",imkp1)
cv2.imshow("Output",imgQ)
cv2.waitKey(0)