from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject

video_path = "StagesepxData/S5.1.mp4"
video = VideoObject(video_path)
video.load_frames()

# --- cutter ---
cutter = VideoCutter()
res = cutter.cut(video)
stable, unstable = res.get_range()
data_home = res.pick_and_save(stable, 5)

# --- classify ---
cl = SVMClassifier()
cl.load(data_home)
cl.train()
classify_result = cl.classify(video, stable)

# --- draw ---
r = Reporter()
r.draw(classify_result)