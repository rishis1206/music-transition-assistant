import librosa
import numpy as np


def detect_snare(audio, sample_rate):
    """
    Detect snare drum hits using transient energy
    in the mid-frequency range.
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

    snare_band = stft[
        (frequencies >= 180)
        &
        (frequencies <= 2500)
    ]

    snare_energy = np.mean(
        snare_band,
        axis=0
    )

    snare_energy /= (
        np.max(snare_energy) + 1e-8
    )

    onset_env /= (
        np.max(onset_env) + 1e-8
    )

    combined = (
        snare_energy * 0.6
        +
        onset_env * 0.4
    )

    threshold = 0.58

    snare_frames = np.where(
        combined >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        snare_frames,
        sr=sample_rate
    )

    confidence = (
        np.mean(combined[snare_frames])
        if len(snare_frames)
        else 0
    )

    return {

        "strength": round(
            float(np.mean(combined)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "hits": len(snare_frames),

        "confidence": round(
            float(confidence),
            3
        ),

    "energy_curve": combined.tolist()

    }