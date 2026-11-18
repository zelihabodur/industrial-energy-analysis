
import pandas as pd

# Güney Kore veri seti
kore = pd.read_csv("data/Steel_industry_data.csv")

# Almanya veri seti
almanya = pd.read_csv(
    "data/LoadProfile_30IPs_2017.csv",
    sep=";",
    header=1
)

print("GUNEY KORE:")
print("Boyut:", kore.shape)
print(kore.head(3))

print("\nALMANYA:")
print("Boyut:", almanya.shape)
print(almanya.head(3))

# VERI KALITESI KONTROLU

print("\n--- GUNEY KORE KONTROLU ---")

print("Eksik deger sayisi:")
print(kore.isnull().sum())

print("Tekrarlanan satir sayisi:")
print(kore.duplicated().sum())

print("Veri tipleri:")
print(kore.dtypes)

print("Ilk tarih:", kore["date"].iloc[0])
print("Son tarih:", kore["date"].iloc[-1])

print("\n--- ALMANYA KONTROLU ---")

print("Eksik deger sayisi:")
print(almanya.isnull().sum())

print("Tekrarlanan satir sayisi:")
print(almanya.duplicated().sum())

print("Tekrarlanan zaman damgasi sayisi:")
print(almanya["Time stamp"].duplicated().sum())

print("Veri tipleri:")
print(almanya.dtypes)

print("Ilk tarih:", almanya["Time stamp"].iloc[0])
print("Son tarih:", almanya["Time stamp"].iloc[-1])


# ADIM 5 - TARIH VE EKSIK VERI INCELEMESI

# Tarihleri gercek tarih-saat tipine cevir
kore["tarih"] = pd.to_datetime(
    kore["date"],
    format="%d/%m/%Y %H:%M",
    errors="coerce"
)

almanya["tarih"] = pd.to_datetime(
    almanya["Time stamp"],
    format="%d.%m.%Y %H:%M:%S",
    errors="coerce"
)

# Tarih araliklarini kontrol et
print("\n--- TARIH KONTROLU ---")

print("Kore ilk tarih:", kore["tarih"].min())
print("Kore son tarih:", kore["tarih"].max())

print("Almanya ilk tarih:", almanya["tarih"].min())
print("Almanya son tarih:", almanya["tarih"].max())

print("Kore gecersiz tarih:", kore["tarih"].isna().sum())
print("Almanya gecersiz tarih:", almanya["tarih"].isna().sum())

# Almanya'daki 30 isletmenin eksik kayitlari
lg_sutunlari = [
    sutun for sutun in almanya.columns
    if sutun.startswith("LG ")
]

print("\n--- ALMANYA EKSIK VERILER ---")
print(almanya[lg_sutunlari].isna().sum().to_string())

# Eksik kayitlarin hangi tarihlerde oldugunu gor
eksik_satirlar = almanya[
    almanya[lg_sutunlari].isna().any(axis=1)
]

print("\nEksik veri bulunan satir sayisi:",
      len(eksik_satirlar))

print("\nEksik veri bulunan ilk 5 tarih:")
print(eksik_satirlar["Time stamp"].head(5))

print("\n--- ALMANYA ZAMAN ARALIKLARI ---")
print(almanya["tarih"].diff().value_counts().head(10))


# ADIM 6 - SON VERI KALITESI KONTROLU

# 30 isletmenin tamaminda veri olmayan satirlar
tamamen_bos = almanya[lg_sutunlari].isna().all(axis=1)

# En az bir isletmede veri eksik olan satirlar
eksik_var = almanya[lg_sutunlari].isna().any(axis=1)

print("\n--- EKSIK KAYIT OZETI ---")

print("Tamamen bos satir:", tamamen_bos.sum())

print("Kismen bos satir:",
      (eksik_var & ~tamamen_bos).sum())

print("\n--- TARIH ARALIGI ---")

print("Ilk tarih:", almanya["tarih"].min())
print("Son tarih:", almanya["tarih"].max())

print("Gecersiz tarih:",
      almanya["tarih"].isna().sum())

print("\n--- ZAMAN FARKLARI ---")

print(
    almanya["tarih"]
    .diff()
    .value_counts()
    .head(10)
    .to_string()
)

print("\n--- SON 5 SATIR ---")

print(
    almanya[["Time stamp", "LG 01", "LG 30"]]
    .tail(5)
    .to_string(index=False)
)


# ADIM 7 - GECERSIZ TARIHLERI ARASTIRMA

print("\n--- GECERSIZ TARIH KAYITLARI ---")

hatali_tarihler = almanya[
    almanya["tarih"].isna()
]

print(
    hatali_tarihler[
        ["Time stamp", "LG 01", "LG 30"]
    ].to_string()
)

# Hatali tarihlerin etrafindaki kayitlar
print("\n--- CEVRESINDEKI TARIHLER ---")

for idx in hatali_tarihler.index[:1]:
    print(
        almanya.loc[
            max(0, idx - 4):idx + 8,
            ["Time stamp", "LG 01", "LG 30"]
        ].to_string()
    )

# Elektrik olcumu bulunan son kayit
print("\n--- SON DOLU OLCUM ---")

dolu_satirlar = almanya[
    almanya[lg_sutunlari].notna().any(axis=1)
]

print(
    dolu_satirlar[
        ["Time stamp", "LG 01", "LG 30"]
    ].tail(3).to_string(index=False)
)


# ADIM 8 - OZEL TARIH KAYITLARINI DUZELTME

# Sonunda b bulunan tarihleri isaretle
almanya["tekrarlanan_saat"] = (
    almanya["Time stamp"]
    .str.endswith(" b")
)

# Tarihteki b isaretini gecici olarak kaldir
temiz_tarih = almanya["Time stamp"].str.replace(
    r"\s+b$", "", regex=True
)

# Tarih tipine donustur
almanya["tarih_duzeltilmis"] = pd.to_datetime(
    temiz_tarih,
    format="%d.%m.%Y %H:%M:%S",
    errors="coerce"
)

print("\n--- TARIH DUZELTME KONTROLU ---")

print("b isaretli kayit sayisi:",
      almanya["tekrarlanan_saat"].sum())

print("Donusturulemeyen tarih:",
      almanya["tarih_duzeltilmis"].isna().sum())

print("Ayni yerel saate sahip ek kayit:",
      almanya["tarih_duzeltilmis"].duplicated().sum())

# Mart ayindaki saat degisimini kontrol et
print("\n--- 26 MART 2017 KONTROLU ---")

mart = almanya[
    almanya["Time stamp"].str.startswith("26.03.2017")
]

mart_saatleri = mart[
    mart["Time stamp"].str.contains(
        r" 0[123]:", regex=True
    )
]

print(mart_saatleri["Time stamp"].to_string(index=False))

