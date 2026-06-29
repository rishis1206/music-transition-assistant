import librosa
import numpy as np


def detect_kick(audio, sample_rate):
    """
    Detect kick drum hits using onset strength
    and low-frequency energy.
    """

    onset_env = librosa.onset.onset_strength(
        y=audio,
        sr=sample_rate
    )

    stft = np.abs(librosa.stft(audio))

    frequencies = librosa.fft_frequencies(
        sr=sample_rate
    )

    kick_band = stft[
        (frequencies >= 40)
        &
        (frequencies <= 150)
    ]

    kick_energy = np.mean(
        kick_band,
        axis=0
    )

    kick_energy = kick_energy / (
        np.max(kick_energy) + 1e-8
    )

    onset_env = onset_env / (
        np.max(onset_env) + 1e-8
    )

    combined = (
        kick_energy * 0.7
        +
        onset_env * 0.3
    )

    threshold = 0.60

    kick_frames = np.where(
        combined >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        kick_frames,
        sr=sample_rate
    )

    if len(kick_frames):

        confidence = np.mean(
            combined[kick_frames]
        )

    else:

        confidence = 0

    return {

        "strength": round(
            float(np.mean(combined)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "hits": len(kick_frames),

        "confidence": round(
            float(confidence),
            3
        ),

    "energy_curve": combined.tolist()

    }