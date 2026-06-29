import matplotlib.pyplot as plt

def plot_energy(
    times,
    rms
):

    plt.figure(
        figsize=(12, 4)
    )

    plt.plot(
        times,
        rms
    )

    plt.title(
        "Song Energy Curve"
    )

    plt.xlabel(
        "Time (seconds)"
    )

    plt.ylabel(
        "Energy"
    )

    plt.tight_layout()

    plt.show()