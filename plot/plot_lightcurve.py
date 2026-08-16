import pandas as pd
import lightkurve as lk
import matplotlib.pyplot as plt

# Lecture du CSV déjà téléchargé (aucun téléchargement ici)
df = pd.read_csv("kepler10_lightcurve.csv")
lc = lk.LightCurve(time=df["time"], flux=df["flux"])

# Retire la tendance lente de variabilité stellaire
#flat_lc = lc.flatten(window_length=401)

# Replie le signal sur la période connue de Kepler-10b (0.837491 jours)
#folded_lc = flat_lc.fold(period=0.837491)

# Regroupe les points par bins pour lisser le bruit et voir le creux net
binned_lc = lc.bin(time_bin_size=0.01)

binned_lc.scatter()
plt.title("Kepler-10b - transit replié (tous quarters)")
plt.show()
