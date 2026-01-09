"""
SIMULASI LENGKAP: Tarif Parkir Progresif Random Forest
Script ini menunjukkan SETIAP TAHAP tanpa menggunakan Streamlit
Bisa dijalankan di terminal/PowerShell dengan: python simulasi_training.py
"""

import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

print("="*80)
print("SIMULASI LENGKAP: PREDIKSI TARIF PARKIR MENGGUNAKAN RANDOM FOREST")
print("="*80)

# ============================================================================
# TAHAP 1: FUNGSI-FUNGSI UTILITY
# ============================================================================
print("\n[TAHAP 1] Membuat Fungsi-Fungsi Utility...")
print("-" * 80)

def parse_time_to_decimal(time_str):
    """Konversi waktu HH:MM atau HH.MM ke jam desimal (jam + menit/60)"""
    try:
        time_str = str(time_str).replace(',', '.').replace(':', '.')
        if '.' in time_str:
            h_str, m_part_str = time_str.split('.', 1)
            h = int(h_str) if h_str else 0
            m = int(m_part_str.ljust(2, '0')[:2])  # 2 digit pertama = menit
            return h + m / 60.0
        else:
            return float(time_str)
    except Exception:
        return np.nan

def konversi_jam(x):
    """Konversi format jam rentang (20.00-22.00) ke jam desimal rata-rata (21.0)"""
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
    """Kategorisasi jam menjadi Sepi/Sedang/Ramai"""
    if (jam <= 6) or (jam >= 22):
        return 'Sepi'
    elif (jam > 8 and jam <= 19):
        return 'Ramai'
    else:
        return 'Sedang'

print("✓ Fungsi parse_time_to_decimal() - konversi jam ke desimal")
print("✓ Fungsi konversi_jam() - konversi format rentang jam")
print("✓ Fungsi kategori_jam_otomatis() - kategorisasi jam")

# ============================================================================
# TAHAP 2: LOAD DATA
# ============================================================================
print("\n[TAHAP 2] Memuat Data dari Excel...")
print("-" * 80)

try:
    df = pd.read_excel('DataParkir_Fix.xlsx')
    print(f"✓ Data berhasil dimuat dari 'DataParkir_Fix.xlsx'")
    print(f"  - Jumlah baris: {len(df)}")
    print(f"  - Jumlah kolom: {len(df.columns)}")
    print(f"  - Kolom: {list(df.columns)}")
except FileNotFoundError:
    print("⚠ File 'DataParkir_Fix.xlsx' tidak ditemukan!")
    print("  Membuat data DUMMY untuk demonstrasi...")
    
    # Data dummy untuk testing
    df = pd.DataFrame({
        'Hari Operasional': ['Senin-Jumat'] * 30 + ['Sabtu-Minggu'] * 30,
        'Jam': ['08.00-10.00', '10.00-12.00', '12.00-14.00'] * 20,
        'Jumlah Motor Weekday': np.random.randint(50, 200, 60),
        'Jumlah Motor Weekend': np.random.randint(30, 150, 60),
        'Jumlah Mobil Weekday': np.random.randint(30, 150, 60),
        'Jumlah Mobil Weekend': np.random.randint(20, 100, 60),
        'Class_Motor': np.random.choice(['Rendah', 'Sedang', 'Tinggi'], 60),
        'Class_Mobil': np.random.choice(['Rendah', 'Sedang', 'Tinggi'], 60),
    })
    print("✓ Data dummy berhasil dibuat (60 baris)")

print(f"\nSampel data (5 baris pertama):")
print(df.head())

# ============================================================================
# TAHAP 3: DATA PREPROCESSING
# ============================================================================
print("\n[TAHAP 3] Preprocessing Data...")
print("-" * 80)

# Konversi jam
df['Jam_Desimal'] = df['Jam'].apply(konversi_jam)
print(f"✓ Konversi jam ke desimal (contoh: '08.00-10.00' → {df['Jam_Desimal'].iloc[0]:.2f})")

# Kategorisasi jam
df['Kategori_Jam'] = df['Jam_Desimal'].apply(kategori_jam_otomatis)
print(f"✓ Kategorisasi jam otomatis (Sepi/Sedang/Ramai)")

# Hapus baris dengan nilai NaN
df_clean = df.dropna(subset=['Class_Motor', 'Class_Mobil', 'Jam_Desimal'])
print(f"✓ Hapus baris dengan nilai NaN")
print(f"  - Data sebelum: {len(df)} baris")
print(f"  - Data sesudah: {len(df_clean)} baris")
print(f"  - Data dihapus: {len(df) - len(df_clean)} baris")

# Fitur yang digunakan untuk training
feature_cols = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend', 
                'Jumlah Mobil Weekday', 'Jumlah Mobil Weekend', 'Jam_Desimal']

X = df_clean[feature_cols].copy()
print(f"\n✓ Fitur yang digunakan: {feature_cols}")
print(f"  - Shape: {X.shape}")

