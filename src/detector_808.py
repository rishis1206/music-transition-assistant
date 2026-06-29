import librosa
import numpy as np


def detect_808(audio, sample_rate):
    """
    Detect sustained 808/sub-bass energy.

    Returns:
    {
        "strength": float,
        "timestamps": [...],
        "confidence": float
    }
    """

    stft = np.abs(librosa.stft(audio))

    frequencies = librosa.fft_frequencies(
        sr=sample_rate
    )

    sub_mask = (
        (frequencies >= 20)
        &
        (frequencies <= 60)
    )

    sub_band = stft[sub_mask]

    frame_energy = np.mean(
        sub_band,
        axis=0
    )

    max_energy = np.max(frame_energy)

    if max_energy == 0:

        return {
            "strength": 0.0,
            "timestamps": [],
            "confidence": 0.0
        }

    normalized = frame_energy / max_energy

    threshold = 0.65

    active_frames = np.where(
        normalized >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        active_frames,
        sr=sample_rate
    )

    strength = np.mean(normalized)

    confidence = np.mean(
        normalized[active_frames]
    ) if len(active_frames) else 0

    return {

        "strength": round(
            float(strength),
            3
        ),

        "timestamps": timestamps.tolist(),

        "confidence": round(
            float(confidence),
            3
        ),

    "energy_curve": normalized.tolist()

    }