from flask import Flask, render_template, request
from src.audio_loader import load_audio
from src.beat_detector import detect_beats
from src.energy_analyzer import analyze_energy
from src.bass_analyzer import analyze_bass
from src.event_classifier import classify_events
from src.ranking_engine import rank_events
from src.dual_song_matcher import find_best_match
from src.feature_extractor import extract_features
from src.similarity_engine import calculate_similarity
from src.detector_808 import detect_808
from src.kick_detector import detect_kick
from src.snare_detector import detect_snare
from src.hihat_detector import detect_hihat
from src.chord_detector import detect_chords
from src.melody_detector import detect_melody
from src.synth_detector import detect_synth
from src.reverb_detector import detect_reverb
from src.drop_detector import detect_drops
from src.buildup_detector import detect_buildups
from src.transition_recommender import recommend_transitions, recommend_pair_transitions
from src.vocal_analyzer import analyze_vocals
from src.lyric_gap_detector import find_vocal_gaps
from src.explanation_engine import build_explanation
from src.manual_analyzer import parse_timestamp, get_event_at_time, evaluate_manual_transition
from src.bpm_compatibility import calculate_bpm_score
from src.harmonic_compatibility import calculate_harmonic_score
from src.stem_separator import separate_stems
import werkzeug.utils

app = Flask(__name__)


def seconds_to_mmss(seconds):
    seconds = float(seconds)
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:05.2f}"


def analyze_song(file_path):
    """
    Run full analysis pipeline on a single song.
    Uses Demucs stems when available for higher accuracy.
    Falls back to full mix if separation fails.
    """

    # Load full mix for features that need the complete audio
    audio_data = load_audio(file_path)
    audio = audio_data["audio"]
    sr = audio_data["sample_rate"]

    features = extract_features(audio, sr)
    beat_data = detect_beats(audio, sr)
    energy_data = analyze_energy(audio, sr)

    # Try to get stems via Demucs
    stems = separate_stems(file_path)

    if stems:
        # Load each stem separately
        bass_audio_data = load_audio(stems["bass"])
        drums_audio_data = load_audio(stems["drums"])
        other_audio_data = load_audio(stems["other"])
        vocals_audio_data = load_audio(stems["vocals"])

        bass_audio = bass_audio_data["audio"]
        drums_audio = drums_audio_data["audio"]
        other_audio = other_audio_data["audio"]
        vocals_audio = vocals_audio_data["audio"]
        stem_sr = bass_audio_data["sample_rate"]

        # Use stem-specific analysis — much more accurate
        bass_data   = analyze_bass(bass_audio, stem_sr)
        detector808 = detect_808(bass_audio, stem_sr)
        kick        = detect_kick(drums_audio, stem_sr)
        snare       = detect_snare(drums_audio, stem_sr)
        hihat       = detect_hihat(drums_audio, stem_sr)
        chord       = detect_chords(other_audio, stem_sr)
        melody      = detect_melody(other_audio, stem_sr)
        synth       = detect_synth(other_audio, stem_sr)
        reverb      = detect_reverb(other_audio, stem_sr)
        drop_data   = detect_drops(drums_audio, stem_sr)
        buildup_data = detect_buildups(other_audio, stem_sr)

        # Whisper on clean vocal stem — no background noise confusion
        vocal_segments = analyze_vocals(stems["vocals"])

        print("[Pipeline] Using stem-based analysis")

    else:
        # Fallback — full mix analysis
        bass_data    = analyze_bass(audio, sr)
        detector808  = detect_808(audio, sr)
        kick         = detect_kick(audio, sr)
        snare        = detect_snare(audio, sr)
        hihat        = detect_hihat(audio, sr)
        chord        = detect_chords(audio, sr)
        melody       = detect_melody(audio, sr)
        synth        = detect_synth(audio, sr)
        reverb       = detect_reverb(audio, sr)
        drop_data    = detect_drops(audio, sr)
        buildup_data = detect_buildups(audio, sr)
        vocal_segments = analyze_vocals(file_path)

        print("[Pipeline] Using full mix analysis (stems unavailable)")

    vocal_gaps = find_vocal_gaps(vocal_segments, min_gap=1.0)

    events = classify_events(
        energy_data["largest_changes"],
        energy_data["times"],
        bass_data["bass_peaks"],
        bass_data["bass_times"],
        bass_data["bass_energy"],
        energy_data["energy_change"],
        energy_data["rms"],
        detector808, kick, snare, hihat, chord,
        melody, synth, reverb, drop_data, buildup_data,
        vocal_gaps=vocal_gaps
    )

    ranked = rank_events(events)
    recommendations = recommend_transitions(events)

    return {
        "features": features,
        "ranked_events": ranked,
        "recommendations": recommendations,
        "duration": audio_data["duration"],
        "vocal_gaps": vocal_gaps,
        "bpm": beat_data["bpm"],
        "chroma": features["chroma"],
        "used_stems": stems is not None
    }


