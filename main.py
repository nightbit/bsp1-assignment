import pyedflib
import numpy as np
from pyedflib import EdfReader
import matplotlib.pyplot as plt

def plot_results(time, data, xlabel, ylabel, plot_title = "Plot"):
    plot_range = [435, 455]
    plot_y_range = [-40, 40]

    print(f"Creating {len(data)} subplots.")

    for i in range(len(data)):
        plt.subplot(len(data), 1, i + 1)
        plt.plot(time, data[i], linewidth=0.5)
        if np.max(data[i]) > 1:
            plt.ylim(plot_y_range)
            plt.ylabel(ylabel)
        else:
            # we can be certain we have a spindle signal
            plt.ylim([0, 1.5])
            plt.ylabel(f"Spindles {i}")

        plt.xlim(plot_range)
        plt.xlabel(xlabel)


    plt.suptitle(plot_title)
    plt.tight_layout()
    plt.show()

# Reading EDF data
file_name = './training_data/excerpt1.prep.edf'
f = EdfReader(file_name)
n = f.signals_in_file
print(f'Number signals: {n}')
signal_labels = f.getSignalLabels()
print('Signal labels:')
for i in range(n):
    print(f' {signal_labels[i]}')

# Read specific signal (eeg)
eeg_fs = f.getSampleFrequency(0)
eeg = f.readSignal(0)

# read sleep spindles signal
spindles_1 = f.readSignal(1)
spindles_1_fs = f.getSampleFrequency(1)
spindles_2 = f.readSignal(2)
spindles_2_fs = f.getSampleFrequency(2)

# interpolate to length of eeg signal because sampling frequency is 10 instead of 100
original_indices = np.linspace(0, 1, num=len(spindles_1))
new_indices = np.linspace(0, 1, num=len(eeg))

spindles_1_interp = np.interp(new_indices, original_indices, spindles_1)
spindles_2_interp = np.interp(new_indices, original_indices, spindles_2)

t = np.divide(range(len(eeg)), eeg_fs)

plot_results(t, [eeg, spindles_1_interp, spindles_2_interp], "Time (s)", "EEG (mV)", "Raw Signals from EEG")