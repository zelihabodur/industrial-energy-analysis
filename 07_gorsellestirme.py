
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Frekans tablomuzu oku
tablo = pd.read_csv(
    "outputs/frekans_analizi.csv"
)

# 2. Grafik verilerini sec
siniflar = tablo["Tuketim Sinifi"]

kore = tablo["Guney Kore Yuzde"]
almanya = tablo["Almanya LG30 Yuzde"]

# 3. Grafik konumlarini belirle
x = np.arange(len(siniflar))
genislik = 0.36

# 4. Grafik alanini olustur
fig, ax = plt.subplots(figsize=(10, 6))

# 5. Sutunlari ciz
sutun_kore = ax.bar(
    x - genislik / 2,
    kore,
    genislik,
    label="Guney Kore"
)

sutun_almanya = ax.bar(
    x + genislik / 2,
    almanya,
    genislik,
    label="Almanya LG30"
)

# 6. Sutunlarin ustune yuzdeleri yaz
ax.bar_label(
    sutun_kore,
    fmt="%.1f%%",
    padding=3
)

ax.bar_label(
    sutun_almanya,
    fmt="%.1f%%",
    padding=3
)

# 7. Baslik ve eksen bilgileri
ax.set_title(
    "Goreli Enerji Tuketimi Karsilastirmasi",
    fontsize=15
)

ax.set_xlabel("Tuketim Sinifi")
ax.set_ylabel("Kayit Orani (%)")

ax.set_xticks(x)
ax.set_xticklabels(siniflar)

ax.set_ylim(0, 70)

# 8. Aciklama ve izgara
ax.legend()
ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)

# 9. Grafigi dosyaya kaydet
Path("outputs/grafikler").mkdir(
    parents=True,
    exist_ok=True
)

plt.tight_layout()

plt.savefig(
    "outputs/grafikler/01_frekans_karsilastirma.png",
    dpi=300,
    bbox_inches="tight"
)

# 10. Grafigi ekranda goster
plt.show()

print("\nGrafik basariyla kaydedildi!")

