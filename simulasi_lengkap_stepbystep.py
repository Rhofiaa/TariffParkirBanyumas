"""
SIMULASI LENGKAP STEP-BY-STEP TANPA STREAMLIT
Dari Import → Data Loading → Data Cleaning → Training → Prediksi

Jalankan dengan: python simulasi_lengkap_stepbystep.py
"""

import sys

# ============================================================================
# STEP 1: IMPORT LIBRARY
# ============================================================================
print("="*100)
print("[STEP 1] IMPORT LIBRARY")
print("="*100)

print("\nMengimport library yang diperlukan...")

import pandas as pd
print("✓ pandas - untuk manipulasi data")

import numpy as np
print("✓ numpy - untuk operasi numerik")

import re
print("✓ re - untuk regex/parsing teks")

from sklearn.model_selection import train_test_split
print("✓ sklearn.model_selection.train_test_split - untuk split data 80:20")

from sklearn.preprocessing import LabelEncoder
print("✓ sklearn.preprocessing.LabelEncoder - untuk encoding label")

from sklearn.ensemble import RandomForestClassifier
print("✓ sklearn.ensemble.RandomForestClassifier - algoritma Random Forest")

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
print("✓ sklearn.metrics - untuk evaluasi model")

from sklearn.tree import plot_tree, export_text
print("✓ sklearn.tree - untuk visualisasi & export decision tree")

import matplotlib.pyplot as plt
print("✓ matplotlib.pyplot - untuk membuat grafik")

import seaborn as sns
print("✓ seaborn - untuk visualisasi heatmap")

print("\n✓✓✓ SEMUA LIBRARY BERHASIL DIIMPORT ✓✓✓\n")

# ============================================================================
# STEP 2: DEFINISI FUNGSI
# ============================================================================
print("="*100)
print("[STEP 2] DEFINISI FUNGSI UTILITY")
print("="*100)

def parse_time_to_decimal(time_str):
    """
    FUNGSI 1: Konversi waktu string (HH:MM atau HH.MM) ke jam desimal
    
    PENJELASAN:
    - Input: "17:15" atau "17.15" (17 jam 15 menit)
    - Proses: 17 + (15 / 60)
    - Output: 17.25 (jam desimal)
    
    CONTOH:
    - "17:15" → 17.25 (17 + 15/60)
    - "10:45" → 10.75 (10 + 45/60)
    - "08:30" → 8.5 (8 + 30/60)
    """
    try:
        time_str = str(time_str).replace(',', '.').replace(':', '.')
        if '.' in time_str:
            h_str, m_part_str = time_str.split('.', 1)
            h = int(h_str) if h_str else 0
            m = int(m_part_str.ljust(2, '0')[:2])
            result = h + m / 60.0
            return result
        else:
            return float(time_str)
    except Exception:
        return np.nan

def konversi_jam(x):
    """
    FUNGSI 2: Konversi format jam rentang (20.00-22.00) ke rata-rata desimal (21.0)
    
    PENJELASAN:
    - Input: "20.00-22.00" (jam 20:00 sampai 22:00)
    - Proses: (20.0 + 22.0) / 2 = 21.0
    - Output: 21.0 (jam desimal rata-rata)
    
    CONTOH:
    - "20.00-22.00" → 21.0
    - "08.00-10.00" → 9.0
    - "12.00-14.00" → 13.0
    """
    if pd.isna(x) or str(x).strip() in ('-', '', 'nan'):
        return np.nan
    s = str(x).strip()
    try:
        parts = re.split(r'\s*-\s*', s)
        start_time_dec = parse_time_to_decimal(parts[0].strip())
        end_time_dec = parse_time_to_decimal(parts[1].strip()) if len(parts) > 1 else start_time_dec
        
        if len(parts) > 1 and pd.notna(start_time_dec) and pd.notna(end_time_dec) and end_time_dec < start_time_dec:
            end_time_dec += 24.0
        
        if pd.isna(start_time_dec) or pd.isna(end_time_dec):
            return np.nan
        return (start_time_dec + end_time_dec) / 2
    except Exception:
        return np.nan

