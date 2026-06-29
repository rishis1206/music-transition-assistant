def calculate_bpm_score(bpm1, bpm2):
    """
    Returns 0.0 to 1.0 based on how compatible two BPMs are.
    Accounts for double/half time relationships common in DJ mixing.
    """

    if bpm1 == 0 or bpm2 == 0:
        return 0.5  # unknown, neutral score

    # Check direct match
    direct_diff = abs(bpm1 - bpm2)

    # Check half/double time (e.g. 140 BPM into 70 BPM is fine)
    half_diff = abs(bpm1 - bpm2 * 2)
    double_diff = abs(bpm1 * 2 - bpm2)

    best_diff = min(direct_diff, half_diff, double_diff)

    # Within 3 BPM = perfect
    # Within 10 BPM = good
    # Within 20 BPM = okay
    # Beyond 20 BPM = penalize hard

    if best_diff <= 3:
        return 1.0
    elif best_diff <= 10:
        return round(1.0 - (best_diff - 3) / 7 * 0.3, 3)
    elif best_diff <= 20:
        return round(0.7 - (best_diff - 10) / 10 * 0.4, 3)
    else:
        return round(max(0.0, 0.3 - (best_diff - 20) / 40), 3)