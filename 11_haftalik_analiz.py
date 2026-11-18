
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. TEMIZ VERILERI OKU

kore = pd.read_csv("outputs/kore_temiz.csv")

almanya = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 2. TARIH SUTUNLARINI DONUSTUR

kore["tarih"] = pd.to_datetime(kore["tarih"])

almanya["tarih_yerel"] = pd.to_datetime(
    almanya["tarih_yerel"]
)

# Iki veri setinin ilgili yilini kullan
kore = kore[kore["tarih"].dt.year == 2018].copy()

almanya = almanya[
    almanya["tarih_yerel"].dt.year == 2017
].copy()

# 3. HAFTANIN GUNUNU BUL

# Pazartesi = 0, Pazar = 6
kore["hafta_gunu"] = kore["tarih"].dt.dayofweek

almanya["hafta_gunu"] = (
    almanya["tarih_yerel"].dt.dayofweek
)

gunler = [
    "Pazartesi", "Sali", "Carsamba",
    "Persembe", "Cuma", "Cumartesi", "Pazar"
]

# 4. HAFTALIK ORTALAMALARI HESAPLA

kore_hafta = kore.groupby("hafta_gunu")[
    "enerji_kWh"
].agg(["mean", "count"]).reindex(range(7))

almanya_hafta = almanya.groupby("hafta_gunu")[
    "enerji_kWh"
].agg(["mean", "count"]).reindex(range(7))

# 5. KARSILASTIRMA TABLOSU

tablo = pd.DataFrame({
    "Gun": gunler,
    "Kore_ortalama_kWh": kore_hafta["mean"].to_numpy(),
    "Almanya_ortalama_kWh": almanya_hafta["mean"].to_numpy(),
    "Kore_kayit": kore_hafta["count"].to_numpy(),
    "Almanya_kayit": almanya_hafta["count"].to_numpy()
})

tablo["Kore_goreli"] = (
    tablo["Kore_ortalama_kWh"]
    / kore["enerji_kWh"].mean()
)

tablo["Almanya_goreli"] = (
    tablo["Almanya_ortalama_kWh"]
    / almanya["enerji_kWh"].mean()
)

print("\n--- HAFTALIK TUKETIM ANALIZI ---")
print(tablo.round(3).to_string(index=False))

# 6. HAFTA ICI VE HAFTA SONU ANALIZI

for isim, veri in [
    ("Guney Kore", kore),
    ("Almanya LG30", almanya)
]:

    hafta_ici = veri.loc[
        veri["hafta_gunu"] < 5, "enerji_kWh"
    ].mean()

    hafta_sonu = veri.loc[
        veri["hafta_gunu"] >= 5, "enerji_kWh"
    ].mean()

    fark_yuzde = (
        (hafta_sonu - hafta_ici)
        / hafta_ici * 100
    )

    print("\nIsletme:", isim)
    print("Hafta ici ortalama:", round(hafta_ici, 3))
    print("Hafta sonu ortalama:", round(hafta_sonu, 3))
    print("Hafta sonu farki (%):", round(fark_yuzde, 2))

# 7. GRAFIK OLUSTUR

fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(
    gunler,
    tablo["Kore_goreli"],
    marker="o",
    linewidth=2.5,
    label="Guney Kore"
)

ax.plot(
    gunler,
    tablo["Almanya_goreli"],
    marker="s",
    linewidth=2.5,
    label="Almanya LG30"
)

ax.axhline(
    1,
    linestyle="--",
    color="gray",
    label="Genel ortalama"
)

ax.set_title(
    "Haftanin Gunlerine Gore Goreli Enerji Tuketimi",
    fontsize=15
)

ax.set_xlabel("Haftanin Gunu")
ax.set_ylabel(
    "Gunluk Ortalama Olcum / Genel Ortalama"
)

ax.grid(alpha=0.25)
ax.legend()

plt.xticks(rotation=20)

# 8. SONUCLARI KAYDET

Path("outputs/grafikler").mkdir(
    parents=True,
    exist_ok=True
)

tablo.to_csv(
    "outputs/haftalik_tuketim_analizi.csv",
    index=False,
    encoding="utf-8-sig"
)

plt.tight_layout()

plt.savefig(
    "outputs/grafikler/05_haftalik_tuketim.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nHaftalik analiz tamamlandi!")

