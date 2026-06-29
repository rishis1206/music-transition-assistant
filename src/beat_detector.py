import librosa

def detect_beats(audio, sample_rate):

    tempo, beats = librosa.beat.beat_track(
        y=audio,
        sr=sample_rate
    )

    beat_times = librosa.frames_to_time(
        beats,
        sr=sample_rate
    )

    try:
        bpm = round(
            float(tempo[0]),
            2
        )
    except:
        bpm = round(
            float(tempo),
            2
        )

    return {
        "bpm": bpm,
        "beats": beats,
        "beat_times": beat_times
    }