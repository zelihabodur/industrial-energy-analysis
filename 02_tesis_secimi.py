
import pandas as pd

# Almanya veri setini oku
almanya = pd.read_csv(
    "data/LoadProfile_30IPs_2017.csv",
    sep=";",
    header=1
)

# 30 isletmeye ait sutunlari bul
lg_sutunlari = [
    sutun for sutun in almanya.columns
    if sutun.startswith("LG ")
]

# Butun isletmelerin olcumu eksik olan
# satirlari yalnizca analiz icin ayir
tamamen_bos = (
    almanya[lg_sutunlari].isna().all(axis=1)
)

veriler = almanya.loc[
    ~tamamen_bos, lg_sutunlari
]

# Isletmelerin istatistiklerini hesapla
ozet = pd.DataFrame({
    "eksik": veriler.isna().sum(),
    "negatif": (veriler < 0).sum(),
    "sifir": (veriler == 0).sum(),
    "ortalama_kW": veriler.mean(),
    "medyan_kW": veriler.median(),
    "std_kW": veriler.std()
})

# Goreli degiskenlik
ozet["degisim_katsayisi"] = (
    ozet["std_kW"] / ozet["ortalama_kW"]
)

# Sifir olcum yuzdesi
ozet["sifir_yuzde"] = (
    ozet["sifir"] / veriler.notna().sum() * 100
)

print("\n--- ISLETME SECIM ANALIZI ---")

print("Incelenen isletme:", len(lg_sutunlari))
print("Analize alinan zaman kaydi:", len(veriler))

print(
    ozet.round(3).to_string()
)

# Sonuclari CSV dosyasina kaydet
from pathlib import Path

Path("outputs").mkdir(exist_ok=True)

ozet.round(3).to_csv(
    "outputs/almanya_tesis_ozeti.csv",
    index_label="isletme",
    encoding="utf-8-sig"
)

print("\nIsletme ozeti dosyaya kaydedildi.")
