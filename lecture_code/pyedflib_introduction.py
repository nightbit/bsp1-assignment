import pyedflib
import numpy as np
from pyedflib import EdfReader
import matplotlib.pyplot as plt


# Reading EDF data
file_name = './s3_run.edf'
f = EdfReader(file_name)
n = f.signals_in_file
print(f'Number signals: {n}')
signal_labels = f.getSignalLabels()
print('Signal labels:')
for i in range(n):
    print(f' {signal_labels[i]}')

# Read specific signal (wrist_ppg)
ecg_fs = f.getSampleFrequency(0)
ecg = f.readSignal(0)
print(f'ECG fs: {ecg_fs}\nECG len: {len(ecg)}\nECG len(s): {len(ecg) / ecg_fs}')
ppg_fs = f.getSampleFrequency(1)
ppg = f.readSignal(1)
print(f'PPG fs: {ppg_fs}\nPPG len: {len(ppg)}\nPPG len(s): {len(ppg) / ppg_fs}')

t = np.divide(range(len(ecg)), ecg_fs)
print(t)
# plot_range = [0, t[-1]]
plot_range = [50, 100]

plt.subplot(2, 1, 1)
plt.plot(t, ecg, linewidth=0.5)
plt.xlabel('Time (s)')
plt.ylabel('ECG (\u03bcV)')
plt.xlim(plot_range)
plt.title('Raw signals from EDF and spectral analysis')
plt.tight_layout()

plt.subplot(2, 1, 2)
plt.plot(t, ppg, linewidth=0.5)
plt.xlabel('Time (s)')
plt.ylabel('PPG')
plt.xlim(plot_range)
plt.tight_layout()
plt.show()
