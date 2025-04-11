import u3
import random
import time
import signal
import matplotlib.pyplot as plt
import numpy as np
# Initialize empty lists to store data
timestamps = []
sensor_data = []
# def update_plot():
#     # Generate random sensor data
#     timestamp = time.time()
#     data = random.randint(0, 100)
    
#     # Append new data to lists
#     timestamps.append(timestamp)
#     sensor_data.append(data)
    
#     # Clear previous plot
#     plt.clf()
    
#     # Plot updated data
#     plt.plot(timestamps, sensor_data)
#     plt.xlabel('Timestamp')
#     plt.ylabel('Sensor Data')
#     plt.title('Live Sensor Data')
#     plt.grid(True)
#     plt.set_ylim()
    
#     # Update plot
#     plt.pause(0.1)  # Pause for 1 second
# Continuously update plot
# while True:
#     update_plot()


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


#  calibration
calib_data_0 = []
calib_data_2 = []
for i in range(1000):
    calib_data_0.append(d.getAIN(0))
    calib_data_2.append(d.getAIN(2))
baseline_0 = np.mean(calib_data_0)
baseline_2 = np.mean(calib_data_2)


timestamps = np.linspace(-10, 0, num=200)
output_array_0 = np.zeros(200).tolist()
output_array_2 = np.zeros(200).tolist()
f, ax = plt.subplots(1, 1, figsize=(18, 6))
def update_plot(output_array_0, output_array_2):
    plt.clf()
    # out = ((d.getAIN(0) - baseline)) * 1000 * 0.0380952
    # out_0 = ((d.getAIN(0) - baseline_0))
    # out_2 = ((d.getAIN(2) - baseline_2))
    out_0 = d.getAIN(0)
    out_2 = d.getAIN(2)
    output_array_0.append(out_0)
    output_array_0 = output_array_0[1:]
    output_array_2.append(out_2)
    output_array_2 = output_array_2[1:]
    plt.plot(timestamps, output_array_0, c="red")
    plt.plot(timestamps, output_array_2, c="blue")
    plt.xlabel('Timestamp')
    plt.ylabel('Sensor Data')
    plt.axhline(4)
    plt.grid(visible=True)
    plt.pause(0.0001)
    plt.ylim(-0.05, 0.4)
    return output_array_0, output_array_2

while True:
    output_array_0, output_array_2 = update_plot(output_array_0, output_array_2)

    if flag.exit():
        break