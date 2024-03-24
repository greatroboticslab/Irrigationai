import sys
import os
import csv
import datetime
import calendar
from PIL import Image
from PIL import ImageDraw

class CSVEntry:
	def __init__(self, i, m):
		self.img = i
		self.moisture = m
	
moistures = []
imgNames = []

entries = []

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

if len(sys.argv) >= 2:

	csvEntries = []
	imgEntries = []
	combinedEntries = []
	
	recordingFolderName = sys.argv[1]
	outputFolder = sys.argv[2]
	
	if len(sys.argv) >= 3:
		for _arg in sys.argv:
			if _arg == "simple":
				simpleClasses = True
			if _arg == "dual":
				twoMeters = True
	
	#Load CSV File
	with open(recordingFolderName+"/moistures.csv", newline='') as csvFile:
		cReader = csv.reader(csvFile, delimiter=",", skipinitialspace=True)
		firstRow = True
		for row in cReader: 
			if firstRow:
				firstRow = False
				continue
			m = float(row[0])
			
			moistures.append(m)
			
	#Load images folder
	imgs = sorted(os.listdir(recordingFolderName))
	for i in imgs:
		if not i.find(".csv") == -1 :
			continue
		imgNames.append(i)
		
	for i in range(len(moistures)):
		newEntry = CSVEntry(imgNames[i], moistures[i])
		entries.append(newEntry)
		
	
	#Create output folder
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
				
	
	outputCsvData = "Image, Moisture\n"
	if twoMeters:
		outputCsvData = "Time, Moisture, Moisture2, Image\n"
	
	ite = 1
		
	for e in entries:
	
		img = Image.open(recordingFolderName+"/"+e.img)
		iDraw = ImageDraw.Draw(img)
		iDraw.text((10,10), "Moisture: " + str(round(e.moisture)) + "\nTime: ", fill=(255,255,0))
		img.save(outputFolder+"/"+str(ite)+".png")
		
		
		
		outputCsvData += str(ite)+".png"
		outputCsvData += ", "
		outputCsvData += str(e.moisture)
		
		outputCsvData += "\n"
		
		ite += 1
	
	outputCsv = open(outputFolder+"/dat.csv", "w")
	outputCsv.write(outputCsvData)
	outputCsv.close()
		
	
else:
	print("Usage: consolidate.py <recording_folder_name> <output_folder>")
