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
	
	for c in range(len(calibrations)):
		if rawMoisture == cal.base:
			lowerBound = c
			upperBound = c
			pos = 0.5
		