# ============================================================================
# TAHAP 4: TRAINING UNTUK MOTOR
# ============================================================================
print("\n[TAHAP 4a] TRAINING MODEL UNTUK MOTOR...")
print("-" * 80)

y_motor = df_clean['Class_Motor']
print(f"Target variable: Class_Motor")
print(f"Distribusi kelas:")
print(y_motor.value_counts())

# Encode label
le_motor = LabelEncoder()
y_motor_encoded = le_motor.fit_transform(y_motor)
print(f"✓ Label encoding: {dict(zip(le_motor.classes_, le_motor.transform(le_motor.classes_)))}")

# Split data
X_train_motor, X_test_motor, y_train_motor, y_test_motor = train_test_split(
    X, y_motor_encoded, test_size=0.2, random_state=42, stratify=y_motor_encoded
)
print(f"\n✓ Split data 80:20")
print(f"  - Training: {len(X_train_motor)} sampel")
print(f"  - Testing: {len(X_test_motor)} sampel")

# Training model
print(f"\n✓ Training Random Forest Classifier...")
print(f"  - n_estimators: 150")
print(f"  - max_depth: 15")
print(f"  - min_samples_leaf: 3")
print(f"  - random_state: 42")

model_motor = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)
model_motor.fit(X_train_motor, y_train_motor)
print(f"✓ Model training selesai!")

# Prediksi
y_pred_motor = model_motor.predict(X_test_motor)
accuracy_motor = accuracy_score(y_test_motor, y_pred_motor)
print(f"\n✓ Akurasi Model Motor: {accuracy_motor:.4f} ({accuracy_motor*100:.2f}%)")

# Training accuracy
y_train_pred_motor = model_motor.predict(X_train_motor)
train_accuracy_motor = accuracy_score(y_train_motor, y_train_pred_motor)
print(f"✓ Training Accuracy Motor: {train_accuracy_motor:.4f} ({train_accuracy_motor*100:.2f}%)")
print(f"✓ Overfitting Gap: {(train_accuracy_motor - accuracy_motor)*100:.2f}%")

# ============================================================================
# TAHAP 4B: TRAINING UNTUK MOBIL
# ============================================================================
print("\n[TAHAP 4b] TRAINING MODEL UNTUK MOBIL...")
print("-" * 80)

y_mobil = df_clean['Class_Mobil']
print(f"Target variable: Class_Mobil")
print(f"Distribusi kelas:")
print(y_mobil.value_counts())

# Encode label
le_mobil = LabelEncoder()
y_mobil_encoded = le_mobil.fit_transform(y_mobil)
print(f"✓ Label encoding: {dict(zip(le_mobil.classes_, le_mobil.transform(le_mobil.classes_)))}")

# Split data
X_train_mobil, X_test_mobil, y_train_mobil, y_test_mobil = train_test_split(
    X, y_mobil_encoded, test_size=0.2, random_state=42, stratify=y_mobil_encoded
)
print(f"\n✓ Split data 80:20")
print(f"  - Training: {len(X_train_mobil)} sampel")
print(f"  - Testing: {len(X_test_mobil)} sampel")

# Training model
print(f"\n✓ Training Random Forest Classifier...")
model_mobil = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)
model_mobil.fit(X_train_mobil, y_train_mobil)
print(f"✓ Model training selesai!")

# Prediksi
y_pred_mobil = model_mobil.predict(X_test_mobil)
accuracy_mobil = accuracy_score(y_test_mobil, y_pred_mobil)
print(f"\n✓ Akurasi Model Mobil: {accuracy_mobil:.4f} ({accuracy_mobil*100:.2f}%)")

# Training accuracy
y_train_pred_mobil = model_mobil.predict(X_train_mobil)
train_accuracy_mobil = accuracy_score(y_train_mobil, y_train_pred_mobil)
print(f"✓ Training Accuracy Mobil: {train_accuracy_mobil:.4f} ({train_accuracy_mobil*100:.2f}%)")
print(f"✓ Overfitting Gap: {(train_accuracy_mobil - accuracy_mobil)*100:.2f}%")

# ============================================================================
# TAHAP 5: CONFUSION MATRIX & CLASSIFICATION REPORT
# ============================================================================
print("\n[TAHAP 5] Evaluasi Model dengan Confusion Matrix & Classification Report...")
print("-" * 80)

print("\n=== MOTOR ===")
cm_motor = confusion_matrix(y_test_motor, y_pred_motor)
print("Confusion Matrix:")
print(cm_motor)
print("\nClassification Report:")
print(classification_report(y_test_motor, y_pred_motor, target_names=le_motor.classes_))

print("\n=== MOBIL ===")
cm_mobil = confusion_matrix(y_test_mobil, y_pred_mobil)
print("Confusion Matrix:")
print(cm_mobil)
print("\nClassification Report:")
print(classification_report(y_test_mobil, y_pred_mobil, target_names=le_mobil.classes_))

