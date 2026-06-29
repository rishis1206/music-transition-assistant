import numpy as np

# Camelot wheel compatibility map
# Keys that mix well together get high scores
CAMELOT_COMPATIBLE = {
    0:  [0, 1, 11, 7],   # C  major
    1:  [1, 2, 0, 8],    # C# major
    2:  [2, 3, 1, 9],    # D  major
    3:  [3, 4, 2, 10],   # Eb major
    4:  [4, 5, 3, 11],   # E  major
    5:  [5, 6, 4, 0],    # F  major
    6:  [6, 7, 5, 1],    # F# major
    7:  [7, 8, 6, 2],    # G  major
    8:  [8, 9, 7, 3],    # Ab major
    9:  [9, 10, 8, 4],   # A  major
    10: [10, 11, 9, 5],  # Bb major
    11: [11, 0, 10, 6],  # B  major
}


def get_dominant_key(chroma):
    """Get the dominant pitch class from chroma vector."""
    if chroma is None or len(chroma) == 0:
        return 0
    return int(np.argmax(chroma))


def calculate_harmonic_score(chroma1, chroma2):
    """
    Returns 0.0 to 1.0 based on harmonic compatibility.
    Uses chroma vectors to determine musical key compatibility.
    """

    if chroma1 is None or chroma2 is None:
        return 0.5  # unknown, neutral score

    key1 = get_dominant_key(chroma1)
    key2 = get_dominant_key(chroma2)

    compatible_keys = CAMELOT_COMPATIBLE.get(key1, [])

    if key2 == key1:
        # Same key — perfect
        return 1.0
    elif key2 in compatible_keys:
        # Compatible key — good
        return 0.8
    else:
        # Calculate distance on circle of fifths
        distance = min(
            abs(key1 - key2),
            12 - abs(key1 - key2)
        )
        # Further apart = worse score
        return round(max(0.0, 1.0 - distance * 0.15), 3)