import csv
import os
import sys

class CalibrationEntry:
	def __init__(self, b, a):
		self.base = b
		self.actual = a

calibrations = []

#Load calibrations file
with open(os.path.dirname(os.path.abspath(__file__))+"/calibration.csv", newline='') as csvFile:
	cReader = csv.reader(csvFile, delimiter=",", skipinitialspace=True)
	firstRow = True
	for row in cReader: 
		if firstRow:
			firstRow = False
			continue
		b = float(row[0])
		a = float(row[1])
		newCal = CalibrationEntry(b, a)
		calibrations.append(newCal)

# Returns the calibrated moisture
def GetMoisture(rawMoisture):
	
	actual = -1.0
	
	lowerBound = 0
	pos = 0.0 # Ranges from 0.0-1.0
	upperBound = 0
	match = False
	slope = 0.0
	
	oob = False
	uppr = False
	
	passed = False
	
	for c in range(len(calibrations)):
		#Exact moisture match
		if rawMoisture == calibrations[c].base:
			lowerBound = c
			upperBound = c
			pos = 0.5
			match = True
			#print(calibrations[c].actual)
			return calibrations[c].actual
		#In between 2 points
		if not match:
			if not passed and c < len(calibrations)-1:
				if rawMoisture < calibrations[c+1].base and rawMoisture > calibrations[c].base:
					passed = True
					upperBound = c+1
	
					lowerBound = c
	
	c = len(calibrations) - 2
	#Moisture is less than on calibration
	if rawMoisture < calibrations[0].base:
		oob = True
		passed = True
		
		
		#rise = calibrations[c+1].actual - calibrations[c].actual
		#run = calibrations[c+1].base - calibrations[c].base
		
		rise = calibrations[1].actual - calibrations[0].actual
		run = calibrations[1].base - calibrations[0].base
		
		slope = rise/run
						
	if not passed:
		
		uppr = True
		oob = True
		
		#rise = calibrations[1].actual - calibrations[0].actual
		#run = calibrations[1].base - calibrations[0].base
		
		rise = calibrations[c+1].actual - calibrations[c].actual
		run = calibrations[c+1].base - calibrations[c].base
		
		
		slope = rise/run
		
	actual = 0.0
		
	if oob:
		# Out of bounds, use slope
		c = len(calibrations) - 1
		if uppr:
			#Above range
			upperBase = calibrations[c].base
			upperAc = calibrations[c].actual
			pos = rawMoisture - upperBase
			ad = pos*slope
			actual = upperAc + ad
		else:
			# Below range
			lowerBase = calibrations[0].base
			lowerAc = calibrations[0].actual
			pos = rawMoisture - lowerBase
			ad = pos*slope
			actual = lowerAc + ad
		
			
	else:
		# In range
		upperBase = calibrations[upperBound].base
		lowerBase = calibrations[lowerBound].base
		rang = abs(upperBase - lowerBase)
		if not match:
			pos = (rawMoisture-lowerBase)/rang
			pos = 1-pos
		
		upperAc = calibrations[upperBound].actual
		lowerAc = calibrations[lowerBound].actual
		rang = abs(upperAc - lowerAc)
		
		actual = upperAc + (pos*rang)
		
	print(actual)
	return actual
	
print(GetMoisture(3000))
