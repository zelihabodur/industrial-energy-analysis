
import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# 1. TEMIZ VERILERI OKU

kore = pd.read_csv("outputs/kore_temiz.csv")

almanya = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 2. TAHMIN HATASI HESAPLA

def metrikler(gercek, tahmin):

    mae = mean_absolute_error(gercek, tahmin)

    rmse = np.sqrt(
        mean_squared_error(gercek, tahmin)
    )

    r2 = r2_score(gercek, tahmin)

    return mae, rmse, r2


# 3. MODELLEME FONKSIYONU

def model_olustur(df, tarih_sutunu, isletme):

    enerji = df["enerji_kWh"]

    tarih = pd.to_datetime(df[tarih_sutunu])

    # Zaman ozellikleri
    saat = tarih.dt.hour + tarih.dt.minute / 60

    # Gecmis enerji degerleri ve takvim bilgileri
    tablo = pd.DataFrame({
        "tarih": tarih,
        "gercek": enerji,
        "son_olcum": enerji.shift(1),
        "lag_2": enerji.shift(2),
        "lag_4": enerji.shift(4),
        "onceki_96": enerji.shift(96),
        "saat_sin": np.sin(2 * np.pi * saat / 24),
        "saat_cos": np.cos(2 * np.pi * saat / 24),
        "hafta_sonu": (
            tarih.dt.dayofweek >= 5
        ).astype(int)
    })

    # Ilk 96 kayitta yeterli gecmis bilgi yok
    tablo = tablo.dropna().reset_index(drop=True)

    # Modelde kullanilacak degiskenler
    ozellikler = [
        "son_olcum",
        "lag_2",
        "lag_4",
        "onceki_96",
        "saat_sin",
        "saat_cos",
        "hafta_sonu"
    ]

    X = tablo[ozellikler]
    y = tablo["gercek"]

    # Ilk %80 egitim, son %20 test
    bolum = int(len(tablo) * 0.80)

    X_train = X.iloc[:bolum]
    X_test = X.iloc[bolum:]

    y_train = y.iloc[:bolum]
    y_test = y.iloc[bolum:]

    print("\nISLETME:", isletme)
    print("Egitim kaydi:", len(X_train))
    print("Test kaydi:", len(X_test))

    # 4. MODELLERI TANIMLA

    modeller = {
        "Linear Regression": LinearRegression(),

        "Random Forest": RandomForestRegressor(
            n_estimators=120,
            max_depth=14,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        )
    }

    # Basit yontemleri de ayni testte degerlendir
    tahminler = {
        "Son olcum": X_test["son_olcum"].to_numpy(),
        "96 kayit once": X_test["onceki_96"].to_numpy()
    }

    # 5. MODELLERI EGIT VE TAHMIN YAP

    for isim, model in modeller.items():

        model.fit(X_train, y_train)

        tahminler[isim] = model.predict(X_test)

    # 6. HATALARI HESAPLA

    sonuclar = []

    for isim, tahmin in tahminler.items():

        mae, rmse, r2 = metrikler(
            y_test, tahmin
        )

        sonuclar.append({
            "Isletme": isletme,
            "Model": isim,
            "MAE_kWh": mae,
            "RMSE_kWh": rmse,
            "R2": r2
        })

    # 7. TEST TAHMINLERINI KAYDET

    detay = pd.DataFrame({
        "tarih": tablo["tarih"].iloc[bolum:].to_numpy(),
        "gercek_kWh": y_test.to_numpy(),
        "son_olcum_kWh": tahminler["Son olcum"],
        "linear_kWh": tahminler["Linear Regression"],
        "forest_kWh": tahminler["Random Forest"]
    })

    dosya_adi = (
        "kore" if isletme == "Guney Kore"
        else "almanya"
    )

    detay.to_csv(
        f"outputs/tahmin_detay_{dosya_adi}.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return sonuclar


# 8. IKI ISLETMEDE MODELLERI CALISTIR

Path("outputs").mkdir(exist_ok=True)

sonuclar = []

sonuclar.extend(
    model_olustur(kore, "tarih", "Guney Kore")
)

sonuclar.extend(
    model_olustur(
        almanya, "tarih_yerel", "Almanya LG30"
    )
)

# 9. SONUCLARI GOSTER

sonuc_tablo = pd.DataFrame(sonuclar)

print("\n--- REGRESYON MODEL SONUCLARI ---")

print(
    sonuc_tablo.round(3).to_string(index=False)
)

sonuc_tablo.to_csv(
    "outputs/regresyon_model_sonuclari.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nModel karsilastirmasi tamamlandi!")
