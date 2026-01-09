"""
SIMULASI LENGKAP: Prediksi Tarif Parkir Progresif dengan Random Forest
Menggunakan data actual dari DataParkir_Fix.xlsx

Format: Load Data → Cleaning → Visualisasi → Modeling → Evaluasi → Prediksi
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import plot_tree
import seaborn as sns
import matplotlib.pyplot as plt
import re
import datetime
import folium
from folium import plugins

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("="*100)
print("[STEP 1] LOAD DATA")
print("="*100)

file_path = 'DataParkir_Fix.xlsx'
df = pd.read_excel(file_path)

print(f"\n✓ Data berhasil dimuat dari: {file_path}")
print(f"  Shape: {df.shape} (baris, kolom)")
print(f"\nPreview Data (5 baris pertama):")
print(df.head())

# ============================================================================
# STEP 2: TAMPILKAN FITUR UTAMA
# ============================================================================
print("\n" + "="*100)
print("[STEP 2] TAMPILKAN FITUR UTAMA YANG DIGUNAKAN")
print("="*100)

fitur_utama = [
    'Titik', 'Latitude', 'Longitude',
    'Jumlah Motor Weekday', 'Jumlah Mobil Weekday',
    'Jumlah Motor Weekend', 'Jumlah Mobil Weekend',
    'Jam Ramai Mobil Weekday', 'Jam Ramai Motor Weekday',
    'Jam Ramai Mobil Weekend', 'Jam Ramai Motor Weekend',
    'Jam Sedang Motor Weekday', 'Jam Sedang Mobil Weekday',
    'Jam Sedang Motor Weekend', 'Jam Sedang Mobil Weekend',
    'Jam Sepi Motor Weekday', 'Jam Sepi Mobil Weekday',
    'Jam Sepi Motor Weekend', 'Jam Sepi Mobil Weekend',
    'Pendapatan Tarif Parkir Weekday Motor per tahun',
    'Pendapatan Tarif Parkir Weekday Mobil per tahun',
    'Pendapatan Tarif Parkir Weekend Motor per tahun',
    'Pendapatan Tarif Parkir Weekend Mobil per tahun'
]

fitur_terpakai = [col for col in fitur_utama if col in df.columns]
df_subset = df[fitur_terpakai]
print(f"\n=== FITUR UTAMA YANG DIGUNAKAN (5 baris pertama) ===")
print(df_subset.head())
print("=" * 100)

# ============================================================================
# STEP 3: FUNGSI KONVERSI JAM
# ============================================================================
print("\n" + "="*100)
print("[STEP 3] FUNGSI KONVERSI JAM")
print("="*100)

def konversi_jam(x):
    """Mengubah format jam (cth: '20.00-22.00') menjadi jam desimal rata-rata (cth: 21.0)."""
    if pd.isna(x) or str(x).strip() == '-':
        return np.nan
    s = str(x).strip()
    parts = s.split('-')
    
    start_str = parts[0]
    end_str = parts[1] if len(parts) > 1 else parts[0]
    
    def to_minutes(time_str):
        time_str = time_str.replace('.', ':')
        h, m = 0, 0
        try:
            if ':' in time_str:
                h, m = map(int, time_str.split(':'))
            else:
                h = int(time_str)
        except ValueError:
            return 0
        return h * 60 + m
    
    start_min = to_minutes(start_str)
    end_min = to_minutes(end_str)
    
    if start_min == end_min and len(parts) == 1:
        return start_min / 60
    
    avg_min = (start_min + end_min) / 2
    return (avg_min / 60)

print("\n✓ Fungsi konversi_jam() berhasil dibuat")
print("\nContoh hasil konversi jam:")
sample_jam_cols = ['Jam Ramai Mobil Weekday', 'Jam Sedang Motor Weekday', 'Jam Sepi Mobil Weekend']
for col in sample_jam_cols:
    if col in df.columns:
        original = df[col].iloc[0]
        converted = konversi_jam(original)
        print(f"  '{original}' → {converted:.2f}")

# ============================================================================
# MAPPING TARIF DASAR (Dari app.py)
# ============================================================================
tarif_mapping = {
    'Motor': {'Rendah': 1000, 'Sedang': 2000, 'Tinggi': 3000},
    'Mobil': {'Rendah': 3000, 'Sedang': 4000, 'Tinggi': 5000}
}

# ============================================================================
# FUNGSI HELPER (Dari app.py) - UNTUK SIMULASI & ANALISIS SPASIAL
# ============================================================================

def kategori_jam_otomatis(jam):
    """Kategorisasi jam otomatis berdasarkan nilai desimal."""
    if (jam <= 6) or (jam >= 22):
        return 'Sepi'
    elif (jam > 8 and jam <= 19):
        return 'Ramai'
    else:
        return 'Sedang'

def time_to_decimal_hour(time_obj):
    """Mengkonversi objek datetime.time (H:M) menjadi jam desimal (H + M/60)."""
    if time_obj is None:
        return np.nan
    return time_obj.hour + time_obj.minute / 60.0

def calculate_progresif_tarif(jenis, potensi_class, jam_desimal):
    """Menerapkan logika tarif progresif berdasarkan potensi dan jam."""
    tarif_dasar = tarif_mapping[jenis].get(potensi_class, 0)
    
    # Logika Progresif (Contoh: Kenaikan Tarif di Atas Jam 9.00)
    if jam_desimal > 9.0:
        if potensi_class == 'Tinggi':
            return tarif_dasar + 1000  # Misalnya dari 3000 jadi 4000
        elif potensi_class == 'Sedang':
            return tarif_dasar + 500  # Misalnya dari 2000 jadi 2500
        else:
            return tarif_dasar
    else:
        return tarif_dasar

# ============================================================================# STEP 4: DATA CLEANING
# ============================================================================
print("\n" + "="*100)
print("[STEP 4] DATA CLEANING & PREPROCESSING")
print("="*100)

df_clean = df.copy()

# 4.1 Cleaning kolom Pendapatan
print("\n[4.1] Membersihkan kolom Pendapatan...")
pend_cols = [
    'Pendapatan Tarif Parkir Weekday Motor per tahun',
    'Pendapatan Tarif Parkir Weekday Mobil per tahun',
    'Pendapatan Tarif Parkir Weekend Motor per tahun',
    'Pendapatan Tarif Parkir Weekend Mobil per tahun'
]

for c in pend_cols:
    if c in df_clean.columns:
        df_clean[c] = df_clean[c].astype(str).str.replace(r'[^\d,\.]', '', regex=True)
        df_clean[c] = df_clean[c].str.replace('.', '', regex=False)
        df_clean[c] = df_clean[c].str.replace(',', '.', regex=False)
        df_clean[c] = pd.to_numeric(df_clean[c], errors='coerce').fillna(0)

print("✓ Kolom Pendapatan dibersihkan")

# 4.2 Konversi kolom Jam
print("\n[4.2] Mengkonversi kolom Jam ke format desimal...")
jam_cols = [c for c in df_clean.columns if 'Jam' in c and 'per tahun' not in c]
for col in jam_cols:
    df_clean[col] = df_clean[col].apply(konversi_jam)
    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())

print(f"✓ {len(jam_cols)} kolom Jam berhasil dikonversi")

# 4.3 Handle Missing Values
print("\n[4.3] Handle Missing Values...")
for col in df_clean.columns:
    if df_clean[col].dtype != 'object':
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    else:
        if df_clean[col].isnull().any():
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else 'Unknown')

print(f"✓ Data setelah pembersihan: {df_clean.shape[0]} baris")

# ============================================================================
# STEP 5: FEATURE ENGINEERING & KLASIFIKASI
# ============================================================================
print("\n" + "="*100)
print("[STEP 5] FEATURE ENGINEERING & KLASIFIKASI TARGET")
print("="*100)

# 5.1 Total Pendapatan
print("\n[5.1] Menghitung Total Pendapatan...")
motor_pend_cols = [c for c in pend_cols if 'Motor' in c]
mobil_pend_cols = [c for c in pend_cols if 'Mobil' in c]

df_clean['Total_Pendapatan_Tahun'] = df_clean[pend_cols].sum(axis=1)
df_clean['Total_Pend_Motor'] = df_clean[motor_pend_cols].sum(axis=1)
df_clean['Total_Pend_Mobil'] = df_clean[mobil_pend_cols].sum(axis=1)

print(f"✓ Total Pendapatan dihitung")
print(f"  Mean Total Pend Motor: Rp{df_clean['Total_Pend_Motor'].mean():,.0f}")
print(f"  Mean Total Pend Mobil: Rp{df_clean['Total_Pend_Mobil'].mean():,.0f}")

# 5.2 Klasifikasi Potensi Tarif (Qcut)
print("\n[5.2] Klasifikasi Potensi Tarif (3 kategori)...")
try:
    df_clean['Class_Motor'] = pd.qcut(df_clean['Total_Pend_Motor'], q=3, labels=['Rendah','Sedang','Tinggi'])
    df_clean['Class_Mobil'] = pd.qcut(df_clean['Total_Pend_Mobil'], q=3, labels=['Rendah','Sedang','Tinggi'])
except ValueError as e:
    print(f"⚠ Peringatan qcut: {e}")
    df_clean['Class_Motor'] = pd.cut(df_clean['Total_Pend_Motor'], 
                                      bins=[-np.inf, df_clean['Total_Pend_Motor'].quantile(0.5), np.inf], 
                                      labels=['Rendah', 'Tinggi']).fillna('Rendah')
    df_clean['Class_Mobil'] = pd.cut(df_clean['Total_Pend_Mobil'], 
                                      bins=[-np.inf, df_clean['Total_Pend_Mobil'].quantile(0.5), np.inf], 
                                      labels=['Rendah', 'Tinggi']).fillna('Rendah')

print("✓ Klasifikasi berhasil dibuat")

# Tampilkan batas kuantil
try:
    batas_motor = df_clean['Total_Pend_Motor'].quantile([0.333, 0.666])
    batas_mobil = df_clean['Total_Pend_Mobil'].quantile([0.333, 0.666])
    
    print("\n💰 BATAS KUANTIL TOTAL PENDAPATAN TAHUNAN (RUPIAH) 💰")
    print("\n--- MOTOR ---")
    print(f"  Rendah : Pendapatan < Rp{batas_motor.loc[0.333]:,.0f}")
    print(f"  Sedang : Rp{batas_motor.loc[0.333]:,.0f} s/d Rp{batas_motor.loc[0.666]:,.0f}")
    print(f"  Tinggi : Pendapatan > Rp{batas_motor.loc[0.666]:,.0f}")
    
    print("\n--- MOBIL ---")
    print(f"  Rendah : Pendapatan < Rp{batas_mobil.loc[0.333]:,.0f}")
    print(f"  Sedang : Rp{batas_mobil.loc[0.333]:,.0f} s/d Rp{batas_mobil.loc[0.666]:,.0f}")
    print(f"  Tinggi : Pendapatan > Rp{batas_mobil.loc[0.666]:,.0f}")
except:
    pass

print("\nDistribusi Kelas Motor:")
print(df_clean['Class_Motor'].value_counts())
print("\nDistribusi Kelas Mobil:")
print(df_clean['Class_Mobil'].value_counts())

# ============================================================================
# STEP 6: PERSIAPAN FITUR UNTUK MODELING
# ============================================================================
print("\n" + "="*100)
print("[STEP 6] PERSIAPAN FITUR UNTUK MODELING")
print("="*100)

fitur_motor = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend'] + [c for c in jam_cols if 'Motor' in c]
fitur_mobil = ['Jumlah Mobil Weekday', 'Jumlah Mobil Weekend'] + [c for c in jam_cols if 'Mobil' in c]

print(f"\n✓ Fitur Motor ({len(fitur_motor)} fitur):")
for i, f in enumerate(fitur_motor, 1):
    print(f"  {i}. {f}")

print(f"\n✓ Fitur Mobil ({len(fitur_mobil)} fitur):")
for i, f in enumerate(fitur_mobil, 1):
    print(f"  {i}. {f}")

# ============================================================================
# STEP 7: BUILD & TRAIN MODEL
# ============================================================================
print("\n" + "="*100)
print("[STEP 7] BUILD & TRAIN MODEL RANDOM FOREST")
print("="*100)

def build_model(X, y):
    """Membangun dan melatih model Random Forest (SAMA DENGAN app.py)."""
    le = LabelEncoder()
    # Hanya fit_transform jika ada lebih dari satu kelas
    if len(y.unique()) > 1:
        y_enc = le.fit_transform(y)
    else:
        y_enc = y 
        
    # Penanganan kasus ketika hanya ada satu kelas (stratify akan error)
    if len(y.unique()) > 1 and all(y.value_counts() > 1):
        X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
        
    # Cek jika X_train kosong
    if X_train.empty:
        return None, le, pd.DataFrame(), pd.DataFrame(), np.array([]), np.array([]), np.array([]), pd.DataFrame(), {}, {}
        
    # Random Forest dengan parameter yang di-tune untuk mencegah overfitting
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=15,
        min_samples_leaf=3,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    # Menggunakan seluruh data sebagai referensi
    X_ref = pd.concat([X_train, X_test]).reset_index(drop=True)
    
    # Hitung training metrics untuk setiap jumlah pohon (untuk visualisasi learning curves)
    train_scores = []
    test_scores = []
    tree_counts = []
    
    # Range disesuaikan dengan n_estimators (150 pohon)
    for n_trees in range(10, 151, 10):
        # Evaluasi dengan n_trees pertama menggunakan cumulative probability voting
        y_pred_train_prob = np.zeros((len(y_train), len(le.classes_)))
        y_pred_test_prob = np.zeros((len(y_test), len(le.classes_)))
        
        # Aggregate predictions dari n_trees pertama
        for estimator in model.estimators_[:n_trees]:
            y_pred_train_prob += estimator.predict_proba(X_train)
            y_pred_test_prob += estimator.predict_proba(X_test)
        
        # Majority voting - ambil kelas dengan probabilitas tertinggi
        y_pred_train_final = np.argmax(y_pred_train_prob, axis=1)
        y_pred_test_final = np.argmax(y_pred_test_prob, axis=1)
        
        # Hitung akurasi
        train_acc = np.mean(y_pred_train_final == y_train)
        test_acc = np.mean(y_pred_test_final == y_test)
        
        train_scores.append(train_acc)
        test_scores.append(test_acc)
        tree_counts.append(n_trees)
    
    training_metrics = {
        'tree_counts': tree_counts,
        'train_scores': train_scores,
        'test_scores': test_scores
    }
    
    oob_scores = {'n_estimators': [10, 50, 100, 150, 200]}
    
    return model, le, X_train, X_test, y_train, y_test, y_pred, X_ref, training_metrics, oob_scores

print("\n=== TRAINING MODEL (MENGGUNAKAN LOGIC DARI app.py) ===")
model_motor, le_motor, X_train_m, X_test_m, y_train_m, y_test_m, y_pred_m, X_ref_m, metrics_m, oob_m = build_model(
    df_clean[fitur_motor], df_clean['Class_Motor']
)
model_mobil, le_mobil, X_train_c, X_test_c, y_train_c, y_test_c, y_pred_c, X_ref_c, metrics_c, oob_c = build_model(
    df_clean[fitur_mobil], df_clean['Class_Mobil']
)

print(f"\n[Motor] Split Data:")
print(f"  Total Data: {len(df_clean)} | Training: {len(X_train_m)} | Testing: {len(X_test_m)}")
print(f"✓ Model Motor training selesai!")

print(f"\n[Mobil] Split Data:")
print(f"  Total Data: {len(df_clean)} | Training: {len(X_train_c)} | Testing: {len(X_test_c)}")
print(f"✓ Model Mobil training selesai!")

# ============================================================================
# STEP 8: EVALUASI MODEL
# ============================================================================
print("\n" + "="*100)
print("[STEP 8] EVALUASI MODEL")
print("="*100)

def print_evaluation(model, X_train, X_test, y_train, y_test, le, title, training_metrics=None):
    """Evaluasi dan print hasil model (menggunakan training_metrics dari build_model)."""
    # Jika ada training_metrics (dari build_model), gunakan untuk 150 trees
    if training_metrics is not None:
        train_acc = training_metrics['train_scores'][-1]  # Akurasi untuk 150 trees
        test_acc = training_metrics['test_scores'][-1]
        y_pred_test = model.predict(X_test)
    else:
        # Fallback jika tidak ada training_metrics
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        train_acc = accuracy_score(y_train, y_pred_train)
        test_acc = accuracy_score(y_test, y_pred_test)
    
    gap = train_acc - test_acc
    
    print(f"\n{'='*60} {title} {'='*60}")
    print(f"Akurasi Training: {train_acc:.4f} ({train_acc*100:.2f}%)")
    print(f"Akurasi Testing : {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"Overfitting Gap : {gap:.4f} ({gap*100:.2f}%)")
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred_test, target_names=le.classes_, zero_division=0))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred_test)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=le.classes_, yticklabels=le.classes_
    )
    plt.title(f'Confusion Matrix - Random Forest ({title})')
    plt.xlabel('Prediksi')
    plt.ylabel('Aktual')
    plt.tight_layout()
    plt.show()

print_evaluation(model_motor, X_train_m, X_test_m, y_train_m, y_test_m, le_motor, "Motor", metrics_m)
print_evaluation(model_mobil, X_train_c, X_test_c, y_train_c, y_test_c, le_mobil, "Mobil", metrics_c)

# ============================================================================
# STEP 9: FEATURE IMPORTANCE
# ============================================================================
print("\n" + "="*100)
print("[STEP 9] FEATURE IMPORTANCE")
print("="*100)

def plot_feature_importance(model, fitur, title):
    """Plot feature importance."""
    importance = pd.DataFrame({
        'Fitur': fitur, 
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    print(f"\n{title}:")
    print(importance.to_string(index=False))
    
    plt.figure(figsize=(10, 6))
    sns.barplot(y='Fitur', x='Importance', data=importance, palette='viridis')
    plt.title(title)
    plt.tight_layout()
    plt.show()

plot_feature_importance(model_motor, fitur_motor, "Feature Importance - Motor")
plot_feature_importance(model_mobil, fitur_mobil, "Feature Importance - Mobil")

# ============================================================================
# STEP 10: VISUALISASI DECISION TREE
# ============================================================================
print("\n" + "="*100)
print("[STEP 10] VISUALISASI DECISION TREE")
print("="*100)

print("\nMembuat visualisasi tree pertama dari 150 trees...")

plt.figure(figsize=(25, 15))
plot_tree(
    model_motor.estimators_[0],
    feature_names=fitur_motor,
    class_names=le_motor.classes_,
    filled=True, rounded=True, fontsize=10
)
plt.title("Visualisasi Salah Satu Pohon Keputusan (Motor) dari 150 Trees", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('motor_decision_tree.png', dpi=300, bbox_inches='tight')
print("✓ Disimpan: motor_decision_tree.png")
plt.show()

plt.figure(figsize=(25, 15))
plot_tree(
    model_mobil.estimators_[0],
    feature_names=fitur_mobil,
    class_names=le_mobil.classes_,
    filled=True, rounded=True, fontsize=10
)
plt.title("Visualisasi Salah Satu Pohon Keputusan (Mobil) dari 150 Trees", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('mobil_decision_tree.png', dpi=300, bbox_inches='tight')
print("✓ Disimpan: mobil_decision_tree.png")
plt.show()

# ============================================================================
# STEP 11: REKOMENDASI TARIF PROGRESIF
# ============================================================================
print("\n" + "="*100)
print("[STEP 11] PEMBENTUKAN TABEL REKOMENDASI KEBIJAKAN TARIF PROGRESIF")
print("="*100)

# Prediksi Motor
y_pred_m_enc = model_motor.predict(df_clean[fitur_motor])
df_clean['Klasifikasi Potensi (Motor)'] = le_motor.inverse_transform(y_pred_m_enc)
df_clean['Rekomendasi Tarif Motor'] = df_clean['Klasifikasi Potensi (Motor)'].apply(
    lambda x: f"Rp{tarif_mapping['Motor'][x]:,} / jam"
)

# Prediksi Mobil
y_pred_c_enc = model_mobil.predict(df_clean[fitur_mobil])
df_clean['Klasifikasi Potensi (Mobil)'] = le_mobil.inverse_transform(y_pred_c_enc)
df_clean['Rekomendasi Tarif Mobil'] = df_clean['Klasifikasi Potensi (Mobil)'].apply(
    lambda x: f"Rp{tarif_mapping['Mobil'][x]:,} / jam"
)

kolom_output = [
    'Titik',
    'Latitude',
    'Longitude',
    'Klasifikasi Potensi (Motor)',
    'Klasifikasi Potensi (Mobil)',
    'Rekomendasi Tarif Motor',
    'Rekomendasi Tarif Mobil'
]

df_rekomendasi = df_clean[kolom_output].copy()

print("\n=== RINGKASAN 10 BARIS PERTAMA REKOMENDASI TARIF ===")
print(df_rekomendasi.head(10).to_string())

# Simpan ke Excel
df_rekomendasi.to_excel("Tabel_Rekomendasi_Tarif_Parkir.xlsx", index=False)
print("\n✓ Hasil disimpan ke: Tabel_Rekomendasi_Tarif_Parkir.xlsx")

# ============================================================================
# STEP 11A: ANALISIS SPASIAL DENGAN FOLIUM MAP
# ============================================================================
print("\n" + "="*100)
print("[STEP 11A] ANALISIS SPASIAL DENGAN PETA INTERAKTIF (FOLIUM)")
print("="*100)

print("\n📍 Membuat peta interaktif dengan folium...")

# Hitung pusat peta berdasarkan koordinat
map_center = [df_clean['Latitude'].mean(), df_clean['Longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=13, tiles='OpenStreetMap')

# Tambahkan TileLayer tambahan
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    name='Esri Satellite',
    attr='Esri',
    overlay=False
).add_to(m)

# Warna untuk setiap kategori
color_mapping = {
    'Rendah': '#FFA500',   # Orange
    'Sedang': '#FFD700',   # Gold
    'Tinggi': '#FF6347'    # Tomato Red
}

# Tambahkan marker untuk setiap titik parkir
fg_motor = folium.FeatureGroup(name='Motor (Potensi Tarif)', show=True)
fg_mobil = folium.FeatureGroup(name='Mobil (Potensi Tarif)', show=True)

for index, row in df_clean.iterrows():
    titik = row['Titik']
    lat, lon = row['Latitude'], row['Longitude']
    motor_class = row['Klasifikasi Potensi (Motor)']
    mobil_class = row['Klasifikasi Potensi (Mobil)']
    motor_tarif = tarif_mapping['Motor'].get(motor_class, 0)
    mobil_tarif = tarif_mapping['Mobil'].get(mobil_class, 0)
    
    # Popup untuk Motor
    popup_motor = f"""
    <div style="font-size:12px; font-family:Arial;">
        <b>{titik}</b><br>
        <hr style="margin:5px 0;">
        <b>Motor</b><br>
        Potensi: {motor_class.upper()}<br>
        Tarif Dasar: Rp{motor_tarif:,.0f}/jam
    </div>
    """
    
    # Popup untuk Mobil
    popup_mobil = f"""
    <div style="font-size:12px; font-family:Arial;">
        <b>{titik}</b><br>
        <hr style="margin:5px 0;">
        <b>Mobil</b><br>
        Potensi: {mobil_class.upper()}<br>
        Tarif Dasar: Rp{mobil_tarif:,.0f}/jam
    </div>
    """
    
    # Marker untuk Motor
    folium.CircleMarker(
        location=[lat, lon],
        radius=7,
        color=color_mapping.get(motor_class, '#808080'),
        fill=True,
        fill_color=color_mapping.get(motor_class, '#808080'),
        fill_opacity=0.8,
        popup=folium.Popup(popup_motor, max_width=300),
        tooltip=f"{titik} (Motor: {motor_class})"
    ).add_to(fg_motor)
    
    # Marker untuk Mobil
    folium.CircleMarker(
        location=[lat, lon],
        radius=7,
        color=color_mapping.get(mobil_class, '#808080'),
        fill=True,
        fill_color=color_mapping.get(mobil_class, '#808080'),
        fill_opacity=0.8,
        popup=folium.Popup(popup_mobil, max_width=300),
        tooltip=f"{titik} (Mobil: {mobil_class})"
    ).add_to(fg_mobil)

fg_motor.add_to(m)
fg_mobil.add_to(m)

# Tambahkan layer control
folium.LayerControl(collapsed=False).add_to(m)

# Tambahkan legenda
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; right: 50px; width: 200px; height: 150px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
     padding: 10px; border-radius: 5px;">
     
<p style="margin:0;"><b>Legenda Potensi Tarif</b></p>
<hr style="margin:5px 0;">
<p style="margin:5px 0;"><i class="fa fa-circle" style="color:#FFA500"></i> Rendah</p>
<p style="margin:5px 0;"><i class="fa fa-circle" style="color:#FFD700"></i> Sedang</p>
<p style="margin:5px 0;"><i class="fa fa-circle" style="color:#FF6347"></i> Tinggi</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Simpan map
map_output = "peta_potensi_tarif_parkir.html"
m.save(map_output)
print(f"✓ Peta interaktif disimpan ke: {map_output}")
print(f"✓ Pusat Peta: [{map_center[0]:.4f}, {map_center[1]:.4f}]")
print(f"✓ Total lokasi parkir: {len(df_clean)}")

# ============================================================================
# STEP 12: SIMULASI PREDIKSI INTERAKTIF
# ============================================================================
print("\n" + "="*100)
print("[STEP 12] SIMULASI PREDIKSI INTERAKTIF DENGAN INPUTAN MANUAL")
print("="*100)

def simulasi_prediksi_interaktif():
    """Fungsi untuk simulasi prediksi dengan inputan user."""
    simulasi_count = 0
    
    while True:
        simulasi_count += 1
        print(f"\n{'='*100}")
        print(f"SIMULASI #{simulasi_count}")
        print(f"{'='*100}")
        
        # Input untuk jenis kendaraan
        print("\n[1] PILIH JENIS KENDARAAN:")
        print("  1 = Motor")
        print("  2 = Mobil")
        
        try:
            jenis_choice = int(input("\nPilih jenis (1 atau 2): ").strip())
            if jenis_choice == 1:
                jenis = 'Motor'
                model = model_motor
                le = le_motor
                fitur = fitur_motor
                X_train = X_train_m
            elif jenis_choice == 2:
                jenis = 'Mobil'
                model = model_mobil
                le = le_mobil
                fitur = fitur_mobil
                X_train = X_train_c
            else:
                print("❌ Input tidak valid! Silakan pilih 1 atau 2.")
                continue
        except (ValueError, KeyError):
            print("❌ Input tidak valid! Silakan masukkan angka 1 atau 2.")
            continue
        
        # Input untuk tipe hari
        print("\n[2] PILIH TIPE HARI:")
        print("  1 = Weekday (Hari Kerja)")
        print("  2 = Weekend (Akhir Pekan)")
        
        try:
            hari_choice = int(input("\nPilih hari (1 atau 2): ").strip())
            if hari_choice == 1:
                hari = 'Weekday'
            elif hari_choice == 2:
                hari = 'Weekend'
            else:
                print("❌ Input tidak valid! Silakan pilih 1 atau 2.")
                continue
        except ValueError:
            print("❌ Input tidak valid! Silakan masukkan angka 1 atau 2.")
            continue
        
        # Input jumlah kendaraan
        print(f"\n[3] MASUKKAN JUMLAH {jenis.upper()} {hari.upper()}:")
        try:
            jumlah_weekday = float(input(f"  Jumlah {jenis} Weekday: ").strip())
            jumlah_weekend = float(input(f"  Jumlah {jenis} Weekend: ").strip())
            
            if jumlah_weekday < 0 or jumlah_weekend < 0:
                print("❌ Jumlah kendaraan tidak boleh negatif!")
                continue
        except ValueError:
            print("❌ Input tidak valid! Silakan masukkan angka.")
            continue
        
        # Input jam
        print(f"\n[4] MASUKKAN JAM PUNCAK (Format Desimal, contoh: 17.5 untuk 17:30):")
        try:
            jam_input = float(input(f"  Jam Puncak {jenis} {hari}: ").strip())
            
            if jam_input < 0 or jam_input > 24:
                print("❌ Jam harus antara 0-24!")
                continue
            
            kategori_jam = kategori_jam_otomatis(jam_input)
        except ValueError:
            print("❌ Input tidak valid! Silakan masukkan angka desimal.")
            continue
        
        # Buat data baru untuk prediksi
        try:
            data_baru = pd.DataFrame([X_train.mean()], columns=X_train.columns)
            data_baru[f'Jumlah {jenis} Weekday'] = jumlah_weekday
            data_baru[f'Jumlah {jenis} Weekend'] = jumlah_weekend
            
            # Set kolom jam yang sesuai dengan kategori
            kolom_jam_input = f'Jam {kategori_jam} {jenis} {hari}'
            if kolom_jam_input in data_baru.columns:
                data_baru[kolom_jam_input] = jam_input
            
            # Prediksi
            pred_encoded = model.predict(data_baru)[0]
            pred_class = le.inverse_transform([pred_encoded])[0]
            proba = model.predict_proba(data_baru)[0]
            confidence = proba[pred_encoded]
            
            # Hitung tarif progresif
            tarif_base = tarif_mapping[jenis][pred_class]
            tarif_progresif = calculate_progresif_tarif(jenis, pred_class, jam_input)
            
            # Tampilkan hasil
            print(f"\n{'='*100}")
            print(f"HASIL SIMULASI #{simulasi_count}")
            print(f"{'='*100}")
            print(f"\n📊 INPUT:")
            print(f"  • Jenis Kendaraan    : {jenis}")
            print(f"  • Tipe Hari          : {hari}")
            print(f"  • Jumlah {jenis} Weekday    : {jumlah_weekday:.0f} unit")
            print(f"  • Jumlah {jenis} Weekend    : {jumlah_weekend:.0f} unit")
            print(f"  • Jam Puncak         : {jam_input:.2f} (Kategori: {kategori_jam})")
            
            print(f"\n🎯 PREDIKSI:")
            print(f"  • Klasifikasi Potensi: {pred_class.upper()}")
            print(f"  • Confidence/Keyakinan: {confidence*100:.2f}%")
            print(f"  • Probabilitas Kelas:")
            for cls, prob in zip(le.classes_, proba):
                print(f"      - {cls.capitalize()}: {prob*100:.2f}%")
            
            print(f"\n💰 REKOMENDASI TARIF:")
            print(f"  • Tarif Dasar        : Rp{tarif_base:,.0f} / jam")
            print(f"  • Tarif Progresif    : Rp{tarif_progresif:,.0f} / jam")
            print(f"  • Selisih            : Rp{tarif_progresif - tarif_base:,.0f} / jam")
        
        except Exception as e:
            print(f"❌ Error saat prediksi: {e}")
            continue
        
        # Tanya apakah user ingin simulasi lagi
        print(f"\n{'='*100}")
        lanjut = input("Apakah Anda ingin simulasi lagi? (y/n): ").strip().lower()
        if lanjut != 'y':
            print(f"\n✓ Total simulasi yang dilakukan: {simulasi_count}")
            break

print("\n=== MULAI SIMULASI PREDIKSI INTERAKTIF ===")
print("Anda dapat melakukan simulasi dengan berbagai kombinasi parameter.")
print("Sistem akan memandu Anda untuk input setiap parameter.\n")

simulasi_prediksi_interaktif()

print(f"\n{'='*100}")
print("TERIMA KASIH TELAH MENGGUNAKAN SIMULASI TARIF PARKIR PROGRESIF!")
print(f"{'='*100}")

# ============================================================================
# STEP 13: RINGKASAN FINAL
# ============================================================================
print("\n" + "="*100)
print("[STEP 13] RINGKASAN FINAL")
print("="*100)

summary = pd.DataFrame({
    'Metrik': [
        'Total Data',
        'Data Training',
        'Data Testing',
        'Jumlah Fitur',
        'Akurasi Training',
        'Akurasi Testing',
        'Overfitting Gap',
        'N Estimators',
        'Max Depth',
        'Min Samples Leaf'
    ],
    'Motor': [
        len(df_clean),
        len(X_train_m),
        len(X_test_m),
        len(fitur_motor),
        f"{accuracy_score(y_train_m, model_motor.predict(X_train_m))*100:.2f}%",
        f"{accuracy_score(y_test_m, model_motor.predict(X_test_m))*100:.2f}%",
        f"{(accuracy_score(y_train_m, model_motor.predict(X_train_m)) - accuracy_score(y_test_m, model_motor.predict(X_test_m)))*100:.2f}%",
        '150',
        '15',
        '3'
    ],
    'Mobil': [
        len(df_clean),
        len(X_train_c),
        len(X_test_c),
        len(fitur_mobil),
        f"{accuracy_score(y_train_c, model_mobil.predict(X_train_c))*100:.2f}%",
        f"{accuracy_score(y_test_c, model_mobil.predict(X_test_c))*100:.2f}%",
        f"{(accuracy_score(y_train_c, model_mobil.predict(X_train_c)) - accuracy_score(y_test_c, model_mobil.predict(X_test_c)))*100:.2f}%",
        '150',
        '15',
        '3'
    ]
})

print("\n" + summary.to_string(index=False))

print("\n" + "="*100)
print("✓✓✓ SIMULASI LENGKAP SELESAI ✓✓✓")
print("="*100)

print(f"""
FILE YANG DIHASILKAN:
1. Tabel_Rekomendasi_Tarif_Parkir.xlsx - Tabel rekomendasi untuk semua lokasi
2. motor_decision_tree.png - Visualisasi tree Motor
3. mobil_decision_tree.png - Visualisasi tree Mobil

RINGKASAN PROSES:
1. Load data dari DataParkir_Fix.xlsx
2. Cleaning & preprocessing data
3. Feature engineering (konversi jam, menghitung pendapatan)
4. Klasifikasi target (Rendah/Sedang/Tinggi) menggunakan qcut
5. Split data 80:20
6. Training Random Forest (150 trees, max_depth=15)
7. Evaluasi dengan confusion matrix & classification report
8. Analisis feature importance
9. Visualisasi decision tree
10. Membentuk tabel rekomendasi tarif progresif
11. Simulasi prediksi pada sampel baru
""")
