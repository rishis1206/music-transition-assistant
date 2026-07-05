🎵 TransitionAI — AI Music Transition Assistant

An AI-powered web application that analyzes two audio tracks and recommends the optimal transition point between them — complete with SFX placement timing, harmonic compatibility scoring, vocal gap detection, and plain-English explanations.

> Built with Python, Flask, Demucs, Whisper, and librosa

---

## 🎬 Live Demo

https://youtu.be/nK41BGnsxJA 

---

## ✨ What It Does

Upload two songs. TransitionAI runs a full audio analysis pipeline on both tracks and tells you:

- **Where** to transition — exact timestamp in both songs (MM:SS format)
- **Why** that point was chosen — plain English musical reasoning
- **What SFX** to add and exactly when to place them (whoosh 2s before, impact on the beat etc)
- **How compatible** the two songs are — BPM, harmonic key, spectral similarity
- **Whether vocals are active** at the transition point — Whisper-based vocal gap detection

---

## 🔥 Features

- **Demucs stem separation** — splits each song into bass, drums, vocals, other stems before analysis. Each detector only sees its relevant audio source for dramatically higher accuracy
- **12+ audio component detectors** — bass, 808s, kicks, snares, hi-hats, chords, melody, synth, reverb, drops, build-ups
- **Smart stem caching** — Demucs only runs once per song. Repeat uploads are instant
- **Whisper vocal detection** — runs on clean vocal stem, no background noise interference
- **BPM compatibility scoring** — with half/double-time awareness (140 BPM mixes cleanly with 70 BPM)
- **Harmonic key matching** — chroma-based key detection + Camelot wheel compatibility
- **Cross-song SFX recommendations** — looks at BOTH songs' features together, not each in isolation
- **Millisecond-level SFX timing** — "add whoosh at 1:18, impact at 1:20, bass carry from 1:20"
- **Compatibility rating** — Excellent / Good / Fair / Low Compatibility with color coding
- **Explanation engine** — reasons selected, strengths, and honest warnings for every recommendation
- **5 transition modes:**
  - Auto → Auto (AI finds both points)
  - Manual → Auto (you fix Song A, AI finds Song B)
  - Auto → Manual (AI finds Song A, you fix Song B)
  - Manual → Manual (you pick both, AI evaluates quality)
  - Range → Range (set search windows, AI finds best point within them)
- Dark immersive UI with animated waveform and loading states

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Stem Separation | Meta Demucs (htdemucs pretrained model) |
| Vocal Detection | OpenAI Whisper (base model) |
| Audio Analysis | librosa, scipy |
| Feature Extraction | STFT, chroma, MFCCs, spectral features |
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Typography | Space Grotesk, JetBrains Mono, Inter |

---

## 📁 Project Structure

```
music-transition-assistant/
├── app.py                         # Flask app + all 5 transition modes
├── main.py                        # CLI pipeline for single song testing
├── src/
│   ├── audio_loader.py            # librosa audio loading
│   ├── beat_detector.py           # BPM and beat tracking
│   ├── energy_analyzer.py         # RMS energy curve + section detection
│   ├── bass_analyzer.py           # Bass frequency analysis
│   ├── feature_extractor.py       # Full spectral feature extraction
│   ├── stem_separator.py          # Demucs stem separation with caching
│   ├── detector_808.py            # Sub-bass 808 detection (bass stem)
│   ├── kick_detector.py           # Kick drum detection (drums stem)
│   ├── snare_detector.py          # Snare detection (drums stem)
│   ├── hihat_detector.py          # Hi-hat detection (drums stem)
│   ├── chord_detector.py          # Chord detection via chroma variance (other stem)
│   ├── melody_detector.py         # Melodic activity detection (other stem)
│   ├── synth_detector.py          # Synth/pad detection (other stem)
│   ├── reverb_detector.py         # Reverb estimation (other stem)
│   ├── drop_detector.py           # Drop detection (drums stem)
│   ├── buildup_detector.py        # Build-up detection (other stem)
│   ├── vocal_analyzer.py          # Whisper vocal segment detection (vocals stem)
│   ├── lyric_gap_detector.py      # Vocal gap identification
│   ├── event_classifier.py        # Multi-feature event classification
│   ├── ranking_engine.py          # Musical quality × vocal safety scoring
│   ├── dual_song_matcher.py       # Cross-song transition pair matching
│   ├── transition_scorer.py       # Weighted transition scoring
│   ├── transition_recommender.py  # Cross-song SFX recommendations with timing
│   ├── explanation_engine.py      # Plain-English transition reasoning
│   ├── manual_analyzer.py         # Manual/range mode utilities
│   ├── bpm_compatibility.py       # BPM matching with half/double time
│   ├── harmonic_compatibility.py  # Key compatibility via Camelot wheel
│   ├── similarity_engine.py       # Spectral similarity scoring
│   ├── music_context_engine.py    # Musical context tagging
│   ├── confidence_engine.py       # Confidence scoring
│   └── frequency_analyzer.py     # Frequency band analysis
├── templates/
│   ├── index.html                 # Upload UI with mode selector
│   └── results.html               # Results page with full analysis
├── songs/                         # Uploaded audio (gitignored)
├── separated/                     # Demucs stem cache (gitignored)
├── requirements.txt
└── .gitignore
```

