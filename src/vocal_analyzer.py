import whisper

_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def analyze_vocals(file_path):
    """
    Use Whisper to detect vocal segments and their timestamps.
    Returns empty list if Whisper fails instead of crashing.
    """

    try:
        model = get_model()

        result = model.transcribe(
            file_path,
            task="transcribe",
            word_timestamps=False,
            fp16=False
        )

        segments = []

        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })

        return segments

    except Exception as e:
        print(f"[Whisper] Warning: vocal analysis failed for {file_path}: {e}")
        print("[Whisper] Continuing without vocal gap detection.")
        return []