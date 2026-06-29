def calculate_transition_score(
    event1,
    event2,
    vocal_gap_score=0.0,
    similarity_score=0.0,
    bpm_score=0.0,
    harmonic_score=0.0
):
    """
    Calculates a transition score using real event
    features instead of placeholder values.
    """

    bass_score = (
        event1.get("bass_strength", 0) +
        event2.get("bass_strength", 0)
    ) / 2

    energy_score = (
        event1.get("energy_strength", 0) +
        event2.get("energy_strength", 0)
    ) / 2

    rms_score = (
        event1.get("rms_strength", 0) +
        event2.get("rms_strength", 0)
    ) / 2

    confidence_score = (
        event1.get("confidence", 0) +
        event2.get("confidence", 0)
    ) / 2

    score = (
        bass_score       * 25 +
        energy_score     * 20 +
        rms_score        * 10 +
        confidence_score * 10 +
        vocal_gap_score  * 15 +
        bpm_score        * 12 +
        harmonic_score   * 8  +
        similarity_score * 0
    )

    return round(score, 2)