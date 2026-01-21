import pandas as pd
import numpy as np
from datetime import time, datetime, timedelta

# Fungsi kategori jam (copy dari streamlit)
def time_to_decimal_hour(t):
    return t.hour + t.minute / 60

def kategori_jam_otomatis(jam_desimal):
    if 6 <= jam_desimal < 9:
        return 'Sepi'
    elif 9 <= jam_desimal < 15:
        return 'Sedang'
    elif 15 <= jam_desimal < 19:
        return 'Ramai'
    else:
        return 'Sepi'

# Load data untuk lihat struktur fitur
df = pd.read_excel('DataParkir_Fix.xlsx')
jam_cols = [c for c in df.columns if 'Jam' in c and 'Motor' in c]

print("=== KOLOM FITUR JAM MOTOR ===")
for col in jam_cols:
    print(f"  {col}")

print("\n=== CONTOH NILAI ===")
print(df[jam_cols].iloc[0])

print("\n=== SIMULASI FITUR UNTUK JAM 8 ===")
jam_8 = 8.0
kategori_8 = kategori_jam_otomatis(jam_8)
print(f"Jam 8.0 → Kategori: {kategori_8}")

# Simulasi konstruksi fitur untuk jam 8
print(f"\nFitur yang akan diisi:")
for col in jam_cols:
    if kategori_8 in col:
        print(f"  {col} = 8.0")
    else:
        print(f"  {col} = (mean/default dari data)")

print("\n=== SIMULASI FITUR UNTUK JAM 9 ===")
jam_9 = 9.0
kategori_9 = kategori_jam_otomatis(jam_9)
print(f"Jam 9.0 → Kategori: {kategori_9}")

print(f"\nFitur yang akan diisi:")
for col in jam_cols:
    if kategori_9 in col:
        print(f"  {col} = 9.0")
    else:
        print(f"  {col} = (mean/default dari data)")

print("\n=== PERBEDAAN ===")
print(f"Jam 8 masuk kategori: {kategori_8}")
print(f"Jam 9 masuk kategori: {kategori_9}")

if kategori_8 != kategori_9:
    print(f"\n⚠️ JAM 8 DAN 9 MASUK KATEGORI BERBEDA!")
    print(f"Ini menyebabkan fitur jam yang berbeda → prediksi bisa berbeda!")
else:
    print(f"\n✓ Jam 8 dan 9 masuk kategori SAMA")
