import os
import cv2
import numpy as np
from datetime import timedelta
from PIL import Image
from numpy import asarray

data_directory = "Data"

FRAMES_PER_SECOND = 10
FRAME_WIDTH = 300
FRAME_HEIGHT = 300

epoch_count = 1


#1 = read video files, 2 = read images
fileMode = 1

rawMoisture = []
videoNames = []
videoData = []

for folderName in os.listdir(data_directory):
    f = os.path.join(data_directory, folderName)
    if not os.path.isfile(f):
    
        frameNames = []
    
        for fileName in os.listdir(f):
            
            #print(fileName)
            f2 = os.path.join(f, fileName)
            if fileName.endswith(".txt"):
                
                mFile = open(f2, "r")
                moisture = float(mFile.read())
                mFile.close()
                rawMoisture.append(moisture)
            else:
                if fileMode == 1:
                    videoNames.append(f2)
                elif fileMode == 2:
                    frameNames.append(f2)
        
        if fileMode == 2:
            videoNames.append(frameNames)

print(rawMoisture)
print(videoNames)


def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    #print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

if(fileMode == 1):

    for videoName in videoNames:
        currentData = []
        cap = cv2.VideoCapture(videoName)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
        saving_frames_per_second = min(fps, FRAMES_PER_SECOND)
        # get the list of duration spots to save
        saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
        
        count = 0
        while True:
            is_read, frame = cap.read()
            
            if not is_read:
                # break out of the loop if there are no frames to read
                break
            # get the duration by dividing the frame count by the FPS
            frame_duration = count / fps
            try:
                # get the earliest duration to save
                closest_duration = saving_frames_durations[0]
            except IndexError:
                # the list is empty, all duration frames were saved
                break
            if frame_duration >= closest_duration:
                # if closest duration is less than or equals the frame duration, 
                # then save the frame
                frame = cv2.resize(frame,(FRAME_WIDTH, FRAME_HEIGHT), interpolation = cv2.INTER_AREA)
                
                frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
                
                currentData.append(frame)
                
                #print(frame)
                
                #cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame) 
                
                
                # drop the duration spot from the list, since this duration spot is already saved
                try:
                    saving_frames_durations.pop(0)
                except IndexError:
                    pass
            # increment the frame count
            count += 1
        
        videoData.append(currentData)

else:
    
    for frames in videoNames:
        framesData = []
        for frameName in frames:
            img = Image.open(frameName)
            img = img.resize((FRAME_WIDTH, FRAME_HEIGHT))
            
            numpydata = asarray(img)
            
            framesData.append(numpydata)
        videoData.append(framesData)
        
#print(videoData[0])

#Now set up the model



from torch import nn
from torchvision import models

class Resnt18Rnn(nn.Module):
    def __init__(self, params_model):
        super(Resnt18Rnn, self).__init__()
        num_classes = params_model["num_classes"]
        dr_rate= params_model["dr_rate"]
        pretrained = params_model["pretrained"]
        rnn_hidden_size = params_model["rnn_hidden_size"]
        rnn_num_layers = params_model["rnn_num_layers"]
        
        baseModel = models.resnet18(pretrained=pretrained)
        num_features = baseModel.fc.in_features
        baseModel.fc = Identity()
        self.baseModel = baseModel
        self.dropout= nn.Dropout(dr_rate)
        self.rnn = nn.LSTM(num_features, rnn_hidden_size, rnn_num_layers)
        self.fc1 = nn.Linear(rnn_hidden_size, num_classes)
    def forward(self, x):
        b_z, ts, c, h, w = x.shape
        ii = 0
        y = self.baseModel((x[:,ii]))
        output, (hn, cn) = self.rnn(y.unsqueeze(1))
        for ii in range(1, ts):
            y = self.baseModel((x[:,ii]))
            out, (hn, cn) = self.rnn(y.unsqueeze(1), (hn, cn))
        out = self.dropout(out[:,-1])
        out = self.fc1(out) 
        return out 
    
class Identity(nn.Module):
    def __init__(self):
        super(Identity, self).__init__()
    def forward(self, x):
        return x   

from torch.utils.data import DataLoader, TensorDataset    
import torch

params_model={
"num_classes": 1,
"dr_rate": 0.1,
"pretrained" : True,
"rnn_num_layers": 1,
"rnn_hidden_size": 100,}
model = Resnt18Rnn(params_model)

videoData = np.array(videoData)
moistures = np.array(rawMoisture)

videoData = torch.tensor(videoData)
moistures = torch.tensor(moistures)

#bothh = [videoData, rawMoisture]

print(videoData.shape) 
print(moistures.shape) 

train_data = TensorDataset(videoData , moistures)

train_loader = DataLoader(train_data, batch_size=64, shuffle=False)


for epoch in range(epoch_count):
    
    for x, y in train_loader:
        
        optimizer.zero_grad()
        
        outputs = model(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        
        #print(y)
        
        running_loss += loss.item()
        if epoch % 2 == 0 or True:    # print every 2000 mini-batches
            print(f'[{epoch + 1}, {epoch + 1:5d}] loss: {running_loss / 2000:.3f}')
            running_loss = 0.0