# Overview
This repo is a collection of tools to use computer vision to estimate the moisture value of soil using images of soil with different spectrum lasers shining on the soil. Frames are recorded, matched to moisture values through different methods, and then trained in YOLOv5 (a copy of which is included) after labeling.

# Requirements
- Python OpenCV2
- PyTorch

# Recording
Using record.py you can record from the webcam every 1 second.
## How to Record
1. python record.py
2. Enter folder name, this recording will be saved in the Data folder.

# Post-Processing/Combining
Now that you have a recording, you need to combine the images and moisture values.
This can be done with:
	
	consolidate.py <recording_folder_name> <output_folder>
	
In the post-processing folder. This method is for manual recordings where you enter in the moisture.

The below method is in the Automatic folder. It uses our custom moisture reader's csv file values, and uses calibration to convert it to the moisture values 0-10. MUST RUN THE SCRIPT IN THE SAME DIRECTORY. To run:

	consolidate_automatic.py <csv_file> <recording_folder_name> <column> <output_folder>
	
### Example:
python consolidate_automatic.py ~/Irrigationai/Data/recording6/2-24-2024_10-13-14.csv ~/Irrigationai/Data/recording6/ 5 ~/Downloads/recording6

# Training

YOLOv5 is in the YOLO folder. It contains a readme with instructions on how to use. Here is a snippet of running the training code:

	python train.py --img 640 --epochs 1000 --data data/moisturev4.yaml --weights yolov5s.pt --hyp data/hyps/hyp.scratch-med.yaml

The output data after training is stored in YOLO/runs/trains/.
![Runs](ReadmeImages/runs.png)

The runs folder contain training results, and example predictions.

![Predictions](ReadmeImages/predictions.jpg)

![Results](ReadmeImages/results.png)

### Data

Data is stored in YOLO/data. A dataset needs a .yaml file in this directory, which links to a folder with its images and classes. For example, moisturev4.yaml links to the folder YOLO/moisturev4, a dataset with 351 images.

### Hyperparameters

Hyperparameters are stored in YOLO/data/hyps. They are .yaml files with arguments that can be edited, for instance: lr0 is initial learning rate, and lrf is the final learning rate. You can specify a .yaml file for hyperparameters with the --hyp argument.
