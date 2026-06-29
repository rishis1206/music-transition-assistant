import librosa
import numpy as np


def detect_chords(audio, sample_rate):
    """
    Detect chord activity using chroma variance.
    Real chords have energy spread across multiple
    pitch classes — pure melody or drums do not.
    """

    chroma = librosa.feature.chroma_stft(
        y=audio,
        sr=sample_rate
    )

    # Variance across pitch classes per frame
    # High variance = energy concentrated in few notes (melody/drums)
    # Low variance = energy spread across many notes (chords/pads)
    chroma_variance = np.var(chroma, axis=0)

    # Invert so high score = more chord-like
    chord_strength = 1.0 - (
        chroma_variance / (np.max(chroma_variance) + 1e-8)
    )

    # Also require minimum overall chroma energy
    # so silence doesn't score as chords
    chroma_energy = np.mean(chroma, axis=0)
    chroma_energy /= (np.max(chroma_energy) + 1e-8)

    # Combine: must have spread AND actual energy
    chord_strength = chord_strength * chroma_energy

    threshold = 0.55

    chord_frames = np.where(
        chord_strength >= threshold
    )[0]

    timestamps = librosa.frames_to_time(
        chord_frames,
        sr=sample_rate
    )

    confidence = (
        np.mean(chord_strength[chord_frames])
        if len(chord_frames)
        else 0
    )

    return {

        "strength": round(
            float(np.mean(chord_strength)),
            3
        ),

        "timestamps": timestamps.tolist(),

        "confidence": round(
            float(confidence),
            3
        ),

        "chroma": np.mean(
            chroma,
            axis=1
        ).tolist(),

        "energy_curve": chord_strength.tolist()

    }