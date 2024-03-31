import matplotlib.pyplot as plt
import calibration

xl = []
yl = []
for x in range(4000):
	xl.append(x)
	yl.append(calibration.GetMoisture(x))

plt.plot(xl,yl)
plt.show()