def kategori_jam_otomatis(jam):
    """
    FUNGSI 3: Kategorisasi jam menjadi 3 kategori
    
    KATEGORI:
    - Sepi: Jam 0-6 atau 22-24 (malam hari)
    - Ramai: Jam 8-19 (siang hari)
    - Sedang: Jam 6-8 atau 19-22 (pagi/malam transisi)
    """
    if (jam <= 6) or (jam >= 22):
        return 'Sepi'
    elif (jam > 8 and jam <= 19):
        return 'Ramai'
    else:
        return 'Sedang'

print("✓ Fungsi parse_time_to_decimal() - konversi jam ke desimal")
print("✓ Fungsi konversi_jam() - konversi format rentang jam")
print("✓ Fungsi kategori_jam_otomatis() - kategorisasi jam")
print("\n✓✓✓ SEMUA FUNGSI BERHASIL DIDEFINISI ✓✓✓\n")

# ============================================================================
# STEP 3: LOAD DATA EXCEL
# ============================================================================
print("="*100)
print("[STEP 3] LOAD DATA DARI EXCEL")
print("="*100)

try:
    df_raw = pd.read_excel('DataParkir_Fix.xlsx')
    print(f"✓ File 'DataParkir_Fix.xlsx' berhasil dimuat!")
    print(f"\nINFORMASI DATA:")
    print(f"  - Jumlah baris: {len(df_raw)}")
    print(f"  - Jumlah kolom: {len(df_raw.columns)}")
    print(f"  - Nama kolom: {list(df_raw.columns)}")
    
except FileNotFoundError:
    print("⚠ File 'DataParkir_Fix.xlsx' TIDAK DITEMUKAN!")
    print("  Membuat DATA DUMMY untuk demonstrasi...\n")
    
    np.random.seed(42)
    df_raw = pd.DataFrame({
        'Hari Operasional': ['Senin-Jumat'] * 30 + ['Sabtu-Minggu'] * 30,
        'Jam': (['08.00-10.00', '10.00-12.00', '14.00-16.00', '16.00-18.00', '18.00-20.00'] * 12),
        'Jumlah Motor Weekday': np.random.randint(80, 200, 60),
        'Jumlah Motor Weekend': np.random.randint(60, 180, 60),
        'Jumlah Mobil Weekday': np.random.randint(40, 150, 60),
        'Jumlah Mobil Weekend': np.random.randint(30, 120, 60),
        'Class_Motor': np.random.choice(['Rendah', 'Sedang', 'Tinggi'], 60),
        'Class_Mobil': np.random.choice(['Rendah', 'Sedang', 'Tinggi'], 60),
    })
    print(f"✓ Data dummy berhasil dibuat: {len(df_raw)} baris")

# ============================================================================
# STEP 4: TAMPILKAN DATA MENTAH
# ============================================================================
print("\n" + "="*100)
print("[STEP 4] MENAMPILKAN DATA MENTAH (RAW DATA)")
print("="*100)

print(f"\nData mentah sebelum cleaning:")
print(f"Shape: {df_raw.shape} (baris, kolom)")
print(f"\n{'FIRST 10 ROWS':-^100}")
print(df_raw.head(10).to_string())

print(f"\n{'DATA INFO':-^100}")
print(f"Data Types:")
print(df_raw.dtypes)

print(f"\n{'MISSING VALUES':-^100}")
print(f"Jumlah nilai kosong di setiap kolom:")
print(df_raw.isnull().sum())

print(f"\n{'STATISTIK DATA NUMERIK':-^100}")
print(df_raw.describe())

print(f"\n{'DISTRIBUSI CLASS TARGET':-^100}")
print("Class_Motor:")
print(df_raw['Class_Motor'].value_counts())
print("\nClass_Mobil:")
print(df_raw['Class_Mobil'].value_counts())

# ============================================================================
# STEP 5: DATA CLEANING
# ============================================================================
print("\n" + "="*100)
print("[STEP 5] DATA CLEANING (PEMBERSIHAN DATA)")
print("="*100)

print("\nProses cleaning yang dilakukan:")
print("1. Konversi kolom 'Jam' ke format desimal")
print("2. Kategorisasi jam ke Sepi/Sedang/Ramai")
print("3. Hapus baris dengan nilai NaN (missing values)")
print("4. Hapus duplikat")

