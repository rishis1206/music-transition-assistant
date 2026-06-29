import librosa
import numpy as np


def detect_buildups(audio, sample_rate):
    """
    Detect gradual energy build-ups leading into drops.
    """

    rms = librosa.feature.rms(
        y=audio
    )[0]

    rms = rms / (np.max(rms) + 1e-8)

    buildup_scores = np.zeros_like(rms)

    window = 8

    for i in range(window, len(rms)):

        previous = np.mean(
            rms[i-window:i-4]
        )

        current = np.mean(
            rms[i-4:i]
        )

        increase = current - previous

        if increase > 0:

            buildup_scores[i] = increase

    buildup_scores = buildup_scores / (
        np.max(buildup_scores) + 1e-8
    )

    threshold = 0.50

    buildup_frames = np.where(
        buildup_scores >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        buildup_frames,
        sr=sample_rate
    )

    confidence = (
        np.mean(
            buildup_scores[buildup_frames]
        )
        if len(buildup_frames)
        else 0
    )

    return {

        "strength": round(
            float(np.mean(buildup_scores)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "confidence": round(
            float(confidence),
            3
        ),

        "energy_curve": buildup_scores.tolist()

    }