# Kepler-10b transit detection from real light curve data

Second part of the pulsar signal-processing project. Reuses the same core technique (Discrete Fourier Transform, hand-coded in C) but applied to **real observational data** instead of a simulation: detecting the orbital period of the exoplanet Kepler-10b from its host star's brightness measurements. The period is not given as input to the DFT: it is read off the frequency spectrum.

## Physical background

When Kepler-10b passes in front of its star (a transit), it blocks a tiny fraction of the star's light. To first order, the relative depth of the dip is the ratio of the projected areas:

$$\delta \approx \left( \frac{R_p}{R_\star} \right)^2$$

For Kepler-10b this is of the order of 0.02 % (a couple hundred ppm). Since the transit repeats every orbit, this produces a **periodic dip** hidden in the star's light curve, buried under stellar variability (starspots, rotation) that is much larger in amplitude. A Fourier transform of the raw flux reveals this hidden periodicity as a peak in the frequency spectrum.

## Project files

- [`fetch_light_curve.py`](fetch_light_curve.py) — downloads the Kepler-10 light curve via the `lightkurve` package (MAST archive) and exports it to CSV. Run once; no need to re-download afterwards.
- [`kepler10_lightcurve.csv`](kepler10_lightcurve.csv) — light curve for a single Kepler quarter (regularly sampled, ~30 min cadence, no large gaps). This is the file actually used as DFT input.
- [`kepler10_lightcurve_full.csv`](kepler10_lightcurve_full.csv) — light curve stitched across all available quarters. It contains large observation gaps (up to ~89 days) between quarters, which break the DFT's assumption of uniform sampling. It is kept for reference and visual inspection (phase-folding), and is not used as DFT input.
- [`dft.c`](dft.c) — reads `kepler10_lightcurve.csv`, computes the DFT of the mean-centered flux, and writes the magnitude spectrum to `magnitudes.csv`.
- [`plot/plot_lightcurve.py`](plot/plot_lightcurve.py) — visualizes the raw and/or phase-folded light curve (using `lightkurve`'s `flatten`/`fold`/`bin`, for visual validation only, not part of the C detection pipeline).
- [`plot/plot_magnitudes.py`](plot/plot_magnitudes.py) — plots the DFT spectrum (`magnitude` vs. `frequency`) from `magnitudes.csv`.
- [`magnitudes.csv`](magnitudes.csv) — output of `dft.c`: the computed spectrum.
- [`Makefile`](Makefile) — build rule for `dft`.

## Build

```bash
make dft
./dft
```

## Method

1. Download the light curve once (`fetch_light_curve.py`): normalized flux (~1.0 baseline) sampled roughly every 30 minutes.
2. Read `time,flux` from CSV in `dft.c` and mean-center the flux. No other preprocessing (no detrending, no folding): the DFT works on the raw signal.
3. Compute $\mathrm{Re}(X[k])$ and $\mathrm{Im}(X[k])$ naively ($O(N^2)$, not a radix-2 FFT) for $k = 0$ to $N/2$ (spectrum symmetry for a real-valued signal).
4. Convert the bin index to a physical frequency, in cycles/day:
$$f_k = \frac{k}{N \, \mathrm{DT}}$$
where `DT` is measured directly from the data (mean time step between consecutive samples, ≈ 0.0207 day ≈ 29.8 min).
5. Look for the peak in the frequency range around the expected transit frequency.

## Result

A clear peak is detected around **f ≈ 1.19–1.2 cycles/day**, corresponding to a period of **≈ 0.837 days**, consistent with Kepler-10b's known orbital period (0.837491 ± 0.000002 days, [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/overview/Kepler-10)).

This peak is a *local* maximum, not the global maximum of the spectrum: the largest peak corresponds to low-frequency stellar variability (starspots/rotation), since no detrending was applied. The peak therefore has to be searched for around the expected frequency, so the result is a confirmation of a known period rather than a fully blind detection.

## Reference values

| Quantity | Value |
|---|---|
| Kepler-10b orbital period | 0.837491 ± 0.000002 days |
| Transit depth | ≈ 0.02 % (order of 200 ppm) |
| Sampling cadence (measured) | ≈ 0.020677 day (≈ 29.8 min, Kepler long cadence) |
| Frequency resolution (one quarter, ~90 days) | $\Delta f = 1/(N\,\mathrm{DT}) \approx 0.011$ cycle/day |

Because of the frequency resolution, the period can only be claimed to two or three significant digits from a single quarter.

## Notes / limitations

- Only a single Kepler quarter is used as DFT input, to keep the sampling uniform (no large gaps), a requirement of the naive DFT as implemented here.
- No detrending (`flatten`) is applied before the DFT; the stellar variability dominates the low-frequency end of the spectrum.
- As in the pulsar project, this is a direct $O(N^2)$ DFT, not an optimized FFT.

## TODO

- [ ] **Detrending**: remove the low-frequency stellar variability with a simple high-pass filter, and check that the transit peak becomes the global maximum of the spectrum.
- [ ] **Significance**: quantify the peak (height compared to the surrounding noise floor of the spectrum).
- [ ] **Phase-folding**: fold the light curve at the period found to visually check the shape of the transit.
- [ ] **Non-uniform sampling**: handle the multi-quarter light curve (with gaps) with a Lomb-Scargle periodogram, which does not require regular sampling, to gain frequency resolution.
- [ ] **FFT**: replace the naive DFT with a radix-2 Cooley-Tukey FFT ($O(N \log N)$) and compare computation times.

## References

- [NASA Exoplanet Archive: Kepler-10](https://exoplanetarchive.ipac.caltech.edu/overview/Kepler-10) — orbital parameters of Kepler-10b
- [MAST archive](https://archive.stsci.edu/) — source of the Kepler light curves, accessed through `lightkurve`
