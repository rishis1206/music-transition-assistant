import librosa
import numpy as np


def detect_reverb(audio, sample_rate):
    """
    Estimate reverb amount from spectral decay.
    """

    stft = np.abs(librosa.stft(audio))

    decay = np.diff(
        stft,
        axis=1
    )

    decay = np.abs(decay)

    reverb_curve = np.mean(
        decay,
        axis=0
    )

    reverb_curve /= (
        np.max(reverb_curve) + 1e-8
    )

    threshold = 0.45

    reverb_frames = np.where(
        reverb_curve <= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        reverb_frames,
        sr=sample_rate
    )

    confidence = (
        1 -
        np.mean(reverb_curve[reverb_frames])
    ) if len(reverb_frames) else 0

    return {

        "strength": round(
            float(1 - np.mean(reverb_curve)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "confidence": round(
            float(confidence),
            3
        ),

        "energy_curve": reverb_curve.tolist()

    }