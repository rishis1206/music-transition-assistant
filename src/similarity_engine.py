def calculate_similarity(features1, features2):
    """
    Calculate normalized similarity score (0-1)
    between two songs.
    """

    weights = {
        "sub_bass": 0.25,
        "bass": 0.30,
        "mids": 0.25,
        "highs": 0.20
    }

    similarity = 0

    for band, weight in weights.items():

        difference = abs(
            features1.get(band, 0)
            -
            features2.get(band, 0)
        )

        band_similarity = max(
            0,
            1 - difference
        )

        similarity += band_similarity * weight

    return round(similarity, 3)