"""
Script untuk generate Jupyter Notebook Analisis Tarif Parkir secara lengkap
"""

import json

# Struktur notebook
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

# Helper untuk tambah cell
def add_markdown_cell(content):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": content.split('\n'),
        "execution_count": None,
        "outputs": []
    })

def add_code_cell(content):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": content.split('\n')
    })

# ============ SECTION 1: TITLE & INTRO ============
add_markdown_cell("""# 🅿️ Analisis Potensi Tarif Parkir Banyumas

## Klasifikasi Random Forest dengan Tarif Adaptif dan Simulasi Interaktif

**Tujuan**: Menganalisis potensi tarif parkir di berbagai lokasi di Banyumas menggunakan klasifikasi berbasis machine learning dengan implementasi tarif progresif.

**Tahapan Analisis**:
1. ✅ Import Library & Konfigurasi
2. ✅ Definisikan Fungsi Utility
3. ✅ Load & Eksplorasi Data Mentah
4. ✅ Cleaning & Preprocessing
5. ✅ EDA (Exploratory Data Analysis)
6. ✅ Feature Engineering & Target Classification
7. ✅ Train-Test Split & Training Model
8. ✅ Evaluasi Model & Metrics
9. ✅ Feature Importance & Interpretasi
10. ✅ Visualisasi Decision Tree
11. ✅ Spatial Analysis & Mapping
12. ✅ Progressive Tariff Calculation
13. ✅ Interactive Prediction & What-If Analysis
14. ✅ Comprehensive Visualization Dashboard""")

# ============ SECTION 2: IMPORTS ============
add_markdown_cell("## 1️⃣ IMPORT REQUIRED LIBRARIES & CONFIGURATION")

add_code_cell("""# Import semua library yang diperlukan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import Search, Fullscreen, MiniMap
import re
import datetime
import warnings
from datetime import datetime as dt

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    roc_auc_score, roc_curve, auc
)
from sklearn.tree import plot_tree

# Plotting Style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
warnings.filterwarnings('ignore')

# Display Options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', None)

print("✅ Semua library berhasil diimport!")
print(f"📊 NumPy version: {np.__version__}")
print(f"📊 Pandas version: {pd.__version__}")""")

# ============ SECTION 3: UTILITY FUNCTIONS ============
add_markdown_cell("## 2️⃣ DEFINE UTILITY FUNCTIONS FOR DATA PROCESSING")

add_code_cell("""# ========== FUNGSI UTILITY UNTUK KONVERSI WAKTU ==========

def parse_time_to_decimal(time_str):
    \"\"\"Mengkonversi string waktu (H.M, H:M, atau H) menjadi jam desimal.\"\"\"
    try:
        time_str = str(time_str).replace(',', '.').replace(':', '.')
        if '.' in time_str:
            h_str, m_part_str = time_str.split('.', 1)
            h = int(h_str) if h_str else 0
            m = int(m_part_str.ljust(2, '0')[:2])
            return h + m / 60.0
        else:
            return float(time_str)
    except Exception:
        return np.nan

def konversi_jam(x):
    \"\"\"Mengubah format jam range (contoh: '20.00-22.00') menjadi jam desimal rata-rata.\"\"\"
    if pd.isna(x) or str(x).strip() in ('-', '', 'nan'):
        return np.nan
    s = str(x).strip()
    try:
        parts = re.split(r'\\s*-\\s*', s)
        start_time_dec = parse_time_to_decimal(parts[0].strip())
        end_time_dec = parse_time_to_decimal(parts[1].strip()) if len(parts) > 1 else start_time_dec
        
        if len(parts) > 1 and pd.notna(start_time_dec) and pd.notna(end_time_dec) and end_time_dec < start_time_dec:
            end_time_dec += 24.0
        
        if pd.isna(start_time_dec) or pd.isna(end_time_dec):
            return np.nan
        
        return (start_time_dec + end_time_dec) / 2
    except Exception:
        return np.nan

def time_to_decimal_hour(time_obj):
    \"\"\"Mengkonversi objek datetime.time menjadi jam desimal.\"\"\"
    if time_obj is None:
        return np.nan
    return time_obj.hour + time_obj.minute / 60.0

def kategori_jam_otomatis(jam):
    \"\"\"Mengkategorikan jam (0-24) ke dalam kategori kepadatan.\"\"\"
    if (jam <= 6) or (jam >= 22):
        return 'Sepi'
    elif (jam > 8 and jam <= 19):
        return 'Ramai'
    else:
        return 'Sedang'

# ========== MAPPING TARIF DASAR ==========

tarif_mapping = {
    'Motor': {'Rendah': 1000, 'Sedang': 2000, 'Tinggi': 3000},
    'Mobil': {'Rendah': 3000, 'Sedang': 4000, 'Tinggi': 5000}
}

print("✅ Fungsi utility berhasil didefinisikan!")
print("\\nTarif Dasar yang Digunakan:")
for jenis, tarifs in tarif_mapping.items():
    print(f"\\n{jenis}:")
    for kategori, harga in tarifs.items():
        print(f"  - {kategori}: Rp{harga:,}")""")