# ============================================================================
# TAHAP 6: FEATURE IMPORTANCE
# ============================================================================
print("\n[TAHAP 6] Feature Importance Analysis...")
print("-" * 80)

importance_motor = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model_motor.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n=== MOTOR ===")
print(importance_motor.to_string(index=False))

importance_mobil = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model_mobil.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n=== MOBIL ===")
print(importance_mobil.to_string(index=False))

# ============================================================================
# TAHAP 7: CONTOH PREDIKSI (INFERENCE)
# ============================================================================
print("\n[TAHAP 7] Contoh Prediksi pada Data Baru...")
print("-" * 80)

# Sample baru
sample_baru = pd.DataFrame({
    'Jumlah Motor Weekday': [150],
    'Jumlah Motor Weekend': [120],
    'Jumlah Mobil Weekday': [80],
    'Jumlah Mobil Weekend': [60],
    'Jam_Desimal': [17.25]  # 17:15
})

print(f"\nSample data baru:")
print(sample_baru)

# Prediksi
pred_motor = model_motor.predict(sample_baru)[0]
pred_motor_prob = model_motor.predict_proba(sample_baru)[0]

pred_mobil = model_mobil.predict(sample_baru)[0]
pred_mobil_prob = model_mobil.predict_proba(sample_baru)[0]

print(f"\n✓ Prediksi untuk Motor:")
print(f"  - Kelas: {le_motor.classes_[pred_motor]}")
print(f"  - Probabilitas:")
for i, kelas in enumerate(le_motor.classes_):
    print(f"    * {kelas}: {pred_motor_prob[i]*100:.2f}%")

print(f"\n✓ Prediksi untuk Mobil:")
print(f"  - Kelas: {le_mobil.classes_[pred_mobil]}")
print(f"  - Probabilitas:")
for i, kelas in enumerate(le_mobil.classes_):
    print(f"    * {kelas}: {pred_mobil_prob[i]*100:.2f}%")

# ============================================================================
# TAHAP 8: VISUALISASI HASIL
# ============================================================================
print("\n[TAHAP 8] Membuat Visualisasi Hasil...")
print("-" * 80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Confusion Matrix Motor
sns.heatmap(cm_motor, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0],
            xticklabels=le_motor.classes_, yticklabels=le_motor.classes_)
axes[0, 0].set_title('Confusion Matrix - Motor')
axes[0, 0].set_ylabel('True Label')
axes[0, 0].set_xlabel('Predicted Label')

# 2. Confusion Matrix Mobil
sns.heatmap(cm_mobil, annot=True, fmt='d', cmap='Greens', ax=axes[0, 1],
            xticklabels=le_mobil.classes_, yticklabels=le_mobil.classes_)
axes[0, 1].set_title('Confusion Matrix - Mobil')
axes[0, 1].set_ylabel('True Label')
axes[0, 1].set_xlabel('Predicted Label')

# 3. Feature Importance Motor
axes[1, 0].barh(importance_motor['Feature'], importance_motor['Importance'], color='skyblue')
axes[1, 0].set_title('Feature Importance - Motor')
axes[1, 0].set_xlabel('Importance')

# 4. Feature Importance Mobil
axes[1, 1].barh(importance_mobil['Feature'], importance_mobil['Importance'], color='lightgreen')
axes[1, 1].set_title('Feature Importance - Mobil')
axes[1, 1].set_xlabel('Importance')

plt.tight_layout()
plt.savefig('hasil_simulasi.png', dpi=300, bbox_inches='tight')
print(f"✓ Visualisasi disimpan ke 'hasil_simulasi.png'")
plt.show()

# ============================================================================
# TAHAP 9: RINGKASAN HASIL
# ============================================================================
print("\n" + "="*80)
print("RINGKASAN HASIL TRAINING")
print("="*80)

summary_data = {
    'Metrik': ['Training Accuracy', 'Testing Accuracy', 'Overfitting Gap', 'Jumlah Estimator', 'Max Depth', 'Min Samples Leaf'],
    'Motor': [
        f"{train_accuracy_motor*100:.2f}%",
        f"{accuracy_motor*100:.2f}%",
        f"{(train_accuracy_motor - accuracy_motor)*100:.2f}%",
        '150',
        '15',
        '3'
    ],
    'Mobil': [
        f"{train_accuracy_mobil*100:.2f}%",
        f"{accuracy_mobil*100:.2f}%",
        f"{(train_accuracy_mobil - accuracy_mobil)*100:.2f}%",
        '150',
        '15',
        '3'
    ]
}

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

print("\n" + "="*80)
print("SIMULASI SELESAI!")
print("="*80)
print("\nFile yang dihasilkan:")
print("- hasil_simulasi.png: Visualisasi hasil training")
print("\nUntuk melihat decision tree, gunakan:")
print("  from sklearn.tree import plot_tree")
print("  plot_tree(model_motor.estimators_[0], feature_names=feature_cols, filled=True)")
