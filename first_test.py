import pyedflib
import numpy as np
from pyedflib import EdfReader
import matplotlib.pyplot as plt


# Reading EDF data
file_name = './training_data/excerpt1.prep.edf'
f = EdfReader(file_name)
n = f.signals_in_file
print(f'Number signals: {n}')
signal_labels = f.getSignalLabels()
print('Signal labels:')
for i in range(n):
    print(f' {signal_labels[i]}')

# Read specific signal (wrist_ppg)
eeg_fs = f.getSampleFrequency(0)
eeg = f.readSignal(0)
print(f'EEG fs: {eeg_fs}\nEEG len: {len(eeg)}\nEEG len(s): {len(eeg) / eeg_fs}')


t = np.divide(range(len(eeg)), eeg_fs)
print(len(t))

plot_range = [0, 20]
plot_y_range = [-40, 40]

plt.plot(t, eeg, linewidth=0.5)
plt.xlabel('Time (s)')
plt.ylabel('ECG (\u03bcV)')
plt.xlim(plot_range)
plt.ylim(plot_y_range)
plt.title('Raw signals from EDF and spectral analysis')
plt.tight_layout()
plt.show()