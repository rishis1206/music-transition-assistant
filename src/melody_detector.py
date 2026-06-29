import librosa
import numpy as np


def detect_melody(audio, sample_rate):
    """
    Detect melodic activity using spectral centroid.
    """

    centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sample_rate
    )[0]

    normalized = centroid / (
        np.max(centroid) + 1e-8
    )

    threshold = 0.55

    melody_frames = np.where(
        normalized >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        melody_frames,
        sr=sample_rate
    )

    confidence = (
        np.mean(normalized[melody_frames])
        if len(melody_frames)
        else 0
    )

    return {

        "strength": round(
            float(np.mean(normalized)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "confidence": round(
            float(confidence),
            3
        ),

        "energy_curve": normalized.tolist()

    }