# 5.1 Konversi jam
df = df_raw.copy()
print(f"\n[5.1] Konversi kolom 'Jam' ke 'Jam_Desimal'...")
df['Jam_Desimal'] = df['Jam'].apply(konversi_jam)
print(f"✓ Konversi selesai")
print(f"\nContoh konversi jam:")
sample_jam = df[['Jam', 'Jam_Desimal']].head(10).copy()
print(sample_jam.to_string(index=False))

# 5.2 Kategorisasi jam
print(f"\n[5.2] Kategorisasi jam ke Sepi/Sedang/Ramai...")
df['Kategori_Jam'] = df['Jam_Desimal'].apply(kategori_jam_otomatis)
print(f"✓ Kategorisasi selesai")
print(f"\nDistribusi kategori jam:")
print(df['Kategori_Jam'].value_counts())

# 5.3 Hapus missing values
print(f"\n[5.3] Menghapus baris dengan nilai NaN...")
rows_before = len(df)
df_clean = df.dropna(subset=['Class_Motor', 'Class_Mobil', 'Jam_Desimal'])
rows_after = len(df_clean)
rows_removed = rows_before - rows_after
print(f"✓ Baris sebelum: {rows_before}")
print(f"✓ Baris sesudah: {rows_after}")
print(f"✓ Baris dihapus: {rows_removed}")

# ============================================================================
# STEP 6: TAMPILKAN DATA SETELAH CLEANING
# ============================================================================
print("\n" + "="*100)
print("[STEP 6] MENAMPILKAN DATA SETELAH CLEANING")
print("="*100)

print(f"\nData setelah cleaning:")
print(f"Shape: {df_clean.shape} (baris, kolom)")

print(f"\n{'FIRST 10 ROWS (AFTER CLEANING)':-^100}")
print(df_clean.head(10).to_string())

print(f"\n{'MISSING VALUES AFTER CLEANING':-^100}")
print(df_clean.isnull().sum())

print(f"\n{'STATISTIK DATA SETELAH CLEANING':-^100}")
print(df_clean[['Jumlah Motor Weekday', 'Jumlah Motor Weekend', 
                'Jumlah Mobil Weekday', 'Jumlah Mobil Weekend', 'Jam_Desimal']].describe())

print(f"\n{'DISTRIBUSI CLASS SETELAH CLEANING':-^100}")
print("Class_Motor:")
print(df_clean['Class_Motor'].value_counts())
print("\nClass_Mobil:")
print(df_clean['Class_Mobil'].value_counts())

# ============================================================================
# STEP 7: PERSIAPAN FITUR & TARGET VARIABLE
# ============================================================================
print("\n" + "="*100)
print("[STEP 7] PERSIAPAN FITUR & TARGET VARIABLE")
print("="*100)

feature_cols = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend', 
                'Jumlah Mobil Weekday', 'Jumlah Mobil Weekend', 'Jam_Desimal']

X = df_clean[feature_cols].copy()
print(f"\nFitur yang digunakan untuk training:")
for i, col in enumerate(feature_cols, 1):
    print(f"  {i}. {col}")

print(f"\nShape fitur X: {X.shape} (baris, kolom)")
print(f"\nSampel fitur (5 baris):")
print(X.head(5).to_string())

# ============================================================================
# STEP 8: TRAINING MOTOR
# ============================================================================
print("\n" + "="*100)
print("[STEP 8] TRAINING MODEL UNTUK MOTOR")
print("="*100)

print("\n[8.1] Persiapan target variable Motor...")
y_motor = df_clean['Class_Motor']
print(f"✓ Target variable: Class_Motor")
print(f"✓ Shape: {y_motor.shape}")
print(f"\nDistribusi kelas:")
print(y_motor.value_counts())

print("\n[8.2] Encoding label Motor...")
le_motor = LabelEncoder()
y_motor_encoded = le_motor.fit_transform(y_motor)
print(f"✓ Label encoding:")
for kelas, encoded_val in zip(le_motor.classes_, le_motor.transform(le_motor.classes_)):
    print(f"  - {kelas} → {encoded_val}")

