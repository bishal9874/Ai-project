
import cv2
import time
import os
import mediapipe as mp
import HandtrackingModule as htm

wcam,hcam= 680,420

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)


folderpath = "fingers"

mylist=os.listdir(folderpath)
print(mylist)
overlaylist = []


#detector

detector = htm.handDetector(detectionCon=0.75)

tipIds= [4,8,12,16,20]


for impth in mylist:
    image = cv2.imread(f'{folderpath}/{impth}')
    overlaylist.append(image)
# print(len(overlaylist))
pTime= 0
while True:

    success,img = cap.read()
    img = detector.findHands(img,draw=True)
    lmlist = detector.findPosition(img,draw=False)
    #print(lmlist)
    
    if len(lmlist) != 0:
        fingers= []
        #thumb
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0]-1][1]:
                
            fingers.append(1)
        else: 
            fingers.append(0)
        # 4 fingers
        for id in  range(1,5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                
                fingers.append(1)
            else: 
                fingers.append(0)
        # print(fingers)

         #total  fingers
        totalfinger = fingers.count(1)
        print(totalfinger)

        h,w,c = overlaylist[totalfinger-1].shape
        img[0:h,0:w] = overlaylist[totalfinger-1]

        cv2.rectangle(img, (20, 225), (170, 425), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(totalfinger), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Image" , img)
    cv2.waitKey(1)