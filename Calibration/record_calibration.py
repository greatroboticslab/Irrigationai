#This program reads in moisture levels and time stamps
#These are compared to our in-house moisture measurement device's timestamps
#and moistures to use linear regression to convert our device to the standard measurements

import sys
import time
from pathlib import Path


lastTime = time.time()
curTime = time.time()

#Seconds since last frame
deltaTime = 0.0

class MoistureMeasurement:
	def __init__(self, t, m):
		self.time = t
		self.moisture = m
		
manualMoistures = []

if len(sys.argv) >= 2:
	if sys.argv[1] == "-manual":
		manualMode = True


#Main recording loop
while(True):
	
	
	
	
	
	m = input("Enter the moisture (format: x.x, example: 1.3) or q to quit: ")
	if m == "q":
		#Wrap up
		manualCSV = open("recording.csv", "w")
		ms = "Time, Moisture\n"
		for mo in manualMoistures:
			ms += str(mo.time)
			ms += ", "
			ms += str(mo.moisture)
			ms += "\n"
		manualCSV.write(ms)
		manualCSV.close()
		break
	else:
		
		try:
		
			#Get current time
			curTime = time.time()
			deltaTime += curTime-lastTime
			lastTime = time.time()
			
			m = float(m)
			newM = MoistureMeasurement(curTime, m)
			manualMoistures.append(newM)
		
		except ValueError:
			print("Error: value is not a float.")

