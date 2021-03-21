import cv2   #importing the libraries
import numpy as np

import time # to provide camera some time to capture the background


#if you have only one default webcam, use 0, that number depends on how many webcams you have
cap = cv2.VideoCapture(0)

time.sleep(2) # here we have provided 2 second for camera to adjust itself

background = 0 #this will be the background image which will get displayed when you have claok around


#Capture the background
for i in range(60):   # creating for loop for the camera to capture the background image perfectly

    ret,background = cap.read()   # this will return 2 values, one is image captured and second is return value - True

#This code will be running till the webcam is capturing the image
while(cap.isOpened()):   # it means it will keep running until capture object is opened.

    ret, img = cap.read()   # capturing an image to perform an operation on it

    if not ret:   # if object is not getting capture, break the loop
        break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # converting our img from BGR to HSV (Hue, Saturation, Value)

    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2

    ## Open and Dilate the mask image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    ## Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)

    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res1 = cv2.bitwise_and(background, background, mask=mask1)

    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    #out.write(finalOutput)
    cv2.imshow("magic", finalOutput)
    k = cv2.waitKey(10)
    if k == 27:
        break


cap.release()
    #out.release()
cv2.destroyAllWindows()






