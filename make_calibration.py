import sys
import os
import csv
import datetime
import calendar
from PIL import Image
from PIL import ImageDraw

class CSVEntry:
	def __init__(self, t, m):
		self.time = t
		self.moisture = m

class RecEntry:
	def __init__(self, t, d):
		self.time = t
		self.moisture = d

class CombinedEntry:
	def __init__(self, c, i):
		self.csv = c
		self.img = i
		self.moisture2 = -1
	

twoMeters = False #Whether or not to use a 2nd meter that you manually add water every
#meterInterval seconds, increasing it by 1 each time until it reaches 10
meterInterval = 60 #Seconds to wait before adding water to the pot to increase by 1
currentMoisture2 = 1

simpleClasses = False
simpleNames = ["dry", "slightly wet", "wet", "very wet", "soaked"]
moistureRange = [3130, 1300]
simpleClassAmount = 5

moistureRanges = []
incr = abs(moistureRange[0] - moistureRange[1])

if len(sys.argv) >= 3:

	csvEntries = []
	recEntries = []
	combinedEntries = []
	
	csvFileName = sys.argv[1]
	#recordingFolderName = sys.argv[2]
	moistureColumn = int(sys.argv[2])
	
	if len(sys.argv) >= 4:
		for _arg in sys.argv:
			if _arg == "simple":
				simpleClasses = True
			if _arg == "dual":
				twoMeters = True
	
	#Load in-house CSV File
	with open(csvFileName, newline='') as csvFile:
		cReader = csv.reader(csvFile, delimiter=",", skipinitialspace=True)
		firstRow = True
		for row in cReader: 
			if firstRow:
				firstRow = False
				continue
			rawDate = row[0].split("-")
			rawTime = row[1].split("-")
			
			rYear = int(rawDate[0])
			rMonth = int(rawDate[1])
			rDay = int(rawDate[2])
			
			rHour = int(rawTime[0])
			rMinute = int(rawTime[1])
			rSecond = int(rawTime[2])
			
			t=datetime.datetime(rYear, rMonth, rDay, rHour, rMinute, rSecond)
			
			#Read in moisture
			m = int(row[moistureColumn+1])
				
			
			newCSV = CSVEntry(int(calendar.timegm(t.timetuple())), m)
			#print(str(newCSV.time) + ", " + str(newCSV.moisture))
			csvEntries.append(newCSV)
			
	#Load manually recorded CSV File
	with open("Calibration/recording.csv", newline='') as csvFile:
		cReader = csv.reader(csvFile, delimiter=",", skipinitialspace=True)
		firstRow = True
		for row in cReader: 
			if firstRow:
				firstRow = False
				continue
			
			_time = float(row[0])
			_moisture = float(row[1])
				
			
			newRec = RecEntry(_time, _moisture)
			#print(str(newCSV.time) + ", " + str(newCSV.moisture))
			recEntries.append(newRec)
	
	class CorrectionEntry:
		def __init__(self, b, c):
			self.base = b
			self.actual = c
	
	corrections = []
	
	for rec in recEntries:
		lowestDelta = 999999999
		lowest = 0
		for c in range(len(csvEntries)):
			td = abs(rec.time - csvEntries[c].time)
			if td < lowestDelta:
				lowestDelta = td
				lowest = c
		newC = CorrectionEntry(csvEntries[lowest].moisture, rec.moisture)
		
		#print(str(newC.base) + " -> " + str(newC.actual))
		
		corrections.append(newC)
		
	#Average duplicates and order by moisture
	for c in range(len(corrections)):
		k = c
		while k < len(corrections):
			if corrections[k].actual < corrections[c].actual:
				temp = corrections[c]
				corrections[c] = corrections[k]
				corrections[k] = temp
			k += 1
	
	finalCorrections = []
	
	curCorrection = None
	avgMoisture = 0.0
	lastMoisture = corrections[0].actual
	dupes = 0
	
	curCorrection = CorrectionEntry(corrections[0].base, corrections[0].actual)
	
	for c in range(len(corrections)):
		curMoisture = corrections[c].actual
		if lastMoisture != curMoisture:
			
			#if curCorrection != None:
			avgMoisture /= dupes
			curCorrection.base = avgMoisture
			finalCorrections.append(curCorrection)
			curCorrection = CorrectionEntry(corrections[c].base, corrections[c].actual)
			dupes = 1
			avgMoisture = curCorrection.base
		else:
			dupes += 1
			avgMoisture += curMoisture
		lastMoisture = corrections[c].actual
		
	avgMoisture /= dupes
	curCorrection.base = avgMoisture
	finalCorrections.append(curCorrection)
			
		
	
	calibrationFile = open("Calibration/calibration.csv", "w")
	
	csvText = "Moisture, Actual\n"
	
	for co in finalCorrections:
		csvText += str(co.base)
		csvText += ", "
		csvText += str(co.actual)
		csvText += "\n"
	
	calibrationFile.write(csvText)
	calibrationFile.close()
		
else:
	print("Usage: consolidate.py <csv_file> <column>")
