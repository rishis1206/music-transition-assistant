import numpy as np

def calculate_compatibility(
    freq_data_1,
    freq_data_2
):

    bass_diff = abs(

        np.mean(
            freq_data_1["bass"]
        )

        -

        np.mean(
            freq_data_2["bass"]
        )

    )

    mids_diff = abs(

        np.mean(
            freq_data_1["mids"]
        )

        -

        np.mean(
            freq_data_2["mids"]
        )

    )

    highs_diff = abs(

        np.mean(
            freq_data_1["highs"]
        )

        -

        np.mean(
            freq_data_2["highs"]
        )

    )

    score = 100

    score -= bass_diff

    score -= mids_diff

    score -= highs_diff

    return max(
        round(score, 2),
        0
    )