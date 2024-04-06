import sys
import os
import csv
import datetime
import calendar
sys.path.append("../Calibration/")
import calibration as cal
from PIL import Image
from PIL import ImageDraw

class CSVEntry:
	def __init__(self, t, m):
		self.time = t
		self.moisture = m

class ImgEntry:
	def __init__(self, t, d):
		self.time = t
		self.directory = d

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

if len(sys.argv) >= 4:

	csvEntries = []
	imgEntries = []
	combinedEntries = []
	
	csvFileName = sys.argv[1]
	recordingFolderName = sys.argv[2]
	moistureColumn = int(sys.argv[3])
	outputFolder = sys.argv[4]
	
	if len(sys.argv) >= 4:
		for _arg in sys.argv:
			if _arg == "simple":
				simpleClasses = True
			if _arg == "dual":
				twoMeters = True
	
	#Load CSV File
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
			m = cal.GetMoisture(m)
				
			
			newCSV = CSVEntry(int(calendar.timegm(t.timetuple())), m)
			#print(str(newCSV.time) + ", " + str(newCSV.moisture))
			csvEntries.append(newCSV)
			
	#Load images folder
	imgs = sorted(os.listdir(recordingFolderName))
	for i in imgs:
		if not i.find(".csv") == -1 :
			continue
		newImg = ImgEntry(int(i[:i.find(".")]), i)
		#print(newImg.time)
		imgEntries.append(newImg)
	
	#Synchronize the two sets
	
	cLen = len(csvEntries)
	iLen = len(imgEntries)
	
	startPoint = 0
	foundPoint = False
	csvOffset = False
	
	#CSV starts before images
	if csvEntries[0].time < imgEntries[0].time:
		for x in range(cLen):
			if csvEntries[x].time > imgEntries[0].time:
				if not foundPoint:
					startPoint = x
				foundPoint = True
				csvOffset = True
	#CSV starts after images
	if csvEntries[0].time > imgEntries[0].time:
		for x in range(iLen):
			if imgEntries[x].time > csvEntries[0].time:
				if not foundPoint:
					startPoint = x
				foundPoint = True
				
	#Combine the two sets with the offsets and make sure they are the same size
	maxLen = cLen
	if iLen < cLen:
		maxLen = iLen
	
	
	t = 0
	#If the list starts at an offset of the CSV entries
	if csvOffset:
		x = startPoint
		y = 0
		while x < maxLen and y < iLen:
			
			newCombined = CombinedEntry(csvEntries[x], imgEntries[y])
			if twoMeters:
				t += 1
				if t >= meterInterval:
					currentMoisture2 += 1
					if currentMoisture > 10:
						currentMoisture = 10
					t = 0
				newCombined.moisture2 = currentMoisture2
			combinedEntries.append(newCombined)
			
			y += 1
			x += 1
	
	else:
		x = startPoint
		y = 0
		while x < maxLen and y < cLen:
			
			newCombined = CombinedEntry(csvEntries[y], imgEntries[x])
			if twoMeters:
				t += 1
				if t >= meterInterval:
					currentMoisture2 += 1
					if currentMoisture > 10:
						currentMoisture = 10
					t = 0
				newCombined.moisture2 = currentMoisture2
			combinedEntries.append(newCombined)
			
			y += 1
			x += 1
	
	#Create output folder
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
				
	
	outputCsvData = "Time, Moisture, Image\n"
	if twoMeters:
		outputCsvData = "Time, Moisture, Moisture2, Image\n"
	
	ite = 1
		
	for e in combinedEntries:
	
		img = Image.open(recordingFolderName+"/"+e.img.directory)
		iDraw = ImageDraw.Draw(img)
		iDraw.text((10,10), "Moisture: " + str(e.csv.moisture) + "\nTime: " + str(e.csv.time), fill=(255,255,0))
		img.save(outputFolder+"/"+str(ite)+".png")
		
		outputCsvData += str(e.csv.time)
		outputCsvData += ", "
		outputCsvData += str(e.csv.moisture)
		outputCsvData += ", "
		if twoMeters:
			outputCsvData += str(e.moisture2)
			outputCsvData += ", "
		outputCsvData += str(ite)+".png"
		outputCsvData += "\n"
		
		ite += 1
	
	outputCsv = open(outputFolder+"/dat.csv", "w")
	outputCsv.write(outputCsvData)
	outputCsv.close()
		
	
else:
	print("Usage: consolidate.py <csv_file> <recording_folder_name> <column> <output_folder>")
