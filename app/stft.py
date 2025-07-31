import scipy
from scipy.signal.windows import hamming
import numpy as np
import matplotlib.pyplot as plt 

def derive_m_and_n(img_array: np.ndarray) -> tuple:
    """
    STFT outputs a spectrogram with N columns and M rows
    """
    n = img_array.shape[1] #COL
    m = img_array.shape[0] # ROW
    return n,m


def divide_into_frames(signal: np.ndarray, window_size, overlap_ratio = 0.5):
    """
    Divides the sound into overlapping frames of equal length. 
    """
    HOP_LENGTH = int(window_size * (1 - overlap_ratio)) #no. of overlap samples
    window = hamming(window_size, sym=False)
    x_n = [] #np.ndarray
    for i in range(0, len(signal) - window_size +1, HOP_LENGTH):
        x = signal[i:i+window_size]
        windowed_frame = x*window
        x_n.append(windowed_frame)
    return x_n, HOP_LENGTH

def spectrogram(x_n) -> np.ndarray:
    dfts = [np.fft.fft(frame) for frame in x_n]
    spectrogram = np.column_stack(dfts) # Shape: (freq_bins, time_frames)
    print(spectrogram.shape)

    plt.figure(figsize=(10, 6))
    plt.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis')
    plt.title("Spectrogram")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.show()

    return spectrogram


