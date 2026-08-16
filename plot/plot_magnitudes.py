import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./magnitudes.csv")

plt.plot(df["freq"], df["magnitudes"])
plt.xlabel("frequency (cycles/day)")
plt.ylabel("magnitude")
plt.title("DFT spectrum")

mask = (df["freq"] > 1.0) & (df["freq"] < 1.4)
idx_max_zoom = df[mask]["magnitudes"].idxmax()
print(df.loc[idx_max_zoom])

plt.show()
