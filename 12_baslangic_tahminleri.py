
import pandas as pd
import numpy as np
from pathlib import Path

# 1. TEMIZ VERILERI OKU

kore = pd.read_csv(
    "outputs/kore_temiz.csv"
)

almanya = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 2. TAHMIN HATALARINI HESAPLAYAN FONKSIYON

def hata_hesapla(gercek, tahmin):

    mae = np.mean(np.abs(gercek - tahmin))

    rmse = np.sqrt(
        np.mean((gercek - tahmin) ** 2)
    )

    return mae, rmse


# 3. IKI TAHMIN YONTEMINI KARSILASTIR

def tahmin_analizi(df, isletme):

    enerji = df["enerji_kWh"]

    tablo = pd.DataFrame({
        "gercek": enerji,
        "son_olcum": enerji.shift(1),
        "onceki_96_kayit": enerji.shift(96)
    })

    # Ilk 96 kayitta yeterli gecmis veri yok
    tablo = tablo.dropna()

    # Verinin ilk %80'i egitim donemi,
    # son %20'si test donemi
    bolum = int(len(tablo) * 0.80)

    test = tablo.iloc[bolum:].copy()

    print("\nISLETME:", isletme)
    print("Egitim donemi kayit:", bolum)
    print("Test donemi kayit:", len(test))

    sonuc_listesi = []

    for isim, sutun in [
        ("Son olcum", "son_olcum"),
        ("96 kayit once", "onceki_96_kayit")
    ]:

        mae, rmse = hata_hesapla(
            test["gercek"],
            test[sutun]
        )

        sonuc_listesi.append({
            "Isletme": isletme,
            "Yontem": isim,
            "MAE_kWh": mae,
            "RMSE_kWh": rmse
        })

    return sonuc_listesi


# 4. IKI ISLETMEYE AYNI YONTEMI UYGULA

sonuclar = []

sonuclar.extend(
    tahmin_analizi(kore, "Guney Kore")
)

sonuclar.extend(
    tahmin_analizi(almanya, "Almanya LG30")
)

# 5. SONUC TABLOSU

sonuc_tablo = pd.DataFrame(sonuclar)

print("\n--- BASLANGIC TAHMIN SONUCLARI ---")

print(
    sonuc_tablo.round(3).to_string(index=False)
)

# 6. DOSYAYA KAYDET

Path("outputs").mkdir(exist_ok=True)

sonuc_tablo.to_csv(
    "outputs/baslangic_tahmin_sonuclari.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nTahmin sonuclari kaydedildi!")
