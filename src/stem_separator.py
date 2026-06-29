import subprocess
import os
import sys


def separate_stems(file_path):
    """
    Run Demucs on a file and return paths to the 4 stems.
    If stems already exist for this file, skip separation and return cached paths.
    """

    song_name = os.path.splitext(os.path.basename(file_path))[0]
    stem_dir = os.path.join("separated", "htdemucs", song_name)

    stems = {
        "bass":   os.path.join(stem_dir, "bass.mp3"),
        "drums":  os.path.join(stem_dir, "drums.mp3"),
        "other":  os.path.join(stem_dir, "other.mp3"),
        "vocals": os.path.join(stem_dir, "vocals.mp3")
    }

    # Check if stems already exist — skip Demucs if so
    all_exist = all(os.path.exists(p) for p in stems.values())

    if all_exist:
        print(f"[Demucs] Using cached stems for {song_name}")
        return stems

    # Stems don't exist — run Demucs using the SAME Python as the app
    print(f"[Demucs] Separating stems for {song_name} (first time, may take a few minutes)...")

    result = subprocess.run(
        [sys.executable, "-m", "demucs", "--mp3", file_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[Demucs] Warning: separation failed: {result.stderr}")
        print(f"[Demucs] Falling back to full mix analysis")
        return None

    # Verify all stems exist after separation
    all_exist = all(os.path.exists(p) for p in stems.values())
    if not all_exist:
        print(f"[Demucs] Warning: some stems missing after separation")
        return None

    print(f"[Demucs] Stems ready and cached for {song_name}")
    return stems