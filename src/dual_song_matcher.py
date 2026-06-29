from src.transition_scorer import calculate_transition_score
from src.bpm_compatibility import calculate_bpm_score
from src.harmonic_compatibility import calculate_harmonic_score


def find_best_match(song1_events, song2_events, bpm1=0, bpm2=0, chroma1=None, chroma2=None):
    """
    Compare every event in Song 1 with every event in Song 2
    and rank the best transition pairs by score.
    Now includes BPM and harmonic compatibility.
    """

    # Calculate song-level compatibility scores once
    bpm_score = calculate_bpm_score(bpm1, bpm2)
    harmonic_score = calculate_harmonic_score(chroma1, chroma2)

    matches = []

    for event1 in song1_events:

        for event2 in song2_events:

            vocal_gap_score = (
                event1.get("vocal_gap_score", 0) +
                event2.get("vocal_gap_score", 0)
            ) / 2

            final_score = calculate_transition_score(
                event1,
                event2,
                vocal_gap_score=vocal_gap_score,
                bpm_score=bpm_score,
                harmonic_score=harmonic_score
            )

            matches.append({
                "song1_time": event1["time"],
                "song2_time": event2["time"],
                "event_type": f"{event1['type']} → {event2['type']}",
                "score": final_score,
                "song1_confidence": event1.get("confidence", 0),
                "song2_confidence": event2.get("confidence", 0),
                "song1_bass": event1.get("bass_strength", 0),
                "song2_bass": event2.get("bass_strength", 0),
                "song1_energy": event1.get("energy_strength", 0),
                "song2_energy": event2.get("energy_strength", 0),
                "song1_type": event1["type"],
                "song2_type": event2["type"],
                "bpm_score": round(bpm_score, 3),
                "harmonic_score": round(harmonic_score, 3)
            })

    matches.sort(key=lambda x: x["score"], reverse=True)

    return matches[:10]