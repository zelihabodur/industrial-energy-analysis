
import pandas as pd

# 1. HAM VERILERI OKU
kore_ham = pd.read_csv(
    "data/Steel_industry_data.csv"
)

almanya_ham = pd.read_csv(
    "data/LoadProfile_30IPs_2017.csv",
    sep=";",
    header=1
)

# 2. TEMIZ VERILERI OKU
kore_temiz = pd.read_csv(
    "outputs/kore_temiz.csv"
)

almanya_temiz = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 3. ALMANYA BOS SATIR KONTROLU
lg = [
    s for s in almanya_ham.columns
    if s.startswith("LG ")
]

bos_satir = (
    almanya_ham[lg].isna().all(axis=1)
)

# 4. KORE TARIH DUZELTMESI KONTROLU
eski_tarih = pd.to_datetime(
    kore_ham["date"],
    format="%d/%m/%Y %H:%M"
)

yeni_tarih = pd.to_datetime(
    kore_temiz["tarih"]
)

duzeltilen = (
    (yeni_tarih - eski_tarih)
    == pd.Timedelta(days=1)
).sum()

# 5. ONCESI VE SONRASI
print("\n--- VERI TEMIZLEME KANITI ---")

print("\nGUNEY KORE")
print("Ham kayit:", len(kore_ham))
print("Temiz kayit:", len(kore_temiz))
print("Duzeltilen tarih:", duzeltilen)
print(
    "Temiz veride eksik enerji:",
    kore_temiz["enerji_kWh"].isna().sum()
)

print("\nALMANYA LG30")
print("Ham kayit:", len(almanya_ham))
print("Bos satir:", bos_satir.sum())
print("Temiz kayit:", len(almanya_temiz))
print(
    "Korunan b kaydi:",
    almanya_temiz["tekrarlanan_saat"]
    .astype(str).str.lower().eq("true").sum()
)
print(
    "Temiz veride eksik enerji:",
    almanya_temiz["enerji_kWh"].isna().sum()
)

# 6. SONUCLARI TABLOYA DONUSTUR
ozet = pd.DataFrame({
    "Isletme": ["Guney Kore", "Almanya LG30"],
    "Ham kayit": [
        len(kore_ham), len(almanya_ham)
    ],
    "Temiz kayit": [
        len(kore_temiz), len(almanya_temiz)
    ],
    "Cikarilan kayit": [
        len(kore_ham) - len(kore_temiz),
        len(almanya_ham) - len(almanya_temiz)
    ],
    "Eksik enerji (son)": [
        kore_temiz["enerji_kWh"].isna().sum(),
        almanya_temiz["enerji_kWh"].isna().sum()
    ]
})

ozet.to_csv(
    "outputs/veri_temizleme_kaniti.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nKANIT TABLOSU:")
print(ozet.to_string(index=False))
