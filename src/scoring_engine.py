def calculate_score(

    energy_jump,

    bass_strength

):

    score = 0

    score += min(
        energy_jump * 300,
        50
    )

    score += min(
        bass_strength * 10,
        50
    )

    return round(score, 2)