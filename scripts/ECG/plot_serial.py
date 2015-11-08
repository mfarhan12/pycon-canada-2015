import serial
import sys
import time
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

# constants
BAUDE_RATE = 9600
COM = 2
ARDUINO_MAX_INT = 2 ** 10
ARDUINO_MAX_VOLTAGE = 3.3
WINDOW_SIZE = 30
MAX_DATA_SIZE = 1024

# declare the Window
app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Arduino Analog Plotter")
win.resize(1000,600)


# initialize plots
raw_plot = win.addPlot(title="Raw Pin Data")
raw_curve = raw_plot.plot(pen = 'y')
raw_plot.addLegend()
raw_plot.showGrid(True, True)
raw_plot.setYRange(0 ,1200)
raw_plot.setXRange(0 ,1024)

# disable auto size of the x-y axis
raw_plot.enableAutoRange('xy', False)
raw_data = np.zeros(1024)
# open serial
ser = serial.Serial(COM, BAUDE_RATE)
line = pg.InfiniteLine(pos = 1024, angle = 0, pen=(24,215,248))
raw_plot.addItem(line)
def update():

    global raw_data
    # open serial port
    raw_capture = []
    for x in range(WINDOW_SIZE):
        r = ser.readline()
        raw_capture.append(float(r))

    
    raw_data = np.concatenate([raw_data, raw_capture])
    
  
    # remove first bin to make room for new bin

    if len(raw_data) > MAX_DATA_SIZE:
        raw_data = raw_data[WINDOW_SIZE:]

    # plot data
    raw_curve.setData(raw_data)

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


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


