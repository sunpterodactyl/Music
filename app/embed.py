from scipy.io import wavfile
import numpy as np
import matplotlib.image as mpimg
from scipy.fft import fft2, ifft2
import subprocess
from stft import divide_into_frames, spectrogram
from scipy.signal import istft
from scipy.io.wavfile import write


def read_music_data(music: str):
    """
    Read music data from a given source.

    Parameters:
    - music: wav file path

    Returns: Parsed music data.
    """
    # Implementation to read and parse the music data

    sr, audio = wavfile.read(music)
    if len(audio.shape) > 1 and audio.shape[1] == 2:
        # Convert stereo to mono by averaging channels
        audio = np.mean(audio, axis=1)
    
    return sr, audio



def read_image_data(image_path):
    """
    Read image data from a given file path.

    Parameters:
    - image_path: Path to the image file.

    Returns: 2D array representing the image data.
    """
    img = mpimg.imread(image_path)
    return img

def convert_mp4_to_wav(input_path, output_path):
    try:
        result = subprocess.run(
            ["ffmpeg","-i", input_path, output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)

img_arr = read_image_data('app/test_audio/bird.jpg')
#convert_mp4_to_wav('app/test_audio/SoundOfSilence.m4a', 'app/test_audio/SoundOfSilence.wav')
samplerate, musicarray = read_music_data('app/test_audio/SoundOfSilence.wav')

print(img_arr.shape) #Image capacity is 4032 x 3024 x 3 = 36.6M pixels
print(len(musicarray))  #time domain signal x(t)

spec_trial = spectrogram(divide_into_frames(musicarray, 4032))


###WRITTEN BY CHATGPT TEST FIRST 

def reconstruct_audio_from_spectrogram(magnitude_spectrogram, sample_rate, window_size, n_iter=100, overlap_ratio=0.50):

    hop_length = int(window_size * (1 - overlap_ratio))
    # Collapse overlapping frames using ISTFT
    _, time_signal_out = istft(magnitude_spectrogram, fs=sample_rate, window="hamming", nperseg=window_size, noverlap=window_size - hop_length, input_onesided=False)
    
    # Normalize
    if np.max(np.abs(time_signal_out)) > 0:
        time_signal_out = time_signal_out / np.max(np.abs(time_signal_out))

    return time_signal_out


reconstructed_audio = reconstruct_audio_from_spectrogram(spec_trial, samplerate, 4032)
reconstructed_audio = np.real(reconstructed_audio)
write("reconstructed.wav", 44100, (reconstructed_audio * 32767).astype(np.int16))
print(reconstructed_audio.shape)
print(f"First 10 samples - Original: {musicarray[:10]}")
print(f"First 10 samples - Reconstructed: {reconstructed_audio[:10]}")