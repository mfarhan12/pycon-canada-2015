import serial
import sys
import time
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

BAUDE_RATE = 9600
COM = 11
ARDUINO_MAX_INT = 2 ** 10
ARDUINO_MAX_VOLTAGE = 3.3
WINDOW_SIZE = 4
MAX_DATA_SIZE = 1024
# declare the GUI
app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Narrow Band Mode I/data Plot")
win.resize(1000,600)
win.setWindowTitle("Narrow Band Mode I/data Plot")

# initialize plots
raw_plot = win.addPlot(title="Raw ECG")
raw_curve = raw_Plot.plot(pen = 'y')

dc_removed_plot = win.addPlot(title = 'DC Offset Removed')
dc_curve = normalized_plot.plot(pen = 'b')

normalized_Plot = win.addPlot(title = 'Normalized ECG')
normalized_curve = normalized_plot.plot(pen = 'r')
win.addRow()

smooth_plot = win.addPlot(title = 'Smooth ECG')
smooth_curve = smooth_plot.plot(pen = 'g')
raw_data = []
dc_data = []
normalized_data = []
smooth_data = []
def update():

    global  raw_curve, normalized_curve, smooth_curve
    # open serial port
    ser = serial.Serial(COM, BAUDE_RATE)
    raw_capture = []

    # capture data

    raw_capture = float(ser.readlines(WINDOW_SIZE))
    raw_data = np.concatenate([raw_data, raw_capture])
    
    ser.close()
    
    # remove dc offset
    removed_dc_offset = raw_capture - (np.mean(raw_capture)
    dc_data = np.concatenate([dc_data, remove_dc_offset])
    
    # normalize data
    normalize = ARDUINO_MAX_VOLTAGE * (removed_dc_offset / ARDUINO_MAX_INT)
    normalized_data =  np.concatenate([normalized_data, normalize])
    
    # smooth out the data by dividing by the mean
    smoothed = normalize / np.mean(normalize)
    smooth_data = np.concatenate([smooth_data, normalized_data])
    # remove first bin to make room for new bin
    if len(raw_data) > MAX_DATA_SIZE:
        raw_data.pop(0)
        dc_data.pop(0)
        normalized_data.pop(0)
        smooth_data.pop(0)
    # plot data
    raw_curve.setData(raw_data)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


