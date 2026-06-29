def find_vocal_gaps(segments, min_gap=1.0):
    """
    Find silent gaps between vocal phrases.
    These are the safe zones to transition.
    """

    gaps = []

    # Handle songs with no vocals at all
    if not segments:
        return gaps

    for i in range(len(segments) - 1):

        current_end = segments[i]["end"]
        next_start = segments[i + 1]["start"]
        gap_duration = next_start - current_end

        if gap_duration >= min_gap:

            gaps.append({
                "start": current_end,
                "end": next_start,
                "duration": round(gap_duration, 3)
            })

    return gaps


def get_vocal_gap_score(transition_time, gaps):
    """
    Returns 0.0 to 1.0.
    1.0 = transition lands perfectly inside a vocal gap.
    0.0 = transition cuts through active vocals.
    """

    for gap in gaps:

        if gap["start"] <= transition_time <= gap["end"]:

            # Longer gap = safer transition = higher score
            score = min(gap["duration"] / 5.0, 1.0)
            return round(score, 3)

    return 0.0


def is_vocal_safe(transition_time, gaps):
    """Returns True if transition time is inside a vocal gap."""
    return get_vocal_gap_score(transition_time, gaps) > 0