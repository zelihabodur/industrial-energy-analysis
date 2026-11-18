
import pandas as pd

# 1. Temiz verileri oku
kore = pd.read_csv("outputs/kore_temiz.csv")

almanya = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 2. Enerji tuketimi serileri
veriler = {
    "Guney Kore": kore["enerji_kWh"],
    "Almanya LG30": almanya["enerji_kWh"]
}

# 3. Tuketim siniflari
sinirlar = [
    float("-inf"), 0.5, 1, 2, float("inf")
]

etiketler = [
    "Cok dusuk",
    "Dusuk-orta",
    "Yuksek",
    "Cok yuksek"
]

sonuclar = {}

# 4. Her isletme icin frekans hesapla
for isletme, enerji in veriler.items():

    ortalama = enerji.mean()

    # Tuketimi kendi ortalamasina bol
    goreli_tuketim = enerji / ortalama

    # Degerleri siniflara ayir
    kategoriler = pd.cut(
        goreli_tuketim,
        bins=sinirlar,
        labels=etiketler
    )

    # Her sinifta kac kayit var?
    frekans = kategoriler.value_counts(
        sort=False
    )

    # Yuzde olarak hesapla
    yuzde = frekans / len(enerji) * 100

    sonuclar[isletme + " Adet"] = frekans
    sonuclar[isletme + " Yuzde"] = yuzde

# 5. Karsilastirma tablosu
tablo = pd.DataFrame(sonuclar)

print("\n--- FREKANS ANALIZI ---")
print(tablo.round(2).to_string())

# 6. Kaydet
tablo.to_csv(
    "outputs/frekans_analizi.csv",
    encoding="utf-8-sig",
    index_label="Tuketim Sinifi"
)

print("\nFrekans tablosu kaydedildi.")
