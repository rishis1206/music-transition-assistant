from src.audio_loader import load_audio
from src.beat_detector import detect_beats
from src.energy_analyzer import analyze_energy
from src.bass_analyzer import analyze_bass
from src.event_classifier import classify_events
from src.visualizer import plot_energy
from src.transition_recommender import recommend_transitions
from src.confidence_engine import calculate_confidence
from src.ranking_engine import rank_events
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
from src.vocal_analyzer import analyze_vocals
from src.lyric_gap_detector import find_vocal_gaps

# =====================================
# LOAD AUDIO
# =====================================

file_path = "songs/metro-boomin-travis-scott-young-thug-trance-visualizer-128-ytshorts.savetube.me.mp3"

audio_data = load_audio(file_path)
audio = audio_data["audio"]
sample_rate = audio_data["sample_rate"]
duration = audio_data["duration"]

# =====================================
# BEAT DETECTION
# =====================================

beat_data = detect_beats(audio, sample_rate)

# =====================================
# ENERGY ANALYSIS
# =====================================

energy_data = analyze_energy(audio, sample_rate)

# =====================================
# BASS ANALYSIS
# =====================================

bass_data = analyze_bass(audio, sample_rate)

# =====================================
# COMPONENT DETECTION
# =====================================

detector808 = detect_808(audio, sample_rate)
kick = detect_kick(audio, sample_rate)
snare = detect_snare(audio, sample_rate)
hihat = detect_hihat(audio, sample_rate)
chord = detect_chords(audio, sample_rate)
melody = detect_melody(audio, sample_rate)
synth = detect_synth(audio, sample_rate)
reverb = detect_reverb(audio, sample_rate)
drop_data = detect_drops(audio, sample_rate)
buildup_data = detect_buildups(audio, sample_rate)

# =====================================
# WHISPER VOCAL ANALYSIS
# =====================================

print("\n========== VOCAL ANALYSIS ==========")
print("Running Whisper... (this may take a moment)")

vocal_segments = analyze_vocals(file_path)
vocal_gaps = find_vocal_gaps(vocal_segments, min_gap=1.0)

print(f"Vocal Segments : {len(vocal_segments)}")
print(f"Vocal Gaps     : {len(vocal_gaps)}")

if vocal_gaps:
    print("Safe Transition Zones:")
    for gap in vocal_gaps:
        print(f"  {gap['start']:.2f}s → {gap['end']:.2f}s  (duration: {gap['duration']:.2f}s)")

# =====================================
# DETECTOR SUMMARY
# =====================================

print("\n========== DETECTOR SUMMARY ==========")
print("808 Strength      :", detector808["strength"])
print("Kick Strength     :", kick["strength"])
print("Snare Strength    :", snare["strength"])
print("HiHat Strength    :", hihat["strength"])
print("Chord Strength    :", chord["strength"])
print("Melody Strength   :", melody["strength"])
print("Synth Strength    :", synth["strength"])
print("Reverb Strength   :", reverb["strength"])
print("Drop Strength     :", drop_data["strength"])
print("BuildUp Strength  :", buildup_data["strength"])
print()
print("808 Peaks      :", len(detector808["timestamps"]))
print("Kick Peaks     :", len(kick["timestamps"]))
print("Snare Peaks    :", len(snare["timestamps"]))
print("HiHat Peaks    :", len(hihat["timestamps"]))
print("Chord Peaks    :", len(chord["timestamps"]))
print("Melody Peaks   :", len(melody["timestamps"]))
print("Synth Peaks    :", len(synth["timestamps"]))
print("Reverb Peaks   :", len(reverb["timestamps"]))
print("Drop Peaks     :", len(drop_data["timestamps"]))
print("BuildUp Peaks  :", len(buildup_data["timestamps"]))
print("Largest Changes:", len(energy_data["largest_changes"]))

# =====================================
# EVENT CLASSIFICATION
# =====================================

events = classify_events(
    energy_data["largest_changes"],
    energy_data["times"],
    bass_data["bass_peaks"],
    bass_data["bass_times"],
    bass_data["bass_energy"],
    energy_data["energy_change"],
    energy_data["rms"],
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
    vocal_gaps=vocal_gaps
)

ranked_events = rank_events(events)
recommendations = recommend_transitions(events)
confidence_scores = calculate_confidence(events)

# =====================================
# OUTPUT
# =====================================

print("\n==========================")
print("SONG ANALYSIS")
print("==========================")
print(f"Duration: {duration:.2f} sec")
print(f"BPM: {beat_data['bpm']}")
print(f"Total Beats: {len(beat_data['beat_times'])}")

print("\n================================")
print("BEST TRANSITION CANDIDATE")
print("================================")

best = ranked_events[0]

print(f"Time          : {best['time']} sec")
print(f"Type          : {best['type']}")
print(f"Score         : {best['score']:.2f}")
print(f"Bass Strength : {best['bass_strength']:.2f}")
print(f"Energy        : {best['energy_strength']:.2f}")
print(f"RMS           : {best['rms_strength']:.2f}")
print(f"Confidence    : {best['confidence']:.2f}")
print(f"Vocal Safe    : {'✅ YES' if best.get('vocal_safe') else '⚠️  NO - vocals detected here'}")
print(f"Vocal Gap Score: {best.get('vocal_gap_score', 0):.3f}")

print("\n================================")
print("ALTERNATIVES")
print("================================")

for alt in ranked_events[1:4]:
    print(f"\n{alt['time']} sec")
    print(f"Type          : {alt['type']}")
    print(f"Score         : {alt['score']:.2f}")
    print(f"Bass Strength : {alt['bass_strength']:.2f}")
    print(f"Energy        : {alt['energy_strength']:.2f}")
    print(f"Confidence    : {alt['confidence']:.2f}")
    print(f"Vocal Safe    : {'✅ YES' if alt.get('vocal_safe') else '⚠️  NO'}")

print("\nTransition Recommendations:")

for rec in recommendations[:10]:
    print(f"\n{rec['time']} sec")
    print(f"Event: {rec['event']}")
    print("Suggested:")
    for t in rec["transitions"]:
        print(f"  - {t}")

print("\n================================")
print("CONFIDENCE SCORES")
print("================================")

for score in confidence_scores[:10]:
    print(f"{score['time']:.2f} sec")
    print(f"Type       : {score['type']}")
    print(f"Confidence : {score['confidence']:.1f}%")
    print("-" * 35)

# =====================================
# GRAPH
# =====================================

plot_energy(
    energy_data["times"],
    energy_data["rms"]
)