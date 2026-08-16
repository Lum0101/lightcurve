# Kepler-10b transit detection from real light curve data

Second part of the pulsar signal-processing project. Reuses the same core technique (Discrete Fourier Transform, hand-coded in C) but applied to **real observational data** instead of a simulation: detecting the orbital period of exoplanet Kepler-10b from its host star's brightness measurements, without providing the period as input.

## Physical background

When Kepler-10b passes in front of its star (a transit), it blocks a tiny fraction of the star's light (~0.02%, i.e. ~230 ppm). Since the transit repeats every orbit, this produces a **periodic dip** hidden in the star's light curve — buried under stellar variability (starspots, rotation) that is much larger in amplitude. A Fourier transform of the raw flux reveals this hidden periodicity as a peak in the frequency spectrum, without needing to know the period in advance.

## Project files

- [`fetch_light_curve.py`](fetch_light_curve.py) — downloads the Kepler-10 light curve via the `lightkurve` package (MAST archive) and exports it to CSV. Run once; no need to re-download afterwards.
- [`kepler10_lightcurve.csv`](kepler10_lightcurve.csv) — light curve for a single Kepler quarter (regularly sampled, ~30 min cadence, no large gaps). This is the file actually used as DFT input.
- [`kepler10_lightcurve_full.csv`](kepler10_lightcurve_full.csv) — light curve stitched across all available quarters. Contains large observation gaps (up to ~89 days) between quarters, which breaks the DFT's assumption of uniform sampling — kept for reference/visual inspection (phase-folding), not used as DFT input.
- [`dft.c`](dft.c) — reads `kepler10_lightcurve.csv`, computes the DFT of the (mean-centered) flux, and writes the magnitude spectrum to `magnitudes.csv`.
- [`plot/plot_lightcurve.py`](plot/plot_lightcurve.py) — visualizes the raw and/or phase-folded light curve (using `lightkurve`'s `flatten`/`fold`/`bin`, for visual validation only — not part of the C detection pipeline).
- [`plot/plot_magnitudes.py`](plot/plot_magnitudes.py) — plots the DFT spectrum (`magnitude` vs. `frequency`) from `magnitudes.csv`.
- [`magnitudes.csv`](magnitudes.csv) — output of `dft.c`: the computed spectrum.
- [`Makefile`](Makefile) — build rule for `dft`.

## Build

```bash
make dft
./dft
```

## Method

1. Download the light curve once (`fetch_light_curve.py`) — normalized flux (~1.0 baseline) sampled roughly every 30 minutes.
2. Read `time,flux` from CSV in `dft.c`, mean-center the flux (subtract 1.0) — no other preprocessing (no detrending, no folding): the DFT works on the raw signal.
3. Compute `Re(X[k])`, `Im(X[k])` naively (`O(N²)`, not a radix-2 FFT) for `k = 0` to `N/2` (spectrum symmetry for a real-valued signal).
4. Convert bin index to physical frequency: `freq = k / (N × DT)`, in cycles/day (`DT` measured directly from the data: mean time step between consecutive samples, ≈ 0.0207 day ≈ 29.8 min).
5. Look for the dominant peak in the frequency range around the expected transit frequency.

## Result

A clear peak is detected around **f ≈ 1.19–1.2 cycles/day**, corresponding to a period of **≈ 0.837 days** — consistent with Kepler-10b's known orbital period (0.837491 ± 0.000002 days, [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/overview/Kepler-10)). This peak is a *local* maximum, not the global maximum of the spectrum — the largest peak in the full spectrum corresponds to low-frequency stellar variability (starspots/rotation), not the planetary transit, since no detrending was applied.

## Reference values

| Quantity | Value |
|---|---|
| Kepler-10b orbital period | 0.837491 ± 0.000002 days |
| Transit depth | ≈ 2287 ppm (≈ 0.23%) |
| Sampling cadence (measured) | ≈ 0.020677 day (≈ 29.8 min, Kepler long cadence) |

## Notes / limitations

- Only a single Kepler quarter is used as DFT input, to keep the sampling uniform (no large gaps) — a requirement of the naive DFT as implemented here.
- No detrending (`flatten`) is applied before the DFT; the stellar variability dominates the low-frequency end of the spectrum, so the transit peak must be searched for around the expected frequency rather than taken as the spectrum's global maximum.
- As in the pulsar project, this is a direct `O(N²)` DFT, not an optimized FFT.
