import librosa
import numpy as np
from scipy.signal import find_peaks

def analyze_bass(audio, sample_rate):

    stft = np.abs(
        librosa.stft(audio)
    )

    frequencies = librosa.fft_frequencies(
        sr=sample_rate
    )

    bass_mask = frequencies <= 250

    bass_energy = stft[
        bass_mask
    ].mean(axis=0)

    bass_times = librosa.times_like(
        bass_energy,
        sr=sample_rate
    )

    bass_peaks, _ = find_peaks(
        bass_energy,
        distance=20
    )

    return {
        "bass_energy": bass_energy,
        "bass_times": bass_times,
        "bass_peaks": bass_peaks
    }