print("\n[8.3] Split data 80:20...")
X_train_motor, X_test_motor, y_train_motor, y_test_motor = train_test_split(
    X, y_motor_encoded, test_size=0.2, random_state=42, stratify=y_motor_encoded
)
print(f"✓ Training set: {len(X_train_motor)} sampel")
print(f"✓ Testing set: {len(X_test_motor)} sampel")
print(f"✓ Total: {len(X_train_motor) + len(X_test_motor)} sampel")

print("\n[8.4] Training Random Forest Motor...")
print("   Parameter yang digunakan:")
print("   - n_estimators: 150 (jumlah trees)")
print("   - max_depth: 15 (kedalaman max tree)")
print("   - min_samples_leaf: 3 (min sampel per leaf)")
print("   - random_state: 42 (reproducibility)")

model_motor = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)
model_motor.fit(X_train_motor, y_train_motor)
print(f"✓ Training selesai!")

print("\n[8.5] Evaluasi Motor...")
y_train_pred_motor = model_motor.predict(X_train_motor)
y_test_pred_motor = model_motor.predict(X_test_motor)

train_acc_motor = accuracy_score(y_train_motor, y_train_pred_motor)
test_acc_motor = accuracy_score(y_test_motor, y_test_pred_motor)
gap_motor = train_acc_motor - test_acc_motor

print(f"✓ Training Accuracy: {train_acc_motor:.4f} ({train_acc_motor*100:.2f}%)")
print(f"✓ Testing Accuracy: {test_acc_motor:.4f} ({test_acc_motor*100:.2f}%)")
print(f"✓ Overfitting Gap: {gap_motor:.4f} ({gap_motor*100:.2f}%)")

# ============================================================================
# STEP 9: TRAINING MOBIL
# ============================================================================
print("\n" + "="*100)
print("[STEP 9] TRAINING MODEL UNTUK MOBIL")
print("="*100)

print("\n[9.1] Persiapan target variable Mobil...")
y_mobil = df_clean['Class_Mobil']
print(f"✓ Target variable: Class_Mobil")
print(f"✓ Shape: {y_mobil.shape}")
print(f"\nDistribusi kelas:")
print(y_mobil.value_counts())

print("\n[9.2] Encoding label Mobil...")
le_mobil = LabelEncoder()
y_mobil_encoded = le_mobil.fit_transform(y_mobil)
print(f"✓ Label encoding:")
for kelas, encoded_val in zip(le_mobil.classes_, le_mobil.transform(le_mobil.classes_)):
    print(f"  - {kelas} → {encoded_val}")

print("\n[9.3] Split data 80:20...")
X_train_mobil, X_test_mobil, y_train_mobil, y_test_mobil = train_test_split(
    X, y_mobil_encoded, test_size=0.2, random_state=42, stratify=y_mobil_encoded
)
print(f"✓ Training set: {len(X_train_mobil)} sampel")
print(f"✓ Testing set: {len(X_test_mobil)} sampel")

print("\n[9.4] Training Random Forest Mobil...")
model_mobil = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)
model_mobil.fit(X_train_mobil, y_train_mobil)
print(f"✓ Training selesai!")

print("\n[9.5] Evaluasi Mobil...")
y_train_pred_mobil = model_mobil.predict(X_train_mobil)
y_test_pred_mobil = model_mobil.predict(X_test_mobil)

train_acc_mobil = accuracy_score(y_train_mobil, y_train_pred_mobil)
test_acc_mobil = accuracy_score(y_test_mobil, y_test_pred_mobil)
gap_mobil = train_acc_mobil - test_acc_mobil

print(f"✓ Training Accuracy: {train_acc_mobil:.4f} ({train_acc_mobil*100:.2f}%)")
print(f"✓ Testing Accuracy: {test_acc_mobil:.4f} ({test_acc_mobil*100:.2f}%)")
print(f"✓ Overfitting Gap: {gap_mobil:.4f} ({gap_mobil*100:.2f}%)")

# ============================================================================
# STEP 10: CONFUSION MATRIX
# ============================================================================
print("\n" + "="*100)
print("[STEP 10] CONFUSION MATRIX & CLASSIFICATION REPORT")
print("="*100)

print("\n{'='*50} MOTOR {'='*50}")
cm_motor = confusion_matrix(y_test_motor, y_test_pred_motor)
print("Confusion Matrix:")
print(cm_motor)

print("\nClassification Report:")
print(classification_report(y_test_motor, y_test_pred_motor, target_names=le_motor.classes_))

