# Recording
Using record.py you can record from the webcam every 1 second.
## How to Record
1. python record.py
2. Enter folder name, this recording will be saved in the Data folder.

# Consolidation/Combining
Now that you have a recording, you need to combine the images and moisture values.
This can be done with:
	
	consolidate.py <csv_file> <recording_folder_name> <column> <output_folder>
	
### Example:
python consolidate.py ~/Irrigationai/Data/recording6/2-24-2024_10-13-14.csv ~/Irrigationai/Data/recording6/ 5 ~/Downloads/recording6

# Training

YOLOv5 is in the YOLO folder. It contains a readme with instructions on how to use. The output data after training is stored in YOLO/runs/trains/. Here is a snippet of running the training code:

	python train.py --img 640 --epochs 1000 --data data/moisturev4.yaml --weights yolov5s.pt

### Data

Data is stored in YOLO/data. A dataset needs a .yaml file in this directory, which links to a folder with its images and classes. For example, moisturev4.yaml links to the folder YOLO/moisturev4, a dataset with 351 images.
