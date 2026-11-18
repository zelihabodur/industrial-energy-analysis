
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 1. TEMIZ VERILERI OKU

kore = pd.read_csv("outputs/kore_temiz.csv")

almanya = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 2. ENERJI TUKETIMLERINI SEC

kore_enerji = kore["enerji_kWh"]
almanya_enerji = almanya["enerji_kWh"]

# 3. TUKETIMLERI ORTALAMAYA GORE NORMALLESTIR

kore_goreli = kore_enerji / kore_enerji.mean()

almanya_goreli = (
    almanya_enerji / almanya_enerji.mean()
)

# 4. HISTOGRAM ARALIKLARINI BELIRLE

ust_sinir = np.ceil(
    max(kore_goreli.max(), almanya_goreli.max())
)

araliklar = np.linspace(0, ust_sinir, 31)

# Kayit sayilari farkli oldugu icin yuzde kullan
kore_agirlik = np.full(
    len(kore_goreli), 100 / len(kore_goreli)
)

almanya_agirlik = np.full(
    len(almanya_goreli), 100 / len(almanya_goreli)
)

# 5. GRAFIK OLUSTUR

fig, ax = plt.subplots(figsize=(11, 6))

ax.hist(
    kore_goreli,
    bins=araliklar,
    weights=kore_agirlik,
    histtype="step",
    linewidth=2.5,
    label="Guney Kore"
)

ax.hist(
    almanya_goreli,
    bins=araliklar,
    weights=almanya_agirlik,
    histtype="step",
    linewidth=2.5,
    label="Almanya LG30"
)

# Ortalama seviyesini isaretle
ax.axvline(
    1,
    color="gray",
    linestyle="--",
    label="Ortalama seviyesi"
)

# 6. BASLIK VE EKSENLER

ax.set_title(
    "Goreli Enerji Tuketimi Dagilimlari",
    fontsize=15
)

ax.set_xlabel(
    "Enerji Tuketimi / Isletme Ortalamasi"
)

ax.set_ylabel("Kayit Orani (%)")

ax.set_xlim(0, ust_sinir)

ax.legend()
ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)

# 7. GRAFIGI KAYDET

Path("outputs/grafikler").mkdir(
    parents=True,
    exist_ok=True
)

plt.tight_layout()

plt.savefig(
    "outputs/grafikler/02_goreli_tuketim_histogrami.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Histogram basariyla kaydedildi!")

