import pyaudio
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 14100
CHUNK = 1024
MAX_PLOT_SIZE = CHUNK * 50
 
# setup audio recording
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

win = pg.GraphicsWindow()
win.setWindowTitle("Microphone Audio Data")

# create a plot for the time domain data
data_plot = win.addPlot(title="Audio Signal Vs Time")
data_plot.setXRange(0 ,MAX_PLOT_SIZE)
data_plot.showGrid(True, True)
data_plot.addLegend()
time_curve = data_plot.plot(pen=(24,215,248), name = "Time Domain Audio")

# create a plot for the frequency domain data
win.nextRow()
fft_plot = win.addPlot(title="Power Vs Frequency Domain") 
fft_plot.addLegend()
fft_curve = fft_plot.plot(pen='y', name = "Power Spectrum")

fft_plot.showGrid(True, True)
total_data = []


def update():
    global stream, total_data, max_hold
    
    # read data
    raw_data = stream.read(CHUNK)
    
    # convert raw bytes into integers
    data_sample = np.fromstring(raw_data, dtype=np.int16)
    total_data = np.concatenate([total_data, data_sample ])
    
    # remove old data
    if len(total_data) > MAX_PLOT_SIZE:
        total_data = total_data[CHUNK:]
    time_curve.setData(total_data)
    
    # calculate the FFT
    fft_data = data_sample * np.hanning(len(data_sample))
    power_spectrum = 20 * np.log10(np.abs(np.fft.rfft(fft_data))/len(fft_data))
    fft_curve.setData(power_spectrum)
    fft_plot.enableAutoRange('xy', False)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start Qt Event
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()