#This program reads in camera frames and writes it to Data/<folder_name>
#as well as creating a .csv for soil moisture for that frame.

import sys
import time
import cv2
from pathlib import Path

#Webcam
cam = cv2.VideoCapture("/dev/v4l/by-id/usb-H264_USB_Camera_H264_USB_Camera_2020032801-video-index0")

cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cam.set( cv2.CAP_PROP_FPS, 2 )

#How many frames to capture per second
FPS = 1

folderName = input("Please enter the name of this recording's file: ")

#Create the recording folder if it does not exist

Path("Data/"+folderName).mkdir(parents=True, exist_ok=True)


lastTime = time.time()
curTime = time.time()

#Seconds since last frame
deltaTime = 0.0

manualMode = True
manualMoistures = []

if len(sys.argv) >= 2:
	if sys.argv[1] == "-manual":
		manualMode = True


frame = None

def SaveFrame():
	
	#Save Frame
	
	ret, frame1 = cam.read()
	ret, frame1 = cam.read()
	deltaTime = 0.0
	if not manualMode:
		cv2.imshow('frame', frame1)
	cv2.imwrite("Data/"+folderName+"/"+str(time.time())+".jpg", frame1)

#Throw away first frame?
ret, frame = cam.read()


#Main recording loop
while(True):

	#Record frame
	#ret, frame = cam.read()

	
	
	
	
	
	
	if deltaTime >= FPS and not manualMode:
		SaveFrame()
	
	if manualMode:
		m = input("Enter the moisture (format: x.x, example: 1.3) or q to quit: ")
		if m == "q":
			#Wrap up
			manualCSV = open("Data/"+folderName+"/moistures.csv", "w")
			ms = "Moisture\n"
			for mo in manualMoistures:
				ms += str(mo)
				ms += "\n"
			manualCSV.write(ms)
			manualCSV.close()
			break
		else:
			SaveFrame()
			m = float(m)
			manualMoistures.append(m)
	else:
		
		if cv2.waitKey(1) & 0xFF == ord('q'): 
			break

cam.release()
cv2.destroyAllWindows()
