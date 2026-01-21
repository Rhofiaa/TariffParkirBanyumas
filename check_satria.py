import pandas as pd
import numpy as np

# Load data
df = pd.read_excel('DataParkir_Fix.xlsx')

# Cari Toko Satria
toko = df[df['Titik'].str.contains('Satria', case=False, na=False)]

print("\n=== DATA TOKO SATRIA ===")
print(toko[['Titik']].to_string())

# Ambil kolom pendapatan motor
pend_weekday = 'Pendapatan Tarif Parkir Weekday Motor per tahun'
pend_weekend = 'Pendapatan Tarif Parkir Weekend Motor per tahun'

print(f"\nPendapatan Weekday Motor: {toko[pend_weekday].values[0]}")
print(f"Pendapatan Weekend Motor: {toko[pend_weekend].values[0]}")

# Convert ke numeric
wd = pd.to_numeric(toko[pend_weekday], errors='coerce').fillna(0).values[0]
we = pd.to_numeric(toko[pend_weekend], errors='coerce').fillna(0).values[0]

total = wd + we
print(f"\nTotal Pendapatan Motor (setelah konversi): Rp{total:,.0f}")
print(f"Weekday: Rp{wd:,.0f}")
print(f"Weekend: Rp{we:,.0f}")

# Hitung threshold dari semua data
pend_cols = [pend_weekday, pend_weekend]
df[pend_cols] = df[pend_cols].apply(lambda x: pd.to_numeric(x, errors='coerce').fillna(0))
df['Total_Pend_Motor'] = df[pend_weekday] + df[pend_weekend]

print(f"\n=== THRESHOLD KUANTIL (dari SEMUA data) ===")
try:
    labels_all = pd.qcut(df['Total_Pend_Motor'], q=3, labels=['Rendah','Sedang','Tinggi'], duplicates='drop')
    quantiles_all = df['Total_Pend_Motor'].quantile([0.333, 0.666]).values
    print(f"Threshold 33.3%: Rp{quantiles_all[0]:,.0f}")
    print(f"Threshold 66.6%: Rp{quantiles_all[1]:,.0f}")
    
    # Klasifikasi Toko Satria
    if total <= quantiles_all[0]:
        kelas = 'Rendah'
    elif total <= quantiles_all[1]:
        kelas = 'Sedang'
    else:
        kelas = 'Tinggi'
    
    print(f"\nKlasifikasi Toko Satria (Rp{total:,.0f}): {kelas}")
except Exception as e:
    print(f"Error: {e}")

# Lihat fitur-fitur lain Toko Satria
print(f"\n=== FITUR TOKO SATRIA ===")
print(f"Jumlah Motor Weekday: {toko['Jumlah Motor Weekday'].values[0]}")
print(f"Jumlah Motor Weekend: {toko['Jumlah Motor Weekend'].values[0]}")

# Cek kolom jam
jam_cols = [c for c in df.columns if 'Jam' in c and 'Motor' in c]
print(f"\nKolom Jam Motor:")
for col in jam_cols[:5]:  # Print 5 pertama saja
    val = toko[col].values[0] if col in toko.columns else 'N/A'
    print(f"  {col}: {val}")
