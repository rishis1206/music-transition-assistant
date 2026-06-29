import numpy as np


def normalize(value, minimum, maximum):

    if maximum - minimum == 0:
        return 0.0

    score = (value - minimum) / (maximum - minimum)

    return float(np.clip(score, 0.0, 1.0))


def safe_curve_value(curve, index):

    if curve is None:
        return 0.0

    if len(curve) == 0:
        return 0.0

    if index >= len(curve):
        index = len(curve) - 1

    return float(curve[index])


def classify_events(
    largest_changes,
    times,
    bass_peaks,
    bass_times,
    bass_energy,
    energy_change,
    rms,
    detector808,
    kick,
    snare,
    hihat,
    chord,
    melody,
    synth,
    reverb,
    drop_data,
    buildup_data,
    vocal_gaps=None
):

    if vocal_gaps is None:
        vocal_gaps = []

    events = []

    max_bass = np.max(bass_energy)
    min_bass = np.min(bass_energy)

    max_energy = np.max(energy_change)
    min_energy = np.min(energy_change)

    max_rms = np.max(rms)
    min_rms = np.min(rms)

    for drop_idx in largest_changes[:20]:

        if drop_idx >= len(times):
            continue

        drop_time = times[drop_idx]

        # --- Bass strength ---
        bass_strength = 0.0
        bass_raw = 0.0

        for peak in bass_peaks:

            if peak >= len(bass_times):
                continue

            bass_time = bass_times[peak]

            if abs(drop_time - bass_time) < 1.0:

                bass_raw = float(bass_energy[peak])

                bass_strength = normalize(
                    bass_raw,
                    min_bass,
                    max_bass
                )

                break

        # --- Energy strength ---
        energy_raw = float(energy_change[drop_idx])

        energy_strength = normalize(
            energy_raw,
            min_energy,
            max_energy
        )

        # --- RMS strength ---
        rms_raw = float(rms[drop_idx])

        rms_strength = normalize(
            rms_raw,
            min_rms,
            max_rms
        )

        # --- Component strengths ---
        sub808_strength = safe_curve_value(detector808["energy_curve"], drop_idx)
        kick_strength = safe_curve_value(kick["energy_curve"], drop_idx)
        snare_strength = safe_curve_value(snare["energy_curve"], drop_idx)
        hihat_strength = safe_curve_value(hihat["energy_curve"], drop_idx)
        chord_strength = safe_curve_value(chord["energy_curve"], drop_idx)
        melody_strength = safe_curve_value(melody["energy_curve"], drop_idx)
        synth_strength = safe_curve_value(synth["energy_curve"], drop_idx)
        reverb_strength = safe_curve_value(reverb["energy_curve"], drop_idx)
        drop_strength = safe_curve_value(drop_data["energy_curve"], drop_idx)
        buildup_strength = safe_curve_value(buildup_data["energy_curve"], drop_idx)

        # --- Confidence score ---
        confidence = (
            bass_strength * 0.25 +
            energy_strength * 0.20 +
            rms_strength * 0.10 +
            sub808_strength * 0.10 +
            kick_strength * 0.08 +
            snare_strength * 0.07 +
            hihat_strength * 0.05 +
            chord_strength * 0.05 +
            melody_strength * 0.04 +
            synth_strength * 0.03 +
            reverb_strength * 0.03
        )

        # --- Vocal gap score ---
        vocal_gap_score = 0.0
        vocal_safe = False

        for gap in vocal_gaps:
            if gap["start"] <= drop_time <= gap["end"]:
                vocal_gap_score = min(gap["duration"] / 5.0, 1.0)
                vocal_safe = True
                break

        # ==========================
        # DETERMINE EVENT TYPE
        # ==========================

        event_scores = {
            "Drop": (drop_strength * 0.50 + kick_strength * 0.30 + energy_strength * 0.20),
            "Build-up": (buildup_strength * 0.50 + energy_strength * 0.30 + melody_strength * 0.20),
            "Synth Lead": (synth_strength * 0.60 + melody_strength * 0.40),
            "Chord Progression": (chord_strength * 0.70 + melody_strength * 0.30),
            "Atmospheric": (reverb_strength * 0.70 + synth_strength * 0.30),
            "Rhythmic Groove": (kick_strength * 0.40 + snare_strength * 0.30 + hihat_strength * 0.30),
            "Melodic Section": (melody_strength)
        }

        event_type = max(event_scores, key=event_scores.get)

        events.append({
            "time": round(drop_time, 2),
            "type": event_type,
            "bass_strength": round(bass_strength, 3),
            "energy_strength": round(energy_strength, 3),
            "rms_strength": round(rms_strength, 3),
            "sub808_strength": round(sub808_strength, 3),
            "kick_strength": round(kick_strength, 3),
            "snare_strength": round(snare_strength, 3),
            "hihat_strength": round(hihat_strength, 3),
            "chord_strength": round(chord_strength, 3),
            "melody_strength": round(melody_strength, 3),
            "synth_strength": round(synth_strength, 3),
            "reverb_strength": round(reverb_strength, 3),
            "drop_strength": round(drop_strength, 3),
            "buildup_strength": round(buildup_strength, 3),
            "confidence": round(confidence, 3),
            "vocal_gap_score": round(vocal_gap_score, 3),
            "vocal_safe": vocal_safe,
            "raw_features": {
                "bass_energy": round(bass_raw, 3),
                "energy_change": round(energy_raw, 3),
                "rms": round(rms_raw, 3)
            }
        })

    # ==========================
    # INJECT VOCAL GAP EVENTS
    # ==========================

    for gap in vocal_gaps:
        mid_point = (gap["start"] + gap["end"]) / 2

        events.append({
            "time": round(mid_point, 2),
            "type": "Vocal Gap",
            "bass_strength": 0.0,
            "energy_strength": 0.5,
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
            "confidence": 0.5,
            "vocal_gap_score": round(min(gap["duration"] / 5.0, 1.0), 3),
            "vocal_safe": True,
            "raw_features": {
                "bass_energy": 0.0,
                "energy_change": 0.0,
                "rms": 0.0
            }
        })

    return events