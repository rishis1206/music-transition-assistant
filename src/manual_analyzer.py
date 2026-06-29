def parse_timestamp(ts_string):
    """
    Convert MM:SS or raw seconds string to float seconds.
    Examples: "1:20" -> 80.0, "0:42" -> 42.0, "80" -> 80.0
    """
    ts_string = str(ts_string).strip()

    if ":" in ts_string:
        parts = ts_string.split(":")
        try:
            minutes = int(parts[0])
            seconds = float(parts[1])
            return round(minutes * 60 + seconds, 2)
        except:
            return 0.0
    else:
        try:
            return round(float(ts_string), 2)
        except:
            return 0.0


def seconds_to_mmss(seconds):
    """
    Convert float seconds to MM:SS string.
    Examples: 80.0 -> "1:20", 42.5 -> "0:42"
    """
    seconds = float(seconds)
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:05.2f}"


def get_event_at_time(ranked_events, target_time, tolerance=3.0):
    """
    Find the closest event to a given timestamp within tolerance.
    If nothing found within tolerance, build a synthetic event.
    """

    best_event = None
    best_diff = float("inf")

    for event in ranked_events:
        diff = abs(event["time"] - target_time)
        if diff < best_diff:
            best_diff = diff
            best_event = event

    if best_event and best_diff <= tolerance:
        return best_event

    # Build synthetic event at exact timestamp
    return {
        "time": target_time,
        "type": "Manual Point",
        "bass_strength": 0.0,
        "energy_strength": 0.0,
        "rms_strength": 0.0,
        "sub808_strength": 0.0,
        "kick_strength": 0.0,
        "snare_strength": 0.0,
        "hihat_strength": 0.0,
        "chord_strength": 0.0,
        "melody_strength": 0.0,
        "synth_strength": 0.0,
        "reverb_strength": 0.0,
        "drop_strength": 0.0,
        "buildup_strength": 0.0,
        "confidence": 0.0,
        "vocal_gap_score": 0.0,
        "vocal_safe": False,
        "raw_features": {
            "bass_energy": 0.0,
            "energy_change": 0.0,
            "rms": 0.0
        }
    }


def evaluate_manual_transition(event1, event2, bpm_score, harmonic_score, similarity_score):
    """
    Evaluate a manually selected transition pair.
    Returns quality score and detailed feedback.
    """

    bass_score = (event1.get("bass_strength", 0) + event2.get("bass_strength", 0)) / 2
    energy_score = (event1.get("energy_strength", 0) + event2.get("energy_strength", 0)) / 2
    confidence_score = (event1.get("confidence", 0) + event2.get("confidence", 0)) / 2
    vocal_gap_score = (event1.get("vocal_gap_score", 0) + event2.get("vocal_gap_score", 0)) / 2

    musical_score = (
        bass_score * 25 +
        energy_score * 20 +
        confidence_score * 15 +
        vocal_gap_score * 15 +
        bpm_score * 12 +
        harmonic_score * 8 +
        similarity_score * 5
    )

    vocal_multiplier = 1.0 + (event1.get("vocal_gap_score", 0) * 0.3)
    final_score = musical_score * vocal_multiplier

    # Quality label
    if final_score >= 70:
        quality = "Excellent"
        quality_color = "#44FF88"
    elif final_score >= 50:
        quality = "Good"
        quality_color = "#FF8C00"
    elif final_score >= 30:
        quality = "Fair"
        quality_color = "#FFAA44"
    else:
        quality = "Weak"
        quality_color = "#FF4444"

    return {
        "score": round(final_score, 2),
        "quality": quality,
        "quality_color": quality_color
    }