
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Tahmin sonuclarini oku
kore = pd.read_csv(
    "outputs/tahmin_detay_kore.csv"
)

almanya = pd.read_csv(
    "outputs/tahmin_detay_almanya.csv"
)

# 2. Grafik klasorunu hazirla
Path("outputs/grafikler").mkdir(
    parents=True,
    exist_ok=True
)

# 3. Grafik fonksiyonumuz
def grafik_olustur(veri, isletme, dosya_adi):

    # Test doneminin ilk 96 olcumu
    # Yaklasik 24 saatlik veri
    ornek = veri.head(96).copy()

    x = range(len(ornek))

    fig, ax = plt.subplots(figsize=(12, 6))

    # Gercek tuketim
    ax.plot(
        x,
        ornek["gercek_kWh"],
        label="Gercek tuketim",
        color="black",
        linewidth=2.3
    )

    # Basit tahmin
    ax.plot(
        x,
        ornek["son_olcum_kWh"],
        label="Son olcum tahmini",
        color="#F59E0B",
        linestyle="--",
        linewidth=1.5
    )

    # Random Forest
    ax.plot(
        x,
        ornek["forest_kWh"],
        label="Random Forest tahmini",
        color="#2563EB",
        linewidth=1.8,
        alpha=0.85
    )

    ax.set_title(
        f"{isletme} - Gercek ve Tahmin Edilen Tuketim",
        fontsize=14
    )

    ax.set_xlabel("Test Donemindeki Olcum Sirasi")
    ax.set_ylabel("15 Dakikalik Enerji (kWh)")

    ax.grid(alpha=0.2)
    ax.legend()

    plt.tight_layout()

    plt.savefig(
        f"outputs/grafikler/{dosya_adi}",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"{isletme} grafigi kaydedildi!")


# 4. Guney Kore grafigi
grafik_olustur(
    kore,
    "Guney Kore",
    "06_kore_tahmin_grafigi.png"
)

# 5. Almanya grafigi
grafik_olustur(
    almanya,
    "Almanya LG30",
    "07_almanya_tahmin_grafigi.png"
)

print("\nIki tahmin grafigi hazir!")
