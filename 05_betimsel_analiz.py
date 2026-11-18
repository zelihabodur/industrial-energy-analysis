
import pandas as pd

# 1. Temiz veri setlerini oku
kore = pd.read_csv("outputs/kore_temiz.csv")

almanya = pd.read_csv(
    "outputs/almanya_LG30_temiz.csv"
)

# 2. Enerji tuketim sutunlarini sec
kore_enerji = kore["enerji_kWh"]
almanya_enerji = almanya["enerji_kWh"]

# 3. Istatistikleri hesaplayan fonksiyon
def istatistik_hesapla(veri, isletme):

    return {
        "Isletme": isletme,
        "Kayit sayisi": veri.count(),
        "Ortalama": veri.mean(),
        "Medyan": veri.median(),
        "Mod": veri.mode().iloc[0],
        "Varyans": veri.var(),
        "Standart sapma": veri.std(),
        "Minimum": veri.min(),
        "Maksimum": veri.max(),
        "Degisim katsayisi": (
            veri.std() / veri.mean()
        )
    }

# 4. Iki isletmenin istatistiklerini hesapla
sonuclar = pd.DataFrame([
    istatistik_hesapla(kore_enerji, "Guney Kore"),
    istatistik_hesapla(almanya_enerji, "Almanya LG30")
])

# 5. Sonuclari ekrana yazdir
print("\n--- BETIMSEL ISTATISTIKLER ---")

print(
    sonuclar.round(3).to_string(index=False)
)

# 6. Sonuclari kaydet
sonuclar.to_csv(
    "outputs/betimsel_istatistikler.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nIstatistik tablosu kaydedildi.")
