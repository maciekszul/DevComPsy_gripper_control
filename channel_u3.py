import u3
import time
import sys

d = u3.U3()
d.configU3()
d.getCalibrationData()
d.configIO(FIOAnalog=3)

for i in range(1000):
    print(d.getAIN(0), d.getAIN(1), d.getAIN(2), d.getAIN(3))
    time.sleep(0.1)

d.close()