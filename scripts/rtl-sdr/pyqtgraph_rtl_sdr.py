#!/usr/bin/env python

# import required libraries
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import numpy as np
from rtlsdr import RtlSdr

# plot constants
CENTER_FREQ = 2450 * 1e6 
SAMPLE_SIZE = 16384
ATTENUATOR = 0
DECIMATION = 4
NFFT = 1024*4
NUM_SAMPLES_PER_SCAN = NFFT*16
NUM_BUFFERED_SWEEPS = 100


win = pg.GraphicsWindow()
win.resize(1000,600)
win.setWindowTitle("RTL-SDR Example")

# initialize plot
data_plot = win.addPlot(title="Voltage Vs. Time")
data_plot.showGrid(True, True, alpha = 1)
data_plot.addLegend()
# initialize a curve for the plot 
i_curve = data_plot.plot(pen='r', name = "In-Phase Signal")
q_curve = data_plot.plot(pen='y', name = "Quadrature Signal")

win.nextRow()
# initialize plot
fft_plot = win.addPlot(title="Power Vs. Frequency")
fft_plot.showGrid(True, True, alpha = 1)
fft_plot.addLegend()
# initialize a curve for the plot 
curve = fft_plot.plot(pen='g', name = "Power Spectrum")
max_curve = fft_plot.plot(pen='r', name = "Max Hold")
sdr = RtlSdr()
# some defaults
sdr.rs = 2e6
sdr.fc = 106.9e6
sdr.gain = 30
max_data = []
def update():
    global dut, curve, max_data
    samples = sdr.read_samples(SAMPLE_SIZE)
    samples = samples * np.hanning(len(samples))
    pow = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples))))
    i_curve.setData(samples.real)
    q_curve.setData(samples.imag)
    if len(max_data) == 0:
        max_data = pow
    else:
        max_data = np.maximum(max_data, pow)
    curve.setData(pow)
    max_curve.setData(max_data)
    data_plot.enableAutoRange('xy', False)
    fft_plot.enableAutoRange('xy', False)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
