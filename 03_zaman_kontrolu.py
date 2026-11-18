
import pandas as pd

# Iki veri setini oku
kore = pd.read_csv(
    "data/Steel_industry_data.csv"
)

almanya = pd.read_csv(
    "data/LoadProfile_30IPs_2017.csv",
    sep=";",
    header=1
)

# 1. Almanya'da ayni olcumler var mi?
print("--- ALMANYA ISLETME KONTROLU ---")

print(
    "LG 27 ve LG 28 tamamen ayni mi?",
    almanya["LG 27"].equals(almanya["LG 28"])
)

lg_sutunlari = [
    s for s in almanya.columns
    if s.startswith("LG ")
]

kopyalar = [
    s for s in lg_sutunlari
    if s != "LG 30"
    and almanya[s].equals(almanya["LG 30"])
]

print("LG 30 ile ayni sutunlar:", kopyalar)

# 2. Kore tarihlerini incele
print("\n--- KORE ZAMAN KONTROLU ---")

tarih = pd.to_datetime(
    kore["date"],
    format="%d/%m/%Y %H:%M",
    errors="coerce"
)

farklar = tarih.diff()

print("Gecersiz tarih:", tarih.isna().sum())
print("Tekrarlanan tarih:", tarih.duplicated().sum())

print(
    "Geriye giden zaman kaydi:",
    (farklar < pd.Timedelta(0)).sum()
)

print("\nZaman farklari:")
print(farklar.value_counts().head(5))

print("\nGunluk kayit sayisi dagilimi:")
gunluk_sayilar = tarih.dt.date.value_counts()
print(gunluk_sayilar.value_counts().sort_index())
