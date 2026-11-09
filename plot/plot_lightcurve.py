"""Visualize the Kepler-10 light curve from the CSV file (no download here).

Optionally removes the slow stellar variability (flatten) and folds the signal
on the known orbital period of Kepler-10b, for visual validation only.
"""

from pathlib import Path

import pandas as pd
import lightkurve as lk
import matplotlib.pyplot as plt

CSV_FILE = "kepler10_lightcurve.csv"
RESULTS_DIR = Path("results")   # Folder where the figure is saved
PERIOD = 0.837491        # Orbital period of Kepler-10b (days)
FLATTEN_WINDOW = 401     # Flatten filter window, in samples (must be odd)
BIN_SIZE = 0.01          # Bin width (days)

FLATTEN = True           # Remove the slow stellar variability
FOLD = False              # Fold the light curve on PERIOD


def main():
    df = pd.read_csv(CSV_FILE)
    lc = lk.LightCurve(time=df["time"], flux=df["flux"])

    title = "Kepler-10 light curve"

    if FLATTEN:
        lc = lc.flatten(window_length=FLATTEN_WINDOW)
        title += ", flattened"

    if FOLD:
        lc = lc.fold(period=PERIOD)
        title += f", folded at P = {PERIOD} d"

    # Bin the points to smooth the noise and make the dip visible
    binned_lc = lc.bin(time_bin_size=BIN_SIZE)

    binned_lc.scatter()
    plt.title(title)

    # Save the figure (must be done before plt.show(), which clears it)
    RESULTS_DIR.mkdir(exist_ok=True)
    filename = "lightcurve_folded.png" if FOLD else "lightcurve.png"
    plt.savefig(RESULTS_DIR / filename, dpi=300, bbox_inches="tight")
    print(f"Figure saved to {RESULTS_DIR / filename}")

    plt.show()


if __name__ == "__main__":
    main()