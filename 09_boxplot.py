
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Verileri oku
kore = pd.read_csv("outputs/kore_temiz.csv")
almanya = pd.read_csv("outputs/almanya_LG30_temiz.csv")

# 2. Goreli tuketimleri hesapla
kore_goreli = (
    kore["enerji_kWh"] / kore["enerji_kWh"].mean()
)

almanya_goreli = (
    almanya["enerji_kWh"] / almanya["enerji_kWh"].mean()
)

veriler = [kore_goreli, almanya_goreli]
isimler = ["Guney Kore", "Almanya LG30"]

# 3. Grafik olustur
fig, ax = plt.subplots(figsize=(10, 7))

bp = ax.boxplot(
    veriler,
    patch_artist=True,
    widths=0.5,
    showmeans=True,
    showfliers=True,
    medianprops={
        "color": "darkred",
        "linewidth": 3
    },
    meanprops={
        "marker": "D",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
        "markersize": 7
    },
    flierprops={
        "marker": "o",
        "markersize": 2,
        "markerfacecolor": "gray",
        "markeredgecolor": "gray",
        "alpha": 0.25
    }
)

# 4. Iki kutuya farkli renk ver
renkler = ["#4C9BD6", "#F2A65A"]

for kutu, renk in zip(bp["boxes"], renkler):
    kutu.set_facecolor(renk)
    kutu.set_alpha(0.8)

# 5. Baslik ve eksenler
ax.set_xticks([1, 2])
ax.set_xticklabels(isimler)

ax.set_title(
    "Isletmelerin Goreli Enerji Tuketimi - Boxplot",
    fontsize=15,
    fontweight="bold"
)

ax.set_ylabel(
    "Enerji Tuketimi / Isletme Ortalamasi"
)

# Ortalama referans cizgisi
ax.axhline(
    1,
    color="gray",
    linestyle="--",
    alpha=0.7,
    label="Ortalama seviyesi (1)"
)

ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)
ax.legend()

# 6. Istatistiksel degerleri hesapla
print("\n--- BOXPLOT ISTATISTIKLERI ---")

for isim, veri in zip(isimler, veriler):

    q1 = veri.quantile(0.25)
    medyan = veri.median()
    q3 = veri.quantile(0.75)
    iqr = q3 - q1

    alt = q1 - 1.5 * iqr
    ust = q3 + 1.5 * iqr

    aykiri = ((veri < alt) | (veri > ust))

    print("\n", isim)
    print("Q1:", round(q1, 3))
    print("Medyan:", round(medyan, 3))
    print("Q3:", round(q3, 3))
    print("IQR:", round(iqr, 3))
    print("Aykiri deger:", int(aykiri.sum()))
    print("Aykiri oran %:",
          round(aykiri.mean() * 100, 2))

# 7. Grafigi kaydet
Path("outputs/grafikler").mkdir(
    parents=True,
    exist_ok=True
)

plt.tight_layout()

plt.savefig(
    "outputs/grafikler/03_kutu_grafigi.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nGrafik basariyla guncellendi!")
