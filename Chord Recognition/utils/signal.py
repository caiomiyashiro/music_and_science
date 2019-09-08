import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa, librosa.display

from scipy.signal import stft

COL_NAMES_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def plot_signal(signal, Fs, title, xlabel, ylabel):
    time_axis = np.arange(0, len(signal)/Fs, 1/Fs)
    plt.plot(time_axis, signal)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

# https://stackoverflow.com/questions/4364823/how-do-i-obtain-the-frequencies-of-each-value-in-an-fft/4371627#4371627
# https://www.mathworks.com/help/matlab/ref/fft.html
# https://www.physicsforums.com/threads/what-is-fft-frequency-resolution.650931/

def plot_spectra(signal, Fs, title="", xlabel="", ylabel="", max_freq=None):
    if(len(signal) % 2 != 0):
        signal = signal[:-1]

    n_half = int(len(signal)/2)

    transform = np.abs(np.fft.fft(signal)[:n_half])        # perform transformation and get first half points
    transform = transform/int(len(signal)/2)               # normalise

    # x-axis calculation
    freqs= Fs*np.arange(len(signal))/len(signal)
    freqs = freqs[:n_half]                                 # first half of the frequencies

    plt.plot(freqs, transform)
    plt.ylabel('Amplitude');
    plt.xlabel('Frequency (Hz)');
    if max_freq is None:
        max_x = Fs/2
    else:
        max_x = max_freq
    plt.xlim([0, max_x])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel);

# https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/
def stft_audio(signal, Fs, print_fft=False):
    window_length_ms = 24
    window_length_points = int(window_length_ms*Fs/1000) # 3 rule

    f, t, Zxx = stft(signal, Fs, nperseg=window_length_points)

    MIN_HZ = 700
    MAX_HZ = 3000
    hz_filter = (f > MIN_HZ) & (f < MAX_HZ)
    f = f[hz_filter]
    Zxx = np.abs(Zxx)[hz_filter]

    t_total = len(signal)/Fs
    t = np.linspace(0, t_total, len(Zxx[0]))

    if(print_fft == True):
        plt.pcolormesh(t, f, Zxx, vmin=0, vmax=np.max(Zxx))
        plt.title('STFT Magnitude')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]');

    return (f, t, Zxx)

# Constants for calc_chromagram
# FFT_SIZE = 4096
# HOP_SIZE = 1024
def calc_chromagram(x, Fs, plot=True):
    C = librosa.feature.chroma_stft(y=x, sr=Fs, tuning=0, norm=2, hop_length=1024, n_fft=4096)

    if(plot==True):
        plt.figure(figsize=(12, 3))
        plt.title('Chromagram $\mathcal{C}$')
        librosa.display.specshow(C, x_axis='time', y_axis='chroma', cmap='gray_r', hop_length=1024)
        plt.xlabel('Time (frames)'); plt.ylabel('Chroma')
        plt.colorbar(); plt.clim([0, 1])
        plt.tight_layout()
    return C

def get_frame_stats(chromagram, signal, Fs):
    frames_per_sec = chromagram.shape[1]/(len(signal)/Fs) # Nbr of frames / length in seconds = frames per second
    frame_duration_sec = 1/frames_per_sec        # frame duration = 1 / frames per second
    return [frames_per_sec, frame_duration_sec]

def chromagram_2_dataframe(chromagram, frame_duration_sec):
    chromagram = pd.DataFrame(np.transpose(chromagram), columns=COL_NAMES_NOTES)

    chromagram['start'] = np.arange(chromagram.shape[0]) * frame_duration_sec
    chromagram['end'] = chromagram['start'] + frame_duration_sec
    return chromagram

def __get_chord_ix(elem, chords_annotation):
    diffs = chords_annotation['start'] - elem
    return diffs[diffs <= 0].index[-1]

def get_annotated_chord_sequence(pcp, chords_annotation):
    chord_ix = pcp['start'].apply(lambda elem: __get_chord_ix(elem, chords_annotation))
    return chords_annotation.iloc[chord_ix.values]['chord'].values    
