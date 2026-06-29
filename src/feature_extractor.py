import librosa
import numpy as np


def extract_features(audio, sample_rate):
    """
    Extract frequency-domain and musical features
    used throughout the AI pipeline.
    """

    stft = np.abs(librosa.stft(audio))

    frequencies = librosa.fft_frequencies(
        sr=sample_rate
    )

    rms = librosa.feature.rms(S=stft)[0]

    spectral_centroid = librosa.feature.spectral_centroid(
        S=stft,
        sr=sample_rate
    )[0]

    spectral_bandwidth = librosa.feature.spectral_bandwidth(
        S=stft,
        sr=sample_rate
    )[0]

    spectral_rolloff = librosa.feature.spectral_rolloff(
        S=stft,
        sr=sample_rate
    )[0]

    zero_crossing_rate = librosa.feature.zero_crossing_rate(
        audio
    )[0]

    chroma = librosa.feature.chroma_stft(
        S=stft,
        sr=sample_rate
    )

    features = {}

    # Frequency bands
    features["sub_bass"] = float(np.mean(
        stft[
            (frequencies >= 20)
            &
            (frequencies < 60)
        ]
    ))

    features["bass"] = float(np.mean(
        stft[
            (frequencies >= 60)
            &
            (frequencies < 250)
        ]
    ))

    features["low_mid"] = float(np.mean(
        stft[
            (frequencies >= 250)
            &
            (frequencies < 500)
        ]
    ))

    features["mids"] = float(np.mean(
        stft[
            (frequencies >= 500)
            &
            (frequencies < 2000)
        ]
    ))

    features["upper_mid"] = float(np.mean(
        stft[
            (frequencies >= 2000)
            &
            (frequencies < 4000)
        ]
    ))

    features["highs"] = float(np.mean(
        stft[
            frequencies >= 4000
        ]
    ))

    # Musical descriptors
    features["rms"] = float(np.mean(rms))

    features["spectral_centroid"] = float(
        np.mean(spectral_centroid)
    )

    features["spectral_bandwidth"] = float(
        np.mean(spectral_bandwidth)
    )

    features["spectral_rolloff"] = float(
        np.mean(spectral_rolloff)
    )

    features["zero_crossing_rate"] = float(
        np.mean(zero_crossing_rate)
    )

    # Harmonic information
    features["chroma"] = np.mean(
        chroma,
        axis=1
    ).tolist()

    return features