import csv

class CalibrationEntry:
	def __init__(self, b, a):
		self.base = b
		self.actual = a

calibrations = []

#Load calibrations file
with open("Calibration/calibration.csv", newline='') as csvFile:
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
	
	lowerBound = 0
	pos = 0.0 # Ranges from 0.0-1.0
	upperBound = 0
	match = False
	slope = 0.0
	
	oob = False
	uppr = False
	
	passed = False
	
	for c in range(len(calibrations)):
		if rawMoisture == calibrations[c].base:
			lowerBound = c
			upperBound = c
			pos = 0.5
			match = True
		if not match:
			if not passed:
				if rawMoisture > calibrations[c].base:
					if c > 0:
						passed = True
						upperBound = c
						lowerBound = c-1
					#Moisture is less than on calibration
					else:
						oob = True
						passed = True
						rise = calibrations[c+1].actual - calibrations[c].actual
						run = calibrations[c+1].base - calibrations[c].base
						slope = rise/run
						
	if not passed:
		c = len(calibrations) - 1
		uppr = True
		oob = True
		
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
			actual = upperBase + ad
		else:
			# Below range
			
	else:
		# In range
		upperBase = calibrations[upperBound].base
		lowerBase = calibrations[lowerBound].base
		rang = abs(upperBase - lowerBase)
		if not match:
			pos = (rawMoisture-lowerBase)/rang
		
		upperAc = calibrations[upperBound].actual
		lowerAc = calibrations[lowerBound].actual
		rang = abs(upperAc - lowerAc)
		
		actual = lowerAc + (pos*rang)
	
