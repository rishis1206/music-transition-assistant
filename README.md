# TransitionAI — AI Music Transition Assistant

An AI-powered web application that analyzes two audio tracks and recommends the optimal transition point between them — complete with SFX placement timing, harmonic compatibility scoring, vocal gap detection, and plain-English explanations.

Built as a portfolio project targeting audio AI roles at companies like Dolby, Samsung R&D, and Qualcomm.

---

## What It Does

Upload two songs. TransitionAI runs a full audio analysis pipeline on both tracks and tells you:

- **Where** to transition (exact timestamp in both songs)
- **Why** that point was chosen (musical reasoning)
- **What SFX** to add and exactly when to place them
- **How compatible** the two songs are (BPM, harmonic key, spectral similarity)
- **Whether vocals are active** at the transition point (Whisper-based vocal gap detection)

---

## Features

- 12+ audio component detectors — bass, 808s, kicks, snares, hi-hats, chords, melody, synth, reverb, drops, build-ups
- Whisper-powered vocal detection and gap analysis
- BPM compatibility scoring with half/double-time awareness
- Harmonic key matching using chroma features and the Camelot wheel
- Cross-song SFX recommendations with millisecond-level placement timing
- Explanation engine — reasons, strengths, and warnings for every recommendation
- Compatibility rating — Excellent / Good / Fair / Low Compatibility
- 5 transition modes:
  - Auto → Auto (AI finds both points)
  - Manual → Auto (you fix Song A, AI finds Song B)
  - Auto → Manual (AI finds Song A, you fix Song B)
  - Manual → Manual (you pick both, AI evaluates)
  - Range → Range (set search windows, AI finds best point within them)
- Dark, immersive web UI with animated waveform and loading states

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Audio Analysis | librosa, scipy |
| Vocal Detection | OpenAI Whisper |
| Feature Extraction | librosa (STFT, chroma, MFCCs, spectral features) |
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Typography | Space Grotesk, JetBrains Mono, Inter |

---

## Project Structure

```
music-transition-assistant/
├── app.py                     # Flask application + all 5 transition modes
├── main.py                    # CLI pipeline for single song testing
├── src/
│   ├── audio_loader.py        # librosa audio loading
│   ├── beat_detector.py       # BPM and beat tracking
│   ├── energy_analyzer.py     # RMS energy curve + section detection
│   ├── bass_analyzer.py       # Bass frequency analysis
│   ├── feature_extractor.py   # Full spectral feature extraction
│   ├── detector_808.py        # Sub-bass 808 detection
│   ├── kick_detector.py       # Kick drum detection
│   ├── snare_detector.py      # Snare detection
│   ├── hihat_detector.py      # Hi-hat detection
│   ├── chord_detector.py      # Chord detection via chroma variance
│   ├── melody_detector.py     # Melodic activity detection
│   ├── synth_detector.py      # Synth/pad detection
│   ├── reverb_detector.py     # Reverb estimation
│   ├── drop_detector.py       # Drop detection
│   ├── buildup_detector.py    # Build-up detection
│   ├── vocal_analyzer.py      # Whisper vocal segment detection
│   ├── lyric_gap_detector.py  # Vocal gap identification
│   ├── event_classifier.py    # Multi-feature event classification
│   ├── ranking_engine.py      # Musical quality × vocal safety scoring
│   ├── dual_song_matcher.py   # Cross-song transition pair matching
│   ├── transition_scorer.py   # Weighted transition scoring
│   ├── transition_recommender.py  # SFX recommendations with timing
│   ├── explanation_engine.py  # Plain-English transition reasoning
│   ├── manual_analyzer.py     # Manual/range mode utilities
│   ├── bpm_compatibility.py   # BPM matching with half/double time
│   ├── harmonic_compatibility.py  # Key compatibility via Camelot wheel
│   ├── similarity_engine.py   # Spectral similarity scoring
│   ├── music_context_engine.py    # Musical context tagging
│   ├── confidence_engine.py   # Confidence scoring
│   └── frequency_analyzer.py  # Frequency band analysis
├── templates/
│   ├── index.html             # Upload UI with mode selector
│   └── results.html           # Results page with full analysis
├── songs/                     # Uploaded audio files (gitignored)
├── requirements.txt
└── .gitignore
```

---

## Installation

**Prerequisites:** Python 3.9+, pip

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/music-transition-assistant.git
cd music-transition-assistant

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create songs directory
mkdir songs

# Run the app
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## How It Works

### Analysis Pipeline

```
Audio File
    ↓
Feature Extraction (STFT, chroma, MFCCs, spectral features)
    ↓
Beat Detection (BPM, beat grid)
    ↓
Component Detection (808, kick, snare, hihat, chord, melody, synth, reverb, drop, buildup)
    ↓
Whisper Vocal Analysis (segment timestamps, gap detection)
    ↓
Event Classification (multi-feature scoring → event type)
    ↓
Ranking Engine (musical quality × vocal safety multiplier)
    ↓
Dual Song Matching (BPM + harmonic + vocal + energy compatibility)
    ↓
Transition Scoring (weighted combination of all factors)
    ↓
SFX Recommendations (cross-song context aware, millisecond timing)
    ↓
Explanation Engine (reasons, strengths, warnings, verdict)
```

### Scoring Formula

```
Musical Score = bass(25%) + energy(20%) + confidence(15%) + vocal_gap(15%) + BPM(12%) + harmonic(8%) + similarity(5%)

Final Score = Musical Score × Vocal Safety Multiplier (1.0–1.3)

Compatibility = BPM(40%) + Harmonic(35%) + Similarity(25%)
```

### Chord Detection

Uses chroma variance rather than raw chroma max — real chords spread energy across multiple pitch classes (low variance), while melody or percussion concentrates in fewer bins (high variance). This prevents the common false-positive problem where every frame gets classified as a chord.

### Vocal Gap Detection

Whisper transcribes the audio and returns segment timestamps. Gaps between segments longer than 1 second are marked as safe transition zones. Events within these zones receive a vocal safety multiplier boost in scoring, but cannot override musically weak candidates.

---

## Transition Modes

| Mode | Song A | Song B | Use Case |
|---|---|---|---|
| Auto → Auto | AI searches full song | AI searches full song | Quick analysis |
| Manual → Auto | You set exit point | AI finds best entry | You know your Song A cut |
| Auto → Manual | AI finds best exit | You set entry point | You know your Song B start |
| Manual → Manual | You set both | AI evaluates quality | Verify a specific transition |
| Range → Range | You set search window | You set search window | Work within specific sections |

---

## Known Limitations

- Whisper runs on CPU — analysis takes 30–60 seconds per song pair
- Synth and reverb detectors have high sensitivity on atmospheric/ambient music (by design — Metro Boomin production correctly scores high on reverb)
- Model training not yet implemented — all detectors are DSP rule-based
- No audio playback in the UI (planned for v2)

---

## Roadmap

- [ ] Replace rule-based detectors with pretrained ML models (Demucs for source separation, Essentia for component classification)
- [ ] Audio preview at transition point in the browser
- [ ] Waveform timeline with drag-and-drop transition markers
- [ ] Genre detection (trap, EDM, lo-fi, phonk, house etc)
- [ ] Export transition report as PDF
- [ ] Async processing so UI doesn't block during analysis
- [ ] Mobile responsive layout

---

## Background

Built by a final-year AI & ML student (VTU) with a background in video and music editing. The project came from a real frustration — existing DJ tools give you BPM matching but nothing tells you *why* a transition works or exactly where to place the SFX that makes it feel natural.

---

## License

MIT