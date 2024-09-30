import pyedflib
import numpy as np
import matplotlib.pyplot as plt

# Function to read EDF file and return signals and metadata
def read_edf_signals(file_name):
    """
    Reads the EDF file and extracts signals along with their sampling frequencies.

    Args:
        file_name (str): The path to the EDF file.

    Returns:
        dict: A dictionary containing signal data, sampling frequencies, and labels.
    """
    f = pyedflib.EdfReader(file_name)
    n_signals = f.signals_in_file

    # Get signal labels
    signal_labels = f.getSignalLabels()
    print(f'Number of signals: {n_signals}')
    print('Signal labels:')
    for i in range(n_signals):
        print(f' {signal_labels[i]}')

    # Extract EEG signal and its frequency
    eeg_signal = f.readSignal(0)
    eeg_fs = f.getSampleFrequency(0)

    # Extract spindle signals and their frequencies
    spindle_1_signal = f.readSignal(1)
    spindle_1_fs = f.getSampleFrequency(1)

    spindle_2_signal = f.readSignal(2)
    spindle_2_fs = f.getSampleFrequency(2)

    f.close()

    return {
        'eeg': eeg_signal,
        'eeg_fs': eeg_fs,
        'spindle_1': spindle_1_signal,
        'spindle_1_fs': spindle_1_fs,
        'spindle_2': spindle_2_signal,
        'spindle_2_fs': spindle_2_fs,
        'labels': signal_labels
    }

# Function to interpolate spindles to match the EEG signal length
def interpolate_spindles(spindle_signal, target_length):
    """
    Interpolates spindle signals to match the EEG signal length.

    Args:
        spindle_signal (np.ndarray): The spindle signal to be interpolated.
        target_length (int): The target length (usually length of EEG signal).

    Returns:
        np.ndarray: The interpolated spindle signal.
    """
    original_indices = np.linspace(0, 1, num=len(spindle_signal))
    new_indices = np.linspace(0, 1, num=target_length)

    interpolated_signal = np.interp(new_indices, original_indices, spindle_signal)
    return interpolated_signal

# Function to plot results
def plot_signals(time, data, xlabel, ylabel, plot_title="Plot"):
    """
    Plots multiple signals on separate subplots.

    Args:
        time (np.ndarray): Time axis values.
        data (list): List of signals to plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        plot_title (str): Title of the plot.
    """
    plot_range = [435, 455]
    eeg_plot_y_range = [-40, 40]  # Fixed y-range for EEG plot

    print(f"Creating {len(data)} subplots.")
    
    plt.figure(figsize=(10, 8))

    for i in range(len(data)):
        plt.subplot(len(data), 1, i + 1)
        plt.plot(time, data[i], linewidth=0.5)

        # Adjust y-axis limits for EEG vs Spindle signals
        if np.max(data[i]) > 1:  # EEG signal
            plt.ylim(eeg_plot_y_range)
            plt.ylabel(ylabel)
        else:  # Spindle signals
            plt.ylim([0, 1.5])
            plt.ylabel(f"Spindles {i + 1}")

        plt.xlim(plot_range)
        plt.xlabel(xlabel)

    plt.suptitle(plot_title)
    plt.tight_layout()
    plt.show()

# Main function to process and plot the data
def main():
    file_name = './training_data/excerpt1.prep.edf'

    # Read the EDF file and extract the required signals
    edf_data = read_edf_signals(file_name)

    # Get EEG and spindle signals along with their sampling frequencies
    eeg = edf_data['eeg']
    eeg_fs = edf_data['eeg_fs']
    spindle_1 = edf_data['spindle_1']
    spindle_2 = edf_data['spindle_2']

    # Interpolate spindle signals to match the EEG length
    spindle_1_interp = interpolate_spindles(spindle_1, len(eeg))
    spindle_2_interp = interpolate_spindles(spindle_2, len(eeg))

    # Create time vector based on EEG sample frequency
    time = np.arange(len(eeg)) / eeg_fs

    # Plot EEG and interpolated spindle signals
    plot_signals(time, [eeg, spindle_1_interp, spindle_2_interp], "Time (s)", "EEG (mV)", "Raw Signals from EEG")

if __name__ == "__main__":
    main()