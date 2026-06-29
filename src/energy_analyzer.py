import librosa
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

def analyze_energy(audio, sample_rate):

    rms = librosa.feature.rms(
        y=audio
    )[0]

    times = librosa.times_like(
        rms,
        sr=sample_rate
    )

    peaks, _ = find_peaks(
        rms,
        distance=20
    )

    energy_change = []

    for i in range(1, len(rms)):
        energy_change.append(
            rms[i] - rms[i - 1]
        )

    largest_changes = sorted(
        range(len(energy_change)),
        key=lambda i: energy_change[i],
        reverse=True
    )

    smoothed_energy = gaussian_filter1d(
        rms,
        sigma=10
    )

    section_changes = []

    for i in range(
        1,
        len(smoothed_energy)
    ):

        diff = abs(
            smoothed_energy[i]
            - smoothed_energy[i - 1]
        )

        section_changes.append(
            diff
        )

    section_points = sorted(
        range(len(section_changes)),
        key=lambda i: section_changes[i],
        reverse=True
    )

    section_points = sorted(
        section_points[:5]
    )

    return {
        "rms": rms,
        "times": times,
        "peaks": peaks,
        "energy_change": energy_change,
        "largest_changes": largest_changes,
        "section_points": section_points
    }