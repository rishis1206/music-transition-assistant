def build_explanation(
    event1,
    event2,
    bpm1,
    bpm2,
    bpm_score,
    harmonic_score,
    similarity_score,
    compat_score
):
    """
    Builds a plain English explanation of why this
    transition was selected and what makes it work.
    """

    reasons = []
    strengths = []
    warnings = []

    a_type = event1.get("type", "Musical Section")
    b_type = event2.get("type", "Musical Section")
    a_vocal_safe = event1.get("vocal_safe", False)
    a_energy = event1.get("energy_strength", 0)
    b_energy = event2.get("energy_strength", 0)
    a_bass = event1.get("bass_strength", 0)
    b_bass = event2.get("bass_strength", 0)
    a_drop = event1.get("drop_strength", 0)
    b_drop = event2.get("drop_strength", 0)
    a_buildup = event1.get("buildup_strength", 0)
    a_confidence = event1.get("confidence", 0)
    b_confidence = event2.get("confidence", 0)

    bpm_diff = abs(bpm1 - bpm2)

    # =====================================
    # WHY THIS POINT WAS CHOSEN
    # =====================================

    if a_type == "Vocal Gap":
        reasons.append("Song A has a natural silence between vocal phrases — the cleanest possible moment to switch.")
    elif a_type == "Drop":
        reasons.append(f"Song A hits a strong drop at this point — high energy exit that sets up Song B's entry.")
    elif a_type == "Build-up":
        reasons.append("Song A is building energy here — a great moment to hand off to Song B before the peak.")
    elif a_type == "Synth Lead":
        reasons.append("Song A has a dominant synth layer — the sustained tone makes a smooth bridge into Song B.")
    elif a_type == "Rhythmic Groove":
        reasons.append("Song A has a strong rhythmic groove — the beat alignment makes a natural cut point.")
    else:
        reasons.append(f"Song A reaches a significant {a_type} moment — a clear structural point in the track.")

    if b_type == "Drop":
        reasons.append("Song B enters at a drop — maximum impact on the switch.")
    elif b_type == "Build-up":
        reasons.append("Song B starts building here — energy will rise naturally after the transition.")
    elif b_type == "Vocal Gap":
        reasons.append("Song B also has vocal space at this point — no clash between lyrics on entry.")
    elif b_type == "Synth Lead":
        reasons.append("Song B opens with synth — the texture continues without a jarring break.")

    # =====================================
    # STRENGTHS
    # =====================================

    if bpm_score >= 0.85:
        strengths.append(f"BPM match is tight ({bpm1:.0f} vs {bpm2:.0f}) — the groove stays locked.")
    elif bpm_score >= 0.65:
        strengths.append(f"BPM difference is manageable ({bpm_diff:.0f} BPM gap) — slight pitch shift or beatmatch recommended.")

    if harmonic_score >= 0.8:
        strengths.append("Keys are harmonically compatible — no clashing notes on the transition.")
    elif harmonic_score >= 0.6:
        strengths.append("Keys are close enough — transition will feel musical rather than jarring.")

    if a_vocal_safe:
        strengths.append("Transition lands in a vocal gap — no lyrics get cut off mid-word.")

    if a_energy > 0.7 and b_energy > 0.6:
        strengths.append("Both songs have high energy at this point — the listener won't feel a drop in intensity.")

    if a_bass > 0.6 and b_bass > 0.5:
        strengths.append("Both tracks carry strong bass — 808 and low end continue naturally through the switch.")

    if a_buildup > 0.5 and b_drop > 0.5:
        strengths.append("Song A builds into Song B's drop — textbook DJ transition structure.")

    if a_confidence > 0.5 and b_confidence > 0.5:
        strengths.append("Both transition points scored high confidence — strong musical moments on both sides.")

    # =====================================
    # WARNINGS
    # =====================================

    if bpm_diff > 20:
        warnings.append(f"BPM gap is large ({bpm1:.0f} vs {bpm2:.0f}) — beatmatching or pitch correction strongly recommended.")
    elif bpm_diff > 10:
        warnings.append(f"BPM difference of {bpm_diff:.0f} — a quick mix or tempo automation will smooth this out.")

    if harmonic_score < 0.4:
        warnings.append("Key compatibility is low — consider adding a harmonic bridge or filter effect.")

    if not a_vocal_safe:
        warnings.append("Vocals may be active in Song A at this point — risk of cutting lyrics mid-phrase.")

    if similarity_score < 0.2:
        warnings.append("Songs have very different spectral profiles — genre mismatch may be audible.")

    if a_energy > 0.8 and b_energy < 0.3:
        warnings.append("Energy drops significantly into Song B — add a fade or filter sweep to ease the change.")

    if b_energy > 0.8 and a_energy < 0.3:
        warnings.append("Song B hits much harder than Song A's exit — add a riser or impact SFX to prepare the listener.")

    # =====================================
    # OVERALL VERDICT
    # =====================================

    if compat_score >= 80:
        verdict = "This is a strong transition. The songs are musically compatible and the timing is well chosen."
    elif compat_score >= 60:
        verdict = "This transition will work well with minor adjustments. Focus on the warnings above for a cleaner mix."
    elif compat_score >= 40:
        verdict = "This transition is possible but will take editing skill to make it feel natural. Consider the SFX guide."
    else:
        verdict = "These songs are difficult to mix together. This is the best available point but expect noticeable differences."

    return {
        "reasons": reasons,
        "strengths": strengths,
        "warnings": warnings,
        "verdict": verdict
    }