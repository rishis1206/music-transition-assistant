def recommend_transitions(events):
    """Single song recommendations — used internally for ranking."""

    recommendations = []

    for event in events:

        transitions = []
        reasons = []

        event_type = event.get("type", "Musical Section")
        transition_time = event.get("time", 0)

        bass = event.get("bass_strength", 0)
        energy = event.get("energy_strength", 0)
        kick = event.get("kick_strength", 0)
        snare = event.get("snare_strength", 0)
        hihat = event.get("hihat_strength", 0)
        chord = event.get("chord_strength", 0)
        melody = event.get("melody_strength", 0)
        synth = event.get("synth_strength", 0)
        reverb = event.get("reverb_strength", 0)
        drop = event.get("drop_strength", 0)
        buildup = event.get("buildup_strength", 0)
        confidence = event.get("confidence", 0)

        if event_type == "Drop":
            transitions.extend([
                {"sfx": "Whoosh", "place_at": round(transition_time - 2.0, 2), "note": "2 seconds before the drop"},
                {"sfx": "Impact", "place_at": round(transition_time, 2), "note": "exactly on the drop"},
                {"sfx": "Bass Carry", "place_at": round(transition_time, 2), "note": "sustain bass through the switch"}
            ])
            reasons.append("Strong drop detected")

        elif event_type == "Build-up":
            transitions.extend([
                {"sfx": "Riser", "place_at": round(transition_time - 4.0, 2), "note": "4 seconds before peak"},
                {"sfx": "Reverse Cymbal", "place_at": round(transition_time - 1.5, 2), "note": "1.5 seconds before transition"},
                {"sfx": "Filter Sweep", "place_at": round(transition_time - 2.0, 2), "note": "sweep into the transition"}
            ])
            reasons.append("Energy is building")

        elif event_type == "Synth Lead":
            transitions.extend([
                {"sfx": "Echo", "place_at": round(transition_time - 0.5, 2), "note": "half second before switch"},
                {"sfx": "Reverb Tail", "place_at": round(transition_time, 2), "note": "let the synth tail bleed into next song"},
                {"sfx": "Low-pass Filter", "place_at": round(transition_time - 1.0, 2), "note": "roll off highs 1 second before"}
            ])
            reasons.append("Synth dominates the section")

        elif event_type == "Chord Progression":
            transitions.extend([
                {"sfx": "Crossfade", "place_at": round(transition_time - 2.0, 2), "note": "start crossfade 2 seconds early"},
                {"sfx": "Reverb Tail", "place_at": round(transition_time, 2), "note": "on the chord change"}
            ])
            reasons.append("Strong harmonic movement")

        elif event_type == "Atmospheric":
            transitions.extend([
                {"sfx": "Long Fade", "place_at": round(transition_time - 4.0, 2), "note": "slow fade starting 4 seconds early"},
                {"sfx": "Delay", "place_at": round(transition_time - 1.0, 2), "note": "delay effect before switch"},
                {"sfx": "Ambient Sweep", "place_at": round(transition_time, 2), "note": "on the transition point"}
            ])
            reasons.append("Ambient texture detected")

        elif event_type == "Melodic Section":
            transitions.extend([
                {"sfx": "Echo", "place_at": round(transition_time - 0.5, 2), "note": "echo the last note before switching"},
                {"sfx": "Smooth Crossfade", "place_at": round(transition_time - 1.5, 2), "note": "blend 1.5 seconds before"}
            ])
            reasons.append("Melody is dominant")

        elif event_type == "Rhythmic Groove":
            transitions.extend([
                {"sfx": "Hard Cut", "place_at": round(transition_time, 2), "note": "cut exactly on the beat"},
                {"sfx": "Beat Cut", "place_at": round(transition_time, 2), "note": "switch on the downbeat"},
                {"sfx": "Stutter", "place_at": round(transition_time - 0.5, 2), "note": "stutter effect half second before"}
            ])
            reasons.append("Strong rhythmic section")

        elif event_type == "Vocal Gap":
            transitions.extend([
                {"sfx": "Whoosh", "place_at": round(transition_time - 1.5, 2), "note": "whoosh during the silence"},
                {"sfx": "Smooth Crossfade", "place_at": round(transition_time - 1.0, 2), "note": "blend while vocals are absent"}
            ])
            reasons.append("Vocal gap — safe transition zone")

        else:
            transitions.append({"sfx": "Hard Cut", "place_at": round(transition_time, 2), "note": "on the transition point"})
            reasons.append("General musical section")

        if bass > 0.75:
            transitions.append({"sfx": "Bass Carry", "place_at": round(transition_time, 2), "note": "strong bass — carry it through"})
        if kick > 0.70:
            transitions.append({"sfx": "Impact", "place_at": round(transition_time, 2), "note": "kick is strong — hit it hard"})
        if snare > 0.70:
            transitions.append({"sfx": "Snare Fill", "place_at": round(transition_time - 0.5, 2), "note": "fill half second before"})
        if hihat > 0.70:
            transitions.append({"sfx": "Beat Cut", "place_at": round(transition_time, 2), "note": "cut on the hi-hat"})
        if synth > 0.75:
            transitions.append({"sfx": "Filter Sweep", "place_at": round(transition_time - 1.0, 2), "note": "sweep 1 second before"})
        if reverb > 0.70:
            transitions.append({"sfx": "Reverb Tail", "place_at": round(transition_time, 2), "note": "let reverb bleed naturally"})
        if drop > 0.75:
            transitions.append({"sfx": "Impact", "place_at": round(transition_time, 2), "note": "drop hit — impact here"})
        if buildup > 0.70:
            transitions.append({"sfx": "Riser", "place_at": round(transition_time - 3.0, 2), "note": "riser 3 seconds before peak"})

        seen = set()
        unique_transitions = []
        for t in transitions:
            if t["sfx"] not in seen:
                seen.add(t["sfx"])
                unique_transitions.append(t)

        reasons = list(dict.fromkeys(reasons))

        recommendations.append({
            "time": transition_time,
            "event": event_type,
            "confidence": round(confidence * 100, 1),
            "transitions": unique_transitions,
            "reasons": reasons
        })

    return recommendations


