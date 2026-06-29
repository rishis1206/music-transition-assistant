import librosa
import numpy as np


def detect_hihat(audio, sample_rate):
    """
    Detect hi-hats using high-frequency transients.
    """

    onset_env = librosa.onset.onset_strength(
        y=audio,
        sr=sample_rate
    )

    stft = np.abs(
        librosa.stft(audio)
    )

    frequencies = librosa.fft_frequencies(
        sr=sample_rate
    )

    hihat_band = stft[
        (frequencies >= 5000)
        &
        (frequencies <= 12000)
    ]

    hihat_energy = np.mean(
        hihat_band,
        axis=0
    )

    hihat_energy /= (
        np.max(hihat_energy) + 1e-8
    )

    onset_env /= (
        np.max(onset_env) + 1e-8
    )

    combined = (
        hihat_energy * 0.7
        +
        onset_env * 0.3
    )

    threshold = 0.55

    hihat_frames = np.where(
        combined >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        hihat_frames,
        sr=sample_rate
    )

    confidence = (
        np.mean(combined[hihat_frames])
        if len(hihat_frames)
        else 0
    )

    return {

        "strength": round(
            float(np.mean(combined)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "hits": len(hihat_frames),

        "confidence": round(
            float(confidence),
            3
        ),

    "energy_curve": combined.tolist()

    }