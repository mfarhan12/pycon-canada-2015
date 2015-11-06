import serial
import sys
import time
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

BAUDE_RATE = 9600
COM = 2
ARDUINO_MAX_INT = 2 ** 10
ARDUINO_MAX_VOLTAGE = 3.3
WINDOW_SIZE = 30
MAX_DATA_SIZE = 1024
# declare the GUI
app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Narrow Band Mode I/data Plot")
win.resize(1000,600)
win.setWindowTitle("Narrow Band Mode I/data Plot")

# initialize plots
raw_plot = win.addPlot(title="Raw ECG")
raw_curve = raw_plot.plot(pen = 'y')


win.nextRow()

smooth_plot = win.addPlot(title = 'Normalized ECG')
smooth_curve = smooth_plot.plot(pen = 'g')
raw_data = np.zeros(1024)
dc_data = []
normalized_data = []
smooth_data = np.zeros(1024)
win.nextRow()
ser = serial.Serial(COM, BAUDE_RATE)
def update():

    global raw_data, smooth_data, dc_data, normalized_data,smooth_data
    # open serial port
    raw_capture = []
    for x in range(WINDOW_SIZE):
        r = ser.readline()
        raw_capture.append(float(r))

    
    raw_data = np.concatenate([raw_data, raw_capture])
    
   
    
    # smooth out the data by dividing by the mean
    smoothed = raw_capture / np.mean(raw_capture)
    smooth_data = np.concatenate([smooth_data, smoothed])
    # remove first bin to make room for new bin

    if len(raw_data) > MAX_DATA_SIZE:

        raw_data = raw_data[WINDOW_SIZE:]

        smooth_data = smooth_data[WINDOW_SIZE:]
    # plot data
    raw_curve.setData(raw_data)
    smooth_curve.setData(smooth_data)
    print max(smooth_data)  
def savecounter():
    ser.close()

import atexit
atexit.register(savecounter)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


