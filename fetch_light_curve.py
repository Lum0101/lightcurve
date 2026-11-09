"""Download the Kepler-10 light curve from MAST and export it to CSV.

Two files are produced:
  - kepler10_lightcurve.csv       : a single quarter (regular sampling), used as DFT input
  - kepler10_lightcurve_full.csv  : all quarters stitched together (large gaps), for visual inspection only
"""

import lightkurve as lk

TARGET = "Kepler-10"
EXPTIME = 1800   # Long cadence, in seconds (~30 min)
QUARTER = 4      # Quarter used as DFT input


def export_light_curve(filename, quarter=None):
    """Download the light curve (one quarter, or all if quarter is None) and write time,flux to CSV."""
    search_kwargs = {"author": "Kepler", "exptime": EXPTIME}
    if quarter is not None:
        search_kwargs["quarter"] = quarter

    search_result = lk.search_lightcurve(TARGET, **search_kwargs)
    lc_collection = search_result.download_all()

    # Concatenate the quarters into a single light curve, drop NaNs, normalize flux to ~1.0
    lc = lc_collection.stitch()
    lc = lc.remove_nans().normalize()

    df = lc.to_pandas().reset_index()
    df[["time", "flux"]].to_csv(filename, index=False)
    print(f"{filename} written successfully ({len(df)} points).")


if __name__ == "__main__":
    export_light_curve("kepler10_lightcurve.csv", quarter=QUARTER)
    export_light_curve("kepler10_lightcurve_full.csv")