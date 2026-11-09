"""Plot the DFT magnitude spectrum and report the peak near the expected transit frequency."""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "magnitudes.csv"
RESULTS_DIR = Path("results")   # Folder where the figure is saved
FREQ_MIN = 1.0   # Search window around the expected transit frequency (cycles/day)
FREQ_MAX = 1.4


def main():
    df = pd.read_csv(CSV_FILE)

    plt.plot(df["freq"], df["magnitudes"])
    plt.xlabel("frequency (cycles/day)")
    plt.ylabel("magnitude")
    plt.title("DFT spectrum")

    # Highest peak inside the search window (not the global maximum of the spectrum)
    in_window = (df["freq"] > FREQ_MIN) & (df["freq"] < FREQ_MAX)
    idx_peak = df.loc[in_window, "magnitudes"].idxmax()
    peak_freq = df.loc[idx_peak, "freq"]
    peak_magnitude = df.loc[idx_peak, "magnitudes"]

    print(f"Peak in [{FREQ_MIN}, {FREQ_MAX}] cycles/day:")
    print(f"  frequency : {peak_freq:.4f} cycles/day")
    print(f"  period    : {1 / peak_freq:.4f} days")
    print(f"  magnitude : {peak_magnitude:.2f}")

    # Save the figure (must be done before plt.show(), which clears it)
    RESULTS_DIR.mkdir(exist_ok=True)
    filename = "dft_spectrum.png"
    plt.savefig(RESULTS_DIR / filename, dpi=300, bbox_inches="tight")
    print(f"Figure saved to {RESULTS_DIR / filename}")

    plt.show()


if __name__ == "__main__":
    main()