print("\n{'='*50} MOBIL {'='*50}")
cm_mobil = confusion_matrix(y_test_mobil, y_test_pred_mobil)
print("Confusion Matrix:")
print(cm_mobil)

print("\nClassification Report:")
print(classification_report(y_test_mobil, y_test_pred_mobil, target_names=le_mobil.classes_))

# ============================================================================
# STEP 11: FEATURE IMPORTANCE
# ============================================================================
print("\n" + "="*100)
print("[STEP 11] FEATURE IMPORTANCE")
print("="*100)

print("\n{'='*50} MOTOR {'='*50}")
importance_motor = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model_motor.feature_importances_
}).sort_values('Importance', ascending=False)
print(importance_motor.to_string(index=False))

print("\n{'='*50} MOBIL {'='*50}")
importance_mobil = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model_mobil.feature_importances_
}).sort_values('Importance', ascending=False)
print(importance_mobil.to_string(index=False))

# ============================================================================
# STEP 12: SIMULASI PREDIKSI
# ============================================================================
print("\n" + "="*100)
print("[STEP 12] SIMULASI PREDIKSI PADA DATA BARU")
print("="*100)

sample_1 = pd.DataFrame({
    'Jumlah Motor Weekday': [150],
    'Jumlah Motor Weekend': [120],
    'Jumlah Mobil Weekday': [80],
    'Jumlah Mobil Weekend': [60],
    'Jam_Desimal': [17.25]
})

print(f"\n[12.1] Sample Input #1:")
print(f"  - Jumlah Motor Weekday: 150")
print(f"  - Jumlah Motor Weekend: 120")
print(f"  - Jumlah Mobil Weekday: 80")
print(f"  - Jumlah Mobil Weekend: 60")
print(f"  - Jam_Desimal: 17.25 (pukul 17:15)")

pred_motor_1 = model_motor.predict(sample_1)[0]
proba_motor_1 = model_motor.predict_proba(sample_1)[0]

pred_mobil_1 = model_mobil.predict(sample_1)[0]
proba_mobil_1 = model_mobil.predict_proba(sample_1)[0]

print(f"\n  PREDIKSI MOTOR:")
print(f"  → Kelas: {le_motor.classes_[pred_motor_1]}")
for i, kelas in enumerate(le_motor.classes_):
    print(f"    - {kelas}: {proba_motor_1[i]*100:.2f}%")

print(f"\n  PREDIKSI MOBIL:")
print(f"  → Kelas: {le_mobil.classes_[pred_mobil_1]}")
for i, kelas in enumerate(le_mobil.classes_):
    print(f"    - {kelas}: {proba_mobil_1[i]*100:.2f}%")

# Sample 2
print(f"\n[12.2] Sample Input #2:")
sample_2 = pd.DataFrame({
    'Jumlah Motor Weekday': [80],
    'Jumlah Motor Weekend': [60],
    'Jumlah Mobil Weekday': [40],
    'Jumlah Mobil Weekend': [30],
    'Jam_Desimal': [9.0]
})

print(f"  - Jumlah Motor Weekday: 80")
print(f"  - Jumlah Motor Weekend: 60")
print(f"  - Jumlah Mobil Weekday: 40")
print(f"  - Jumlah Mobil Weekend: 30")
print(f"  - Jam_Desimal: 9.0 (pukul 09:00)")

pred_motor_2 = model_motor.predict(sample_2)[0]
proba_motor_2 = model_motor.predict_proba(sample_2)[0]

pred_mobil_2 = model_mobil.predict(sample_2)[0]
proba_mobil_2 = model_mobil.predict_proba(sample_2)[0]

print(f"\n  PREDIKSI MOTOR:")
print(f"  → Kelas: {le_motor.classes_[pred_motor_2]}")
for i, kelas in enumerate(le_motor.classes_):
    print(f"    - {kelas}: {proba_motor_2[i]*100:.2f}%")

print(f"\n  PREDIKSI MOBIL:")
print(f"  → Kelas: {le_mobil.classes_[pred_mobil_2]}")
for i, kelas in enumerate(le_mobil.classes_):
    print(f"    - {kelas}: {proba_mobil_2[i]*100:.2f}%")

