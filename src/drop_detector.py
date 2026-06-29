import librosa
import numpy as np


def detect_drops(audio, sample_rate):
    """
    Detect major musical drops using energy changes.
    """

    rms = librosa.feature.rms(
        y=audio
    )[0]

    rms = rms / (np.max(rms) + 1e-8)

    energy_change = np.diff(
        rms,
        prepend=rms[0]
    )

    drop_scores = np.zeros_like(rms)

    for i in range(2, len(rms) - 2):

        before = np.mean(
            rms[i-2:i]
        )

        after = np.mean(
            rms[i:i+2]
        )

        increase = after - before

        if increase > 0:

            drop_scores[i] = increase

    drop_scores = drop_scores / (
        np.max(drop_scores) + 1e-8
    )

    threshold = 0.55

    drop_frames = np.where(
        drop_scores >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        drop_frames,
        sr=sample_rate
    )

    confidence = (
        np.mean(
            drop_scores[drop_frames]
        )
        if len(drop_frames)
        else 0
    )

    return {

        "strength": round(
            float(
                np.mean(drop_scores)
            ),
            3
        ),

        "timestamps": timestamps.tolist(),

        "confidence": round(
            float(confidence),
            3
        ),

        "energy_curve": drop_scores.tolist()

    }