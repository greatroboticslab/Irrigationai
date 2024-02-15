#This program reads in camera frames and writes it to Data/<folder_name>
#as well as creating a .csv for soil moisture for that frame.

import time
import cv2
from pathlib import Path

#Webcam
cam = cv2.VideoCapture(0)

#How many frames to capture per second
FPS = 2

folderName = input("Please enter the name of this recording's file: ")

#Create the recording folder if it does not exist

Path("Data/"+folderName).mkdir(parents=True, exist_ok=True)


lastTime = time.time()
curTime = time.time()

#Seconds since last frame
deltaTime = 0.0

#Main recording loop
while(True):

	#Record frame
	ret, frame = cam.read()

	#Get current time
	curTime = time.time()
	deltaTime += curTime-lastTime
	lastTime = time.time()
	
	#Save Frame
	if deltaTime >= FPS:
		deltaTime = 0.0
		cv2.imshow('frame', frame)
		cv2.imwrite("Data/"+folderName+"/"+str(time.time())+".jpg", frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'): 
        	break

cam.release()
cv2.destroyAllWindows()
