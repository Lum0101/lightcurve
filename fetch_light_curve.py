import lightkurve as lk

# Télécharge TOUS les quarters disponibles pour Kepler-10 (pas juste un seul)
search_result = lk.search_lightcurve('Kepler-10', author='Kepler', exptime=1800)
lc_collection = search_result.download_all()

# Concatène tous les quarters en une seule courbe de lumière continue
lc = lc_collection.stitch()
lc = lc.remove_nans().normalize()

df = lc.to_pandas().reset_index()
print(df.columns.tolist())

df[['time', 'flux']].to_csv('kepler10_lightcurve_full.csv', index=False)
print(f"Fichier kepler10_lightcurve_full.csv écrit avec succès ({len(df)} points).")