add_code_cell("""# ========== FUNGSI TARIF PROGRESIF ==========

def calculate_progresif_tarif(jenis, potensi_class, jam_desimal):
    \"\"\"Menerapkan logika tarif progresif berdasarkan potensi dan waktu.\"\"\"
    tarif_dasar = tarif_mapping[jenis].get(potensi_class, 0)
    
    if jam_desimal > 9.0:
        if potensi_class == 'Tinggi':
            return tarif_dasar + 1000
        elif potensi_class == 'Sedang':
            return tarif_dasar + 500
        else:
            return tarif_dasar
    else:
        return tarif_dasar

print("✅ Fungsi progresif tarif berhasil didefinisikan!")""")

# ============ SECTION 4: LOAD DATA ============
add_markdown_cell("## 3️⃣ LOAD & EXPLORE RAW DATA")

add_code_cell("""# Konfigurasi path file
FILE_PATH = 'DataParkir_Fix.xlsx'

# Load data dari Excel
print(f"📂 Membaca file: {FILE_PATH}...")
try:
    df_raw = pd.read_excel(FILE_PATH)
    print(f"✅ Data berhasil dimuat!")
except FileNotFoundError:
    print(f"❌ File '{FILE_PATH}' tidak ditemukan.")
    raise

print(f"\\n📊 INFORMASI DATA MENTAH:")
print(f"  - Shape: {df_raw.shape} (baris, kolom)")
print(f"  - Jumlah Kolom: {len(df_raw.columns)}")

print(f"\\n📋 Data Types:")
print(df_raw.dtypes)

print(f"\\n👁️  Preview Data (5 baris pertama):")
print(df_raw.head())

print(f"\\n❓ Missing Values:")
print(df_raw.isnull().sum()[df_raw.isnull().sum() > 0])

# Statistik deskriptif
print(f"\\n📈 Statistik Deskriptif:")
print(df_raw.describe())""")

# ============ SECTION 5: DATA CLEANING ============
add_markdown_cell("## 4️⃣ DATA CLEANING & PREPROCESSING")

add_code_cell("""print("🔧 TAHAP 1: CONVERT REVENUE COLUMNS")
print("="*60)

df = df_raw.copy()

# Kolom pendapatan yang perlu dibersihkan
pend_cols = [
    'Pendapatan Tarif Parkir Weekday Motor per tahun', 
    'Pendapatan Tarif Parkir Weekday Mobil per tahun',
    'Pendapatan Tarif Parkir Weekend Motor per tahun', 
    'Pendapatan Tarif Parkir Weekend Mobil per tahun'
]

# Identifikasi kolom Jumlah dan Jam
jumlah_cols = [c for c in df.columns if c.startswith('Jumlah')]
jam_cols = [c for c in df.columns if 'Jam' in c and 'per tahun' not in c]

print(f"✅ Kolom Pendapatan yang diproses: {len(pend_cols)}")
print(f"✅ Kolom Jumlah yang ditemukan: {jumlah_cols}")
print(f"✅ Kolom Jam yang ditemukan: {jam_cols}")

# Membersihkan kolom pendapatan (hapus Rp, ., ubah , jadi .)
for c in pend_cols:
    if c in df.columns:
        df[c] = df[c].astype(str).str.replace(r'[^\\d,\\.]', '', regex=True)
        df[c] = df[c].str.replace('.', '', regex=False)
        df[c] = df[c].str.replace(',', '.', regex=False)
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

print("\\n✅ Kolom pendapatan berhasil dikonversi ke numerik!")
print(df[pend_cols].head())""")

