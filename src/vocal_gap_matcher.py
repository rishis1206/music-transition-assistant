def calculate_vocal_gap_score(
    transition_time,
    gaps
):
    """
    Returns a vocal gap score between 0 and 1.
    """

    for gap in gaps:

        start = gap["start"]
        end = gap["end"]

        if start <= transition_time <= end:

            gap_length = end - start

            score = min(
                gap_length / 5,
                1.0
            )

            return round(score, 3)

    return 0.0


def is_inside_vocal_gap(
    transition_time,
    gaps
):
    return calculate_vocal_gap_score(
        transition_time,
        gaps
    ) > 0