---

## 🚀 Installation

**Prerequisites:** Python 3.9+, pip, ffmpeg

```bash
# Clone the repo
git clone https://github.com/rishis1206/music-transition-assistant.git
cd music-transition-assistant

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir songs
mkdir -p separated/htdemucs

# Run
python app.py
```

Then open `http://127.0.0.1:5000`

> **Note:** First time a song is uploaded, Demucs will separate it into stems (2–4 mins on CPU). Every subsequent upload of the same song is instant due to caching.

---

## ⚙️ How It Works

### Analysis Pipeline

```
MP3 Upload
    ↓
Demucs Stem Separation (bass / drums / vocals / other)
    ↓
Stem-Specific Detection:
  bass stem    → bass analyzer + 808 detector
  drums stem   → kick + snare + hihat + drop detector
  other stem   → chord + melody + synth + reverb + buildup detector
  vocals stem  → Whisper transcription → vocal gap detection
    ↓
Full mix → BPM + beat detection + energy analysis + feature extraction
    ↓
Event Classifier (scores every candidate point, assigns event type)
    ↓
Ranking Engine (musical quality × vocal safety multiplier)
    ↓
Dual Song Matcher (cross-references Song A × Song B with BPM + harmonic + vocal scoring)
    ↓
SFX Recommender (cross-song context aware, millisecond timing)
    ↓
Explanation Engine (reasons, strengths, warnings, verdict)
    ↓
Flask renders results
```

### Scoring Formula

```
Musical Score = bass(18) + energy(18) + rms(10) + 808(10) + kick(10)
              + snare(8) + hihat(6) + chord(6) + melody(5) + synth(4) + reverb(2)

Final Score = Musical Score × Vocal Safety Multiplier (1.0 – 1.3)

Compatibility % = BPM score(40%) + Harmonic score(35%) + Similarity(25%)
```

### Why Stem Separation Matters

Without stems, a bass detector analyzing a full mix picks up bleed from kick drums, vocals, and synths in overlapping frequency ranges. With Demucs isolating each source first, every detector only sees its relevant audio — dramatically improving accuracy. Whisper on a clean vocal stem also eliminates false transcriptions from background instrumentation.

### Chord Detection Fix

Original implementation used `np.max(chroma, axis=0)` — this grabs the loudest pitch class per frame, which is always high in any musical content, causing 90%+ of frames to be classified as chords. Fixed using **chroma variance** — real chords spread energy across multiple pitch classes simultaneously (low variance), while melody or percussion concentrates in fewer bins (high variance). Inverting variance gives accurate chord detection.

---

## 🎛 Transition Modes

| Mode | Song A | Song B | Use Case |
|---|---|---|---|
| Auto → Auto | AI searches full song | AI searches full song | Quick analysis |
| Manual → Auto | You set exit point | AI finds best entry | You know your Song A cut |
| Auto → Manual | AI finds best exit | You set entry point | You know your Song B start |
| Manual → Manual | You set both | AI evaluates quality | Verify a specific transition |
| Range → Range | You set search window | You set search window | Work within specific sections |

---

## ⚠️ Known Limitations

- Demucs + Whisper run on CPU — first-time analysis takes 3–5 mins per song (cached after)
- High reverb/synth scores on atmospheric music are by design (Metro Boomin correctly scores high)
- All component detectors are DSP rule-based — ML model training planned for v2
- No in-browser audio playback yet

---

## 🗺 Roadmap

- [ ] Async processing so UI doesn't block during analysis
- [ ] In-browser audio preview at transition point
- [ ] Waveform timeline with drag-and-drop markers
- [ ] Genre detection (trap, EDM, lo-fi, phonk, house)
- [ ] Essentia integration for ML-based component classification
- [ ] Export transition report as PDF
- [ ] Mobile responsive layout
- [ ] Deployment to cloud with GPU support

---

## 👨‍💻 Developer

**Rishi S**
Final Year AI & ML Student — GMIT, Davangere (VTU)

---

## 📄 License