add_code_cell("""print("\\n🔧 TAHAP 2: CONVERT & IMPUTE TIME COLUMNS")
print("="*60)

# Konversi kolom Jam
for col in jam_cols:
    print(f"Processing: {col}")
    df[col] = df[col].apply(konversi_jam)
    missing_count = df[col].isnull().sum()
    if missing_count > 0:
        df[col] = df[col].fillna(df[col].mean())
        print(f"  ✅ {missing_count} nilai NaN diisi dengan mean")

print("\\n✅ Kolom Jam berhasil dikonversi!")
print(df[jam_cols[:3]].head())""")

add_code_cell("""print("\\n🔧 TAHAP 3: IMPUTE NUMERIC & CATEGORICAL COLUMNS")
print("="*60)

# Impute kolom numerik dengan median
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    missing_count = df[col].isnull().sum()
    if missing_count > 0:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"✅ {col}: {missing_count} NaN diisi dengan median ({median_val:.2f})")

# Impute kolom kategorikal dengan mode
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if col not in ['Titik', 'Class_Motor', 'Class_Mobil']:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            mode_val = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
            df[col] = df[col].fillna(mode_val)
            print(f"✅ {col}: {missing_count} NaN diisi dengan mode ({mode_val})")

print("\\n✅ Imputation selesai!")
print(f"\\nTotal missing values: {df.isnull().sum().sum()}")""")

add_code_cell("""print("\\n🔧 TAHAP 4: HANDLE SPATIAL DATA")
print("="*60)

# Buat dataframe spasial
if all(c in df.columns for c in ['Latitude', 'Longitude', 'Titik']):
    df_spasial = df[['Latitude', 'Longitude', 'Titik'] + jam_cols + jumlah_cols].copy()
    
    # Bersihkan Titik
    df_spasial['Titik'] = df_spasial['Titik'].astype(str).str.strip()
    df_spasial = df_spasial.replace({'Titik': {'nan': None}})
    df_spasial = df_spasial.dropna(subset=['Titik', 'Latitude', 'Longitude'])
    df_spasial = df_spasial.reset_index(drop=True)
    
    print(f"✅ Data spasial berhasil diproses!")
    print(f"   - Jumlah lokasi dengan koordinat: {len(df_spasial)}")
    print(f"   - Koordinat range:")
    print(f"     Latitude: {df_spasial['Latitude'].min():.4f} - {df_spasial['Latitude'].max():.4f}")
    print(f"     Longitude: {df_spasial['Longitude'].min():.4f} - {df_spasial['Longitude'].max():.4f}")
    
    # Filter df utama juga
    df['Titik'] = df['Titik'].astype(str).str.strip()
    df = df.replace({'Titik': {'nan': None}})
    df = df.dropna(subset=['Titik']).reset_index(drop=True)
    print(f"\\n✅ Data mentah setelah filter: {df.shape}")
else:
    print("❌ Kolom spasial (Titik, Latitude, Longitude) tidak ditemukan!")""")

# ============ SECTION 6: FEATURE ENGINEERING ============
add_markdown_cell("## 5️⃣ FEATURE ENGINEERING & TARGET CLASSIFICATION")

add_code_cell("""print("🔧 TAHAP 1: CALCULATE TOTAL REVENUE")
print("="*60)

# Identifikasi kolom pendapatan untuk motor dan mobil
motor_pend_cols = [c for c in pend_cols if 'Motor' in c]
mobil_pend_cols = [c for c in pend_cols if 'Mobil' in c]

df['Total_Pend_Motor'] = df[motor_pend_cols].sum(axis=1)
df['Total_Pend_Mobil'] = df[mobil_pend_cols].sum(axis=1)

print(f"✅ Total Pendapatan Motor:")
print(df['Total_Pend_Motor'].describe())

print(f"\\n✅ Total Pendapatan Mobil:")
print(df['Total_Pend_Mobil'].describe())""")

