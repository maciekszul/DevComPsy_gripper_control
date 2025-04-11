import signal
import u3
import time
import numpy as np


class GracefulExiter():

    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.change_state)

    def change_state(self, signum, frame):
        print("exit flag set to True (repeat to exit now)")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def exit(self):
        return self.state

flag = GracefulExiter()    

d = u3.U3()
d.configU3()
d.getCalibrationData()
d.configIO(FIOAnalog=3)

iter = 0
calibration = []
baseline = 0.0
calib = True
while True:
    iter += 1
    data = []
    for ms in range(10):
        data.append(d.getAIN(0))
        time.sleep(0.001)
    output = np.mean(data)*1000

    if calib:
        if iter < 50:
            calibration.append(output)
            calibrated = False
        
        elif iter == 50:
            baseline = np.mean(calibration)
            calibrated = True

        print(f"calibrated: {calibrated} output: {output - baseline}")
    else:
        print(output)

    if flag.exit():
        break



d.close()