def filter_events_by_range(events, start_time, end_time):
    filtered = [e for e in events if start_time <= e["time"] <= end_time]
    if not filtered:
        mid = (start_time + end_time) / 2
        closest = min(events, key=lambda e: abs(e["time"] - mid))
        filtered = [closest]
    return filtered


def get_compat_label(compat_score):
    if compat_score >= 80:
        return "Excellent", "#44FF88"
    elif compat_score >= 60:
        return "Good", "#FF8C00"
    elif compat_score >= 40:
        return "Fair", "#FFAA44"
    else:
        return "Low Compatibility", "#FF4444"


def build_result(best, matches, result1, result2, similarity_score, mode="auto-auto"):
    song1_event = next(
        (e for e in result1["ranked_events"] if e["time"] == best["song1_time"]), None
    )
    song2_event = next(
        (e for e in result2["ranked_events"] if e["time"] == best["song2_time"]), None
    )

    transitions = []
    if song1_event and song2_event:
        transitions = recommend_pair_transitions(song1_event, song2_event)

    compat_score = (
        best.get("bpm_score", 0) * 0.40 +
        best.get("harmonic_score", 0) * 0.35 +
        similarity_score * 0.25
    ) * 100

    compat_label, compat_color = get_compat_label(compat_score)

    explanation = build_explanation(
        event1=song1_event or {},
        event2=song2_event or {},
        bpm1=result1["bpm"],
        bpm2=result2["bpm"],
        bpm_score=best.get("bpm_score", 0),
        harmonic_score=best.get("harmonic_score", 0),
        similarity_score=similarity_score,
        compat_score=compat_score
    )

    return dict(
        song1_time=best["song1_time"],
        song2_time=best["song2_time"],
        song1_time_mmss=seconds_to_mmss(best["song1_time"]),
        song2_time_mmss=seconds_to_mmss(best["song2_time"]),
        event_type=best.get("event_type", best.get("type", "—")),
        score=best["score"],
        similarity_score=similarity_score,
        song1_bass=best.get("song1_bass", 0),
        song2_bass=best.get("song2_bass", 0),
        song1_energy=best.get("song1_energy", 0),
        song2_energy=best.get("song2_energy", 0),
        song1_confidence=best.get("song1_confidence", 0),
        song2_confidence=best.get("song2_confidence", 0),
        transitions=transitions,
        alternatives=[
            {**a,
             "song1_time_mmss": seconds_to_mmss(a["song1_time"]),
             "song2_time_mmss": seconds_to_mmss(a["song2_time"])}
            for a in (matches[1:4] if matches else [])
        ],
        song1_duration=result1["duration"],
        song2_duration=result2["duration"],
        song1_vocal_gaps=result1["vocal_gaps"],
        song2_vocal_gaps=result2["vocal_gaps"],
        bpm1=result1["bpm"],
        bpm2=result2["bpm"],
        bpm_score=best.get("bpm_score", 0),
        harmonic_score=best.get("harmonic_score", 0),
        compat_score=round(compat_score, 1),
        compat_label=compat_label,
        compat_color=compat_color,
        explanation=explanation,
        mode=mode,
        manual_quality=None,
        manual_quality_color=None,
        song1_used_stems=result1.get("used_stems", False),
        song2_used_stems=result2.get("used_stems", False)
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    song1 = request.files["song1"]
    song2 = request.files["song2"]
    mode = request.form.get("mode", "auto-auto")

    song1_filename = werkzeug.utils.secure_filename(song1.filename)
    song2_filename = werkzeug.utils.secure_filename(song2.filename)

    song1_path = f"songs/{song1_filename}"
    song2_path = f"songs/{song2_filename}"

    song1.save(song1_path)
    song2.save(song2_path)

    result1 = analyze_song(song1_path)
    result2 = analyze_song(song2_path)

    similarity_score = calculate_similarity(result1["features"], result2["features"])

    bpm_kw = dict(
        bpm1=result1["bpm"],
        bpm2=result2["bpm"],
        chroma1=result1["chroma"],
        chroma2=result2["chroma"]
    )

    if mode == "auto-auto":
        matches = find_best_match(result1["ranked_events"], result2["ranked_events"], **bpm_kw)
        if not matches:
            return "No matching transition found."
        matches.sort(key=lambda x: x["score"], reverse=True)
        return render_template("results.html",
            **build_result(matches[0], matches, result1, result2, similarity_score, mode))

    elif mode == "manual-auto":
        ts1 = parse_timestamp(request.form.get("timestamp1", "0"))
        event1 = get_event_at_time(result1["ranked_events"], ts1)
        matches = find_best_match([event1], result2["ranked_events"], **bpm_kw)
        if not matches:
            return "No matching transition found."
        matches.sort(key=lambda x: x["score"], reverse=True)
        best = matches[0]
        best["song1_time"] = ts1
        return render_template("results.html",
            **build_result(best, matches, result1, result2, similarity_score, mode))

    elif mode == "auto-manual":
        ts2 = parse_timestamp(request.form.get("timestamp2", "0"))
        event2 = get_event_at_time(result2["ranked_events"], ts2)
        matches = find_best_match(result1["ranked_events"], [event2], **bpm_kw)
        if not matches:
            return "No matching transition found."
        matches.sort(key=lambda x: x["score"], reverse=True)
        best = matches[0]
        best["song2_time"] = ts2
        return render_template("results.html",
            **build_result(best, matches, result1, result2, similarity_score, mode))

    elif mode == "manual-manual":
        ts1 = parse_timestamp(request.form.get("timestamp1", "0"))
        ts2 = parse_timestamp(request.form.get("timestamp2", "0"))

        event1 = get_event_at_time(result1["ranked_events"], ts1)
        event2 = get_event_at_time(result2["ranked_events"], ts2)

        bpm_score = calculate_bpm_score(result1["bpm"], result2["bpm"])
        harmonic_score = calculate_harmonic_score(result1["chroma"], result2["chroma"])
        evaluation = evaluate_manual_transition(event1, event2, bpm_score, harmonic_score, similarity_score)
        transitions = recommend_pair_transitions(event1, event2)
        compat_score = (bpm_score * 0.40 + harmonic_score * 0.35 + similarity_score * 0.25) * 100
        compat_label, compat_color = get_compat_label(compat_score)
        explanation = build_explanation(
            event1=event1, event2=event2,
            bpm1=result1["bpm"], bpm2=result2["bpm"],
            bpm_score=bpm_score, harmonic_score=harmonic_score,
            similarity_score=similarity_score, compat_score=compat_score
        )

        return render_template("results.html",
            song1_time=ts1, song2_time=ts2,
            song1_time_mmss=seconds_to_mmss(ts1),
            song2_time_mmss=seconds_to_mmss(ts2),
            event_type=f"{event1['type']} → {event2['type']}",
            score=evaluation["score"],
            manual_quality=evaluation["quality"],
            manual_quality_color=evaluation["quality_color"],
            similarity_score=similarity_score,
            song1_bass=event1.get("bass_strength", 0),
            song2_bass=event2.get("bass_strength", 0),
            song1_energy=event1.get("energy_strength", 0),
            song2_energy=event2.get("energy_strength", 0),
            song1_confidence=event1.get("confidence", 0),
            song2_confidence=event2.get("confidence", 0),
            transitions=transitions, alternatives=[],
            song1_duration=result1["duration"],
            song2_duration=result2["duration"],
            song1_vocal_gaps=result1["vocal_gaps"],
            song2_vocal_gaps=result2["vocal_gaps"],
            bpm1=result1["bpm"], bpm2=result2["bpm"],
            bpm_score=bpm_score, harmonic_score=harmonic_score,
            compat_score=round(compat_score, 1),
            compat_label=compat_label, compat_color=compat_color,
            explanation=explanation, mode=mode,
            song1_used_stems=result1.get("used_stems", False),
            song2_used_stems=result2.get("used_stems", False)
        )

    elif mode == "range-range":
        start1 = parse_timestamp(request.form.get("range1_start", "0"))
        end1   = parse_timestamp(request.form.get("range1_end", "60"))
        start2 = parse_timestamp(request.form.get("range2_start", "0"))
        end2   = parse_timestamp(request.form.get("range2_end", "60"))

        events1_filtered = filter_events_by_range(result1["ranked_events"], start1, end1)
        events2_filtered = filter_events_by_range(result2["ranked_events"], start2, end2)

        matches = find_best_match(events1_filtered, events2_filtered, **bpm_kw)
        if not matches:
            return "No matching transition found within the specified ranges."
        matches.sort(key=lambda x: x["score"], reverse=True)
        return render_template("results.html",
            **build_result(matches[0], matches, result1, result2, similarity_score, mode))

    return "Invalid mode selected."


if __name__ == "__main__":
    app.run(debug=True)