def recommend_pair_transitions(event1, event2):
    """
    Cross-song aware SFX recommendations.
    Looks at what BOTH songs are doing at the transition
    and generates SFX that bridge them intelligently.
    """

    t = event1.get("time", 0)

    # Song A features (exiting)
    a_bass = event1.get("bass_strength", 0)
    a_808 = event1.get("sub808_strength", 0)
    a_kick = event1.get("kick_strength", 0)
    a_synth = event1.get("synth_strength", 0)
    a_reverb = event1.get("reverb_strength", 0)
    a_vocal_safe = event1.get("vocal_safe", False)
    a_energy = event1.get("energy_strength", 0)
    a_drop = event1.get("drop_strength", 0)
    a_buildup = event1.get("buildup_strength", 0)
    a_type = event1.get("type", "")

    # Song B features (entering)
    b_bass = event2.get("bass_strength", 0)
    b_kick = event2.get("kick_strength", 0)
    b_energy = event2.get("energy_strength", 0)
    b_drop = event2.get("drop_strength", 0)
    b_synth = event2.get("synth_strength", 0)
    b_type = event2.get("type", "")

    transitions = []

    # =====================================
    # CROSS-SONG LOGIC
    # =====================================

    # Song A has 808 bleeding out → carry it into Song B
    if a_808 > 0.5 and b_bass > 0.4:
        transitions.append({
            "sfx": "808 Carry",
            "place_at": round(t, 2),
            "note": "Song A's 808 is strong — let it bleed into Song B's bass"
        })

    # Song A exiting on a drop → hit it with impact
    if a_drop > 0.5 or a_type == "Drop":
        transitions.append({
            "sfx": "Impact",
            "place_at": round(t, 2),
            "note": "Song A drops hard — hit the switch with an impact"
        })
        transitions.append({
            "sfx": "Whoosh",
            "place_at": round(t - 2.0, 2),
            "note": "build tension 2 seconds before Song A's drop"
        })

    # Song B entering on a drop → prep with a riser
    if b_drop > 0.5 or b_type == "Drop":
        transitions.append({
            "sfx": "Riser",
            "place_at": round(t - 3.0, 2),
            "note": "Song B drops hard — riser 3 seconds before entry"
        })
        transitions.append({
            "sfx": "Reverse Cymbal",
            "place_at": round(t - 1.0, 2),
            "note": "reverse cymbal 1 second before Song B kicks in"
        })

    # Song A has reverb heavy mix → let it tail naturally
    if a_reverb > 0.6:
        transitions.append({
            "sfx": "Reverb Tail",
            "place_at": round(t, 2),
            "note": "Song A is reverb heavy — let it tail into Song B naturally"
        })

    # Both songs have strong synth → filter sweep to blend
    if a_synth > 0.5 and b_synth > 0.5:
        transitions.append({
            "sfx": "Filter Sweep",
            "place_at": round(t - 1.5, 2),
            "note": "both songs are synth heavy — sweep the filter to blend"
        })

    # Song A vocal safe → clean whoosh transition
    if a_vocal_safe:
        transitions.append({
            "sfx": "Whoosh",
            "place_at": round(t - 1.0, 2),
            "note": "vocals are absent — clean whoosh transition here"
        })

    # Energy drop from A to B → smooth it out
    if a_energy > 0.7 and b_energy < 0.4:
        transitions.append({
            "sfx": "Low-pass Filter",
            "place_at": round(t - 1.0, 2),
            "note": "Song B is lower energy — roll off highs to ease into it"
        })
        transitions.append({
            "sfx": "Smooth Crossfade",
            "place_at": round(t - 2.0, 2),
            "note": "energy drops — start blending 2 seconds early"
        })

    # Energy jump from A to B → make it hit
    if b_energy > 0.7 and a_energy < 0.5:
        transitions.append({
            "sfx": "Impact",
            "place_at": round(t, 2),
            "note": "Song B hits harder — impact on entry"
        })
        transitions.append({
            "sfx": "Whoosh",
            "place_at": round(t - 1.5, 2),
            "note": "build into Song B's energy spike"
        })

    # Song A buildup → Song B drop = perfect combo
    if a_buildup > 0.5 and (b_drop > 0.5 or b_type == "Drop"):
        transitions.append({
            "sfx": "Riser",
            "place_at": round(t - 4.0, 2),
            "note": "Song A builds, Song B drops — riser 4 seconds early"
        })
        transitions.append({
            "sfx": "Impact",
            "place_at": round(t, 2),
            "note": "Song B drop lands — hit it hard"
        })

    # Both kicks strong → beat cut
    if a_kick > 0.6 and b_kick > 0.6:
        transitions.append({
            "sfx": "Beat Cut",
            "place_at": round(t, 2),
            "note": "both songs have strong kicks — hard beat cut here"
        })

    # Fallback if nothing triggered
    if not transitions:
        transitions.append({
            "sfx": "Crossfade",
            "place_at": round(t - 2.0, 2),
            "note": "general transition — crossfade 2 seconds early"
        })

    # Remove duplicates
    seen = set()
    unique = []
    for tr in transitions:
        if tr["sfx"] not in seen:
            seen.add(tr["sfx"])
            unique.append(tr)

    return unique