add_code_cell("""print("\\n🔧 TAHAP 2: CREATE TARGET CLASSES (CLASSIFICATION)")
print("="*60)

# Klasifikasi Motor
try:
    df['Class_Motor'] = pd.qcut(df['Total_Pend_Motor'], q=3, 
                                 labels=['Rendah','Sedang','Tinggi'], 
                                 duplicates='drop')
    batas_motor = df['Total_Pend_Motor'].quantile([0.333, 0.666]).drop_duplicates().sort_values()
    print(f"✅ Motor berhasil diklasifikasi dengan 3 kelas")
except ValueError:
    df['Class_Motor'] = pd.cut(df['Total_Pend_Motor'], 
                                bins=[-np.inf, df['Total_Pend_Motor'].median(), np.inf], 
                                labels=['Rendah', 'Tinggi']).fillna('Rendah')
    batas_motor = df['Total_Pend_Motor'].quantile([0.5])
    print(f"⚠️  Motor diklasifikasi dengan 2 kelas (data terbatas)")

print(f"Distribusi Class_Motor:")
print(df['Class_Motor'].value_counts())

# Klasifikasi Mobil
try:
    df['Class_Mobil'] = pd.qcut(df['Total_Pend_Mobil'], q=3, 
                                 labels=['Rendah','Sedang','Tinggi'], 
                                 duplicates='drop')
    batas_mobil = df['Total_Pend_Mobil'].quantile([0.333, 0.666]).drop_duplicates().sort_values()
    print(f"\\n✅ Mobil berhasil diklasifikasi dengan 3 kelas")
except ValueError:
    df['Class_Mobil'] = pd.cut(df['Total_Pend_Mobil'], 
                                bins=[-np.inf, df['Total_Pend_Mobil'].median(), np.inf], 
                                labels=['Rendah', 'Tinggi']).fillna('Rendah')
    batas_mobil = df['Total_Pend_Mobil'].quantile([0.5])
    print(f"\\n⚠️  Mobil diklasifikasi dengan 2 kelas (data terbatas)")

print(f"Distribusi Class_Mobil:")
print(df['Class_Mobil'].value_counts())

print(f"\\n✅ Data Preprocessing Selesai!")
print(f"\\nData Shape: {df.shape}")
print(f"\\nPreview Data Terproses:")
print(df[['Titik', 'Total_Pend_Motor', 'Class_Motor', 'Total_Pend_Mobil', 'Class_Mobil']].head(10))""")

# ============ SECTION 7: EDA ============
add_markdown_cell("## 6️⃣ EXPLORATORY DATA ANALYSIS (EDA)")

add_code_cell("""print("📊 VISUALISASI DISTRIBUSI PENDAPATAN")
print("="*60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Motor Revenue Distribution
axes[0, 0].hist(df['Total_Pend_Motor'], bins=20, color='#2E86AB', alpha=0.7, edgecolor='black')
axes[0, 0].set_title('Distribusi Total Pendapatan Motor', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Pendapatan (Rp)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].grid(axis='y', alpha=0.3)

# Motor by Class
df['Class_Motor'].value_counts().plot(kind='bar', ax=axes[0, 1], color=['#FF6B6B', '#4ECDC4', '#FFC93C'])
axes[0, 1].set_title('Distribusi Kelas Motor', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Kelas Potensi')
axes[0, 1].set_ylabel('Jumlah Lokasi')
axes[0, 1].tick_params(axis='x', rotation=0)
axes[0, 1].grid(axis='y', alpha=0.3)

# Mobil Revenue Distribution
axes[1, 0].hist(df['Total_Pend_Mobil'], bins=20, color='#A23B72', alpha=0.7, edgecolor='black')
axes[1, 0].set_title('Distribusi Total Pendapatan Mobil', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Pendapatan (Rp)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].grid(axis='y', alpha=0.3)

# Mobil by Class
df['Class_Mobil'].value_counts().plot(kind='bar', ax=axes[1, 1], color=['#FF6B6B', '#4ECDC4', '#FFC93C'])
axes[1, 1].set_title('Distribusi Kelas Mobil', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Kelas Potensi')
axes[1, 1].set_ylabel('Jumlah Lokasi')
axes[1, 1].tick_params(axis='x', rotation=0)
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

print("\\n✅ Visualisasi distribusi selesai!")"
