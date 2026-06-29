import librosa
import numpy as np


def detect_synth(audio, sample_rate):
    """
    Detect sustained synth/pad activity.
    """

    stft = np.abs(librosa.stft(audio))

    centroid = librosa.feature.spectral_centroid(
        S=stft,
        sr=sample_rate
    )[0]

    bandwidth = librosa.feature.spectral_bandwidth(
        S=stft,
        sr=sample_rate
    )[0]

    centroid /= np.max(centroid) + 1e-8
    bandwidth /= np.max(bandwidth) + 1e-8

    synth_score = (
        centroid * 0.45 +
        bandwidth * 0.55
    )

    threshold = 0.55

    synth_frames = np.where(
        synth_score >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        synth_frames,
        sr=sample_rate
    )

    confidence = (
        np.mean(synth_score[synth_frames])
        if len(synth_frames)
        else 0
    )

    return {

        "strength": round(
            float(np.mean(synth_score)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "confidence": round(
            float(confidence),
            3
        ),

        "energy_curve": synth_score.tolist()

    }