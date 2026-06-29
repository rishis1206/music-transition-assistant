import numpy as np


def build_music_context(event):
    """
    Generate a musical context from detector outputs.
    """

    context = []

    if event["bass_strength"] > 0.70:
        context.append("Strong Bass")

    if event["sub808_strength"] > 0.70:
        context.append("Strong 808")

    if event["kick_strength"] > 0.65:
        context.append("Strong Kick")

    if event["snare_strength"] > 0.60:
        context.append("Strong Snare")

    if event["hihat_strength"] > 0.60:
        context.append("Busy HiHats")

    if event["energy_strength"] > 0.75:
        context.append("High Energy")

    if event["chord_strength"] > 0.65:
        context.append("Chord Progression")

    if event["melody_strength"] > 0.65:
        context.append("Strong Melody")

    if event["synth_strength"] > 0.60:
        context.append("Synth Present")

    if event["reverb_strength"] > 0.60:
        context.append("Wide Atmosphere")

    if event["confidence"] > 0.75:
        context.append("Important Musical Event")

    return context