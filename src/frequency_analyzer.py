import librosa
import numpy as np


def analyze_frequencies(audio, sample_rate):

    stft = np.abs(
        librosa.stft(audio)
    )

    frequencies = librosa.fft_frequencies(
        sr=sample_rate
    )

    def band(low, high=None):

        if high is None:

            mask = frequencies >= low

        else:

            mask = (
                (frequencies >= low)
                &
                (frequencies < high)
            )

        values = stft[mask]

        return {
            "energy": values.mean(axis=0),
            "average": float(np.mean(values)),
            "maximum": float(np.max(values))
        }

    return {

        "sub_bass": band(20, 60),

        "bass": band(60, 250),

        "low_mid": band(250, 500),

        "mids": band(500, 2000),

        "upper_mid": band(2000, 4000),

        "highs": band(4000),

        "spectral_centroid": float(
            np.mean(
                librosa.feature.spectral_centroid(
                    S=stft,
                    sr=sample_rate
                )
            )
        ),

        "spectral_bandwidth": float(
            np.mean(
                librosa.feature.spectral_bandwidth(
                    S=stft,
                    sr=sample_rate
                )
            )
        ),

        "spectral_rolloff": float(
            np.mean(
                librosa.feature.spectral_rolloff(
                    S=stft,
                    sr=sample_rate
                )
            )
        )

    }