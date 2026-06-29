from src.music_context_engine import build_music_context


def rank_events(events):
    """
    Rank events using all detector outputs.
    Final score = musical quality * vocal safety boost
    so vocal gaps enhance good transitions instead of replacing them.
    """

    ranked_events = []

    for event in events:

        bass = event.get("bass_strength", 0)
        energy = event.get("energy_strength", 0)
        rms = event.get("rms_strength", 0)
        sub808 = event.get("sub808_strength", 0)
        kick = event.get("kick_strength", 0)
        snare = event.get("snare_strength", 0)
        hihat = event.get("hihat_strength", 0)
        chord = event.get("chord_strength", 0)
        melody = event.get("melody_strength", 0)
        synth = event.get("synth_strength", 0)
        reverb = event.get("reverb_strength", 0)
        confidence = event.get("confidence", 0)
        vocal_gap_score = event.get("vocal_gap_score", 0)

        # Musical quality score
        musical_score = (
            bass     * 18 +
            energy   * 18 +
            rms      * 10 +
            sub808   * 10 +
            kick     * 10 +
            snare    *  8 +
            hihat    *  6 +
            chord    *  6 +
            melody   *  5 +
            synth    *  4 +
            reverb   *  2 +
            confidence * 3
        )

        # Vocal safety multiplier
        # 0.0 gap = no boost (x1.0)
        # 1.0 gap = 30% boost (x1.3)
        # This means vocal gaps enhance good transitions
        # but can't save a musically weak event
        vocal_multiplier = 1.0 + (vocal_gap_score * 0.3)

        score = musical_score * vocal_multiplier

        context = build_music_context(event)

        ranked_events.append({
            **event,
            "context": context,
            "score": round(score, 2)
        })

    ranked_events.sort(key=lambda x: x["score"], reverse=True)

    return ranked_events