# ============================================================================
# STEP 13: VISUALISASI
# ============================================================================
print("\n" + "="*100)
print("[STEP 13] MEMBUAT VISUALISASI")
print("="*100)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Confusion Matrix Motor
sns.heatmap(cm_motor, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0],
            xticklabels=le_motor.classes_, yticklabels=le_motor.classes_)
axes[0, 0].set_title('Confusion Matrix - Motor')
axes[0, 0].set_ylabel('True Label')
axes[0, 0].set_xlabel('Predicted Label')

# Confusion Matrix Mobil
sns.heatmap(cm_mobil, annot=True, fmt='d', cmap='Greens', ax=axes[0, 1],
            xticklabels=le_mobil.classes_, yticklabels=le_mobil.classes_)
axes[0, 1].set_title('Confusion Matrix - Mobil')
axes[0, 1].set_ylabel('True Label')
axes[0, 1].set_xlabel('Predicted Label')

# Feature Importance Motor
axes[1, 0].barh(importance_motor['Feature'], importance_motor['Importance'], color='skyblue')
axes[1, 0].set_title('Feature Importance - Motor')
axes[1, 0].set_xlabel('Importance')

# Feature Importance Mobil
axes[1, 1].barh(importance_mobil['Feature'], importance_mobil['Importance'], color='lightgreen')
axes[1, 1].set_title('Feature Importance - Mobil')
axes[1, 1].set_xlabel('Importance')

plt.tight_layout()
plt.savefig('hasil_simulasi_lengkap.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Visualisasi disimpan: hasil_simulasi_lengkap.png")
plt.show()

# ============================================================================
# STEP 14: SUMMARY
# ============================================================================
print("\n" + "="*100)
print("[STEP 14] RINGKASAN HASIL TRAINING")
print("="*100)

summary_table = pd.DataFrame({
    'Metrik': [
        'Training Accuracy',
        'Testing Accuracy',
        'Overfitting Gap',
        'Total Estimators',
        'Max Depth',
        'Min Samples Leaf',
        'Data Training',
        'Data Testing'
    ],
    'Motor': [
        f"{train_acc_motor*100:.2f}%",
        f"{test_acc_motor*100:.2f}%",
        f"{gap_motor*100:.2f}%",
        '150',
        '15',
        '3',
        f"{len(X_train_motor)} sampel",
        f"{len(X_test_motor)} sampel"
    ],
    'Mobil': [
        f"{train_acc_mobil*100:.2f}%",
        f"{test_acc_mobil*100:.2f}%",
        f"{gap_mobil*100:.2f}%",
        '150',
        '15',
        '3',
        f"{len(X_train_mobil)} sampel",
        f"{len(X_test_mobil)} sampel"
    ]
})

print("\n" + summary_table.to_string(index=False))

print("\n" + "="*100)
print("✓✓✓ SIMULASI LENGKAP SELESAI ✓✓✓")
print("="*100)

print(f"""
PENJELASAN HASIL:

1. DATA LOADING:
   - Membaca file Excel dan membuat dummy jika tidak ada
   - Total data mentah: {len(df_raw)} baris

2. DATA CLEANING:
   - Konversi format jam ke desimal
   - Kategorisasi jam (Sepi/Sedang/Ramai)
   - Hapus missing values
   - Final data: {len(df_clean)} baris ({rows_removed} dihapus)

3. FEATURE ENGINEERING:
   - Menggunakan 5 fitur untuk training
   - Fitur: {', '.join(feature_cols)}

4. MODEL TRAINING:
   - Random Forest dengan 150 trees
   - Split data 80:20
   - Motor accuracy: {test_acc_motor*100:.2f}%
   - Mobil accuracy: {test_acc_mobil*100:.2f}%

5. EVALUASI:
   - Menggunakan Confusion Matrix
   - Classification Report
   - Feature Importance Analysis

6. PREDIKSI:
   - Sample 1: Motor → {le_motor.classes_[pred_motor_1]}, Mobil → {le_mobil.classes_[pred_mobil_1]}
   - Sample 2: Motor → {le_motor.classes_[pred_motor_2]}, Mobil → {le_mobil.classes_[pred_mobil_2]}

SETIAP TAHAP SUDAH DIJELASKAN DI ATAS!
""")
