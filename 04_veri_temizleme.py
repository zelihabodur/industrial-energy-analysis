
import pandas as pd
from pathlib import Path

# 1. VERI SETLERINI OKU

kore = pd.read_csv(
    "data/Steel_industry_data.csv"
)

almanya = pd.read_csv(
    "data/LoadProfile_30IPs_2017.csv",
    sep=";",
    header=1
)

# 2. GUNEY KORE TARIHLERINI DUZELT

kore["tarih"] = pd.to_datetime(
    kore["date"],
    format="%d/%m/%Y %H:%M",
    errors="raise"
)

onceki = kore["tarih"].shift(1)

# 00:00 kaydi, ayni gunun 23:45
# kaydindan hemen sonra mi geliyor?
gece_sonu = (
    kore["tarih"].dt.strftime("%H:%M").eq("00:00")
    & onceki.dt.strftime("%H:%M").eq("23:45")
    & kore["tarih"].dt.normalize().eq(
        onceki.dt.normalize()
    )
)

geriye_giden = (
    kore["tarih"].diff() < pd.Timedelta(0)
)

print("Kore gece sonu kaydi:", gece_sonu.sum())

# Bekledigimiz duzen dogrulanmazsa dur
if not geriye_giden.equals(gece_sonu):
    raise ValueError(
        "Kore tarih sirasi beklenenden farkli!"
    )

# Gece sonu kayitlarini ertesi gune tasi
kore.loc[gece_sonu, "tarih"] += pd.Timedelta(days=1)

# Tum kayitlar 15 dakika aralikli mi?
zaman_farklari = kore["tarih"].diff().iloc[1:]

if not zaman_farklari.eq(
    pd.Timedelta(minutes=15)
).all():
    raise ValueError("Kore zaman araliklari duzensiz!")

kore_temiz = kore[
    ["date", "tarih", "Usage_kWh"]
].copy()

kore_temiz = kore_temiz.rename(columns={
    "date": "tarih_orijinal",
    "Usage_kWh": "enerji_kWh"
})

# 3. ALMANYA BOS SATIRLARINI AYIR

lg_sutunlari = [
    s for s in almanya.columns
    if s.startswith("LG ")
]

tamamen_bos = (
    almanya[lg_sutunlari].isna().all(axis=1)
)

almanya_temiz = almanya.loc[
    ~tamamen_bos,
    ["Time stamp", "LG 30"]
].copy()

# Secilen tesiste hala eksik kayit var mi?
if almanya_temiz["LG 30"].isna().any():
    raise ValueError("LG 30 eksik kayit iceriyor!")

# 4. ALMANYA TARIHLERINI HAZIRLA

almanya_temiz["tekrarlanan_saat"] = (
    almanya_temiz["Time stamp"].str.endswith(" b")
)

tarih_metni = (
    almanya_temiz["Time stamp"]
    .str.replace(r"\s+b$", "", regex=True)
)

almanya_temiz["tarih_yerel"] = pd.to_datetime(
    tarih_metni,
    format="%d.%m.%Y %H:%M:%S",
    errors="raise"
)

# Orijinal kayit sirasini koru
almanya_temiz["kayit_sirasi"] = range(
    1, len(almanya_temiz) + 1
)

almanya_temiz = almanya_temiz.rename(columns={
    "Time stamp": "tarih_orijinal",
    "LG 30": "ortalama_guc_kW"
})

# 15 dakikalik ortalama gucu enerjiye cevir
almanya_temiz["enerji_kWh"] = (
    almanya_temiz["ortalama_guc_kW"] * 0.25
)

# 5. SONUCLARI KAYDET

Path("outputs").mkdir(exist_ok=True)

kore_temiz.to_csv(
    "outputs/kore_temiz.csv",
    index=False,
    encoding="utf-8-sig"
)

almanya_temiz.to_csv(
    "outputs/almanya_LG30_temiz.csv",
    index=False,
    encoding="utf-8-sig"
)

# 6. SON KONTROLLER

print("\n--- KORE SONUCLARI ---")
print("Kayit sayisi:", len(kore_temiz))
print("Ilk tarih:", kore_temiz["tarih"].min())
print("Son tarih:", kore_temiz["tarih"].max())
print("Eksik enerji:", kore_temiz["enerji_kWh"].isna().sum())

print("\n--- ALMANYA SONUCLARI ---")
print("Kayit sayisi:", len(almanya_temiz))
print("Cikarilan bos satir:", tamamen_bos.sum())
print("Ozel b kaydi:",
      almanya_temiz["tekrarlanan_saat"].sum())
print("Eksik enerji:",
      almanya_temiz["enerji_kWh"].isna().sum())

print("\nIKI TEMIZ DOSYA OLUSTURULDU!")
