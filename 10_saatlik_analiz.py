
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. TEMIZ VERILERI OKU
kore = pd.read_csv("outputs/kore_temiz.csv")

almanya = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 2. TARIH SUTUNLARINI DONUSTUR
kore["tarih"] = pd.to_datetime(
    kore["tarih"]
)

almanya["tarih_yerel"] = pd.to_datetime(
    almanya["tarih_yerel"]
)

# 3. SAAT BILGILERINI AYIR
kore["saat"] = kore["tarih"].dt.hour

almanya["saat"] = (
    almanya["tarih_yerel"].dt.hour
)

# 4. HER SAATIN ORTALAMA TUKETIMINI HESAPLA
kore_saat = kore.groupby("saat")["enerji_kWh"].agg(
    ["mean", "count"]
)

almanya_saat = almanya.groupby("saat")["enerji_kWh"].agg(
    ["mean", "count"]
)

# 5. KARSILASTIRMA TABLOSU OLUSTUR
tablo = pd.DataFrame({
    "Saat": range(24)
})

tablo["Kore_ortalama_kWh"] = (
    kore_saat["mean"].reindex(range(24)).to_numpy()
)

tablo["Almanya_ortalama_kWh"] = (
    almanya_saat["mean"].reindex(range(24)).to_numpy()
)

tablo["Kore_kayit_sayisi"] = (
    kore_saat["count"].reindex(range(24)).to_numpy()
)

tablo["Almanya_kayit_sayisi"] = (
    almanya_saat["count"].reindex(range(24)).to_numpy()
)

# 6. GORELI TUKETIM HESAPLA
tablo["Kore_goreli"] = (
    tablo["Kore_ortalama_kWh"]
    / kore["enerji_kWh"].mean()
)

tablo["Almanya_goreli"] = (
    tablo["Almanya_ortalama_kWh"]
    / almanya["enerji_kWh"].mean()
)

print("\n--- SAATLIK TUKETIM ANALIZI ---")
print(tablo.round(3).to_string(index=False))

# 7. EN YUKSEK VE EN DUSUK SAATLER
for isim, sutun in [
    ("Guney Kore", "Kore_goreli"),
    ("Almanya LG30", "Almanya_goreli")
]:
    yuksek = tablo.loc[tablo[sutun].idxmax()]
    dusuk = tablo.loc[tablo[sutun].idxmin()]

    print("\n", isim)
    print("En yuksek saat:", int(yuksek["Saat"]))
    print("En dusuk saat:", int(dusuk["Saat"]))

# 8. GRAFIK OLUSTUR
fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(
    tablo["Saat"],
    tablo["Kore_goreli"],
    marker="o",
    linewidth=2,
    label="Guney Kore"
)

ax.plot(
    tablo["Saat"],
    tablo["Almanya_goreli"],
    marker="s",
    linewidth=2,
    label="Almanya LG30"
)

# Genel ortalamayi gosteren cizgi
ax.axhline(
    1,
    color="gray",
    linestyle="--",
    label="Genel ortalama"
)

ax.set_title(
    "Saatlere Gore Goreli Elektrik Tuketimi",
    fontsize=15
)

ax.set_xlabel("Gunun Saati")
ax.set_ylabel(
    "Saatlik Ortalama / Genel Ortalama"
)

ax.set_xticks(range(0, 24, 2))
ax.set_xlim(0, 23)

ax.grid(alpha=0.25)
ax.legend()

# 9. SONUCLARI KAYDET
Path("outputs/grafikler").mkdir(
    parents=True,
    exist_ok=True
)

tablo.to_csv(
    "outputs/saatlik_tuketim_analizi.csv",
    index=False,
    encoding="utf-8-sig"
)

plt.tight_layout()

plt.savefig(
    "outputs/grafikler/04_saatlik_tuketim.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nSaatlik analiz tamamlandi!")

