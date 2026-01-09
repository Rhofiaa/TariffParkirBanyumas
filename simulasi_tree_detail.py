"""
SIMULASI LENGKAP DENGAN VISUALISASI DECISION TREE
Script ini menunjukkan setiap tahap + cara melihat struktur tree
Jalankan: python simulasi_tree_detail.py
"""

import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree, export_text
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

print("="*80)
print("SIMULASI DECISION TREE STRUCTURE - MOTOR & MOBIL")
print("="*80)

# ============================================================================
# 1. LOAD & PREPROCESS DATA
# ============================================================================
print("\n[STEP 1] Load & Preprocess Data")
print("-" * 80)

def parse_time_to_decimal(time_str):
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

try:
    df = pd.read_excel('DataParkir_Fix.xlsx')
    print(f"✓ Data loaded: {len(df)} rows, {len(df.columns)} columns")
except FileNotFoundError:
    print("⚠ Using dummy data...")
    df = pd.DataFrame({
        'Jam': ['08.00-10.00', '10.00-12.00', '12.00-14.00'] * 20,
        'Jumlah Motor Weekday': np.random.randint(50, 200, 60),
        'Jumlah Motor Weekend': np.random.randint(30, 150, 60),
        'Jumlah Mobil Weekday': np.random.randint(30, 150, 60),
        'Jumlah Mobil Weekend': np.random.randint(20, 100, 60),
        'Class_Motor': np.random.choice(['Rendah', 'Sedang', 'Tinggi'], 60),
        'Class_Mobil': np.random.choice(['Rendah', 'Sedang', 'Tinggi'], 60),
    })

# Preprocessing
df['Jam_Desimal'] = df['Jam'].apply(konversi_jam)
df_clean = df.dropna(subset=['Class_Motor', 'Class_Mobil', 'Jam_Desimal'])

feature_cols = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend', 
                'Jumlah Mobil Weekday', 'Jumlah Mobil Weekend', 'Jam_Desimal']
X = df_clean[feature_cols].copy()

print(f"✓ Data preprocessed: {len(df_clean)} rows")
print(f"✓ Features: {feature_cols}")

# ============================================================================
# 2. TRAINING MODEL MOTOR
# ============================================================================
print("\n[STEP 2] Training Motor Model")
print("-" * 80)

y_motor = df_clean['Class_Motor']
le_motor = LabelEncoder()
y_motor_encoded = le_motor.fit_transform(y_motor)

X_train_motor, X_test_motor, y_train_motor, y_test_motor = train_test_split(
    X, y_motor_encoded, test_size=0.2, random_state=42, stratify=y_motor_encoded
)

model_motor = RandomForestClassifier(
    n_estimators=150, max_depth=15, min_samples_leaf=3, random_state=42
)
model_motor.fit(X_train_motor, y_train_motor)

acc_motor = accuracy_score(y_test_motor, model_motor.predict(X_test_motor))
print(f"✓ Motor model trained")
print(f"  - Test Accuracy: {acc_motor*100:.2f}%")
print(f"  - Total trees: 150")
print(f"  - Max depth: 15")

# ============================================================================
# 3. VISUALISASI SATU TREE DARI MOTOR (TREE #0)
# ============================================================================
print("\n[STEP 3] Visualizing Motor Tree #0")
print("-" * 80)

fig, ax = plt.subplots(figsize=(25, 15))
plot_tree(
    model_motor.estimators_[0],
    feature_names=feature_cols,
    class_names=le_motor.classes_,
    filled=True,
    ax=ax,
    fontsize=10
)
plt.title("Decision Tree #0 - Motor Vehicle Tariff Prediction\n(1 dari 150 trees dalam Random Forest)", 
          fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('motor_tree_0.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved to: motor_tree_0.png (25x15 inches)")
print(f"  - Shows one complete decision tree structure")
print(f"  - Each node shows split condition and class distribution")

# ============================================================================
# 4. PRINT TEXT REPRESENTATION MOTOR TREE
# ============================================================================
print("\n[STEP 4] Text Representation of Motor Tree #0")
print("-" * 80)

tree_rules_motor = export_text(model_motor.estimators_[0], feature_names=feature_cols)
print("\nMOTOR TREE STRUCTURE (First 50 lines):")
print(tree_rules_motor[:2000])  # Print first 2000 chars

# Save to file
with open('motor_tree_rules.txt', 'w') as f:
    f.write(tree_rules_motor)
print(f"\n✓ Full tree rules saved to: motor_tree_rules.txt")

# ============================================================================
# 5. TRAINING MODEL MOBIL
# ============================================================================
print("\n[STEP 5] Training Mobil Model")
print("-" * 80)

y_mobil = df_clean['Class_Mobil']
le_mobil = LabelEncoder()
y_mobil_encoded = le_mobil.fit_transform(y_mobil)

X_train_mobil, X_test_mobil, y_train_mobil, y_test_mobil = train_test_split(
    X, y_mobil_encoded, test_size=0.2, random_state=42, stratify=y_mobil_encoded
)

model_mobil = RandomForestClassifier(
    n_estimators=150, max_depth=15, min_samples_leaf=3, random_state=42
)
model_mobil.fit(X_train_mobil, y_train_mobil)

acc_mobil = accuracy_score(y_test_mobil, model_mobil.predict(X_test_mobil))
print(f"✓ Mobil model trained")
print(f"  - Test Accuracy: {acc_mobil*100:.2f}%")
print(f"  - Total trees: 150")
print(f"  - Max depth: 15")

# ============================================================================
# 6. VISUALISASI SATU TREE DARI MOBIL (TREE #0)
# ============================================================================
print("\n[STEP 6] Visualizing Mobil Tree #0")
print("-" * 80)

fig, ax = plt.subplots(figsize=(25, 15))
plot_tree(
    model_mobil.estimators_[0],
    feature_names=feature_cols,
    class_names=le_mobil.classes_,
    filled=True,
    ax=ax,
    fontsize=10
)
plt.title("Decision Tree #0 - Car Vehicle Tariff Prediction\n(1 dari 150 trees dalam Random Forest)", 
          fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('mobil_tree_0.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved to: mobil_tree_0.png (25x15 inches)")

# ============================================================================
# 7. PRINT TEXT REPRESENTATION MOBIL TREE
# ============================================================================
print("\n[STEP 7] Text Representation of Mobil Tree #0")
print("-" * 80)

tree_rules_mobil = export_text(model_mobil.estimators_[0], feature_names=feature_cols)
print("\nMOBIL TREE STRUCTURE (First 50 lines):")
print(tree_rules_mobil[:2000])

with open('mobil_tree_rules.txt', 'w') as f:
    f.write(tree_rules_mobil)
print(f"\n✓ Full tree rules saved to: mobil_tree_rules.txt")

# ============================================================================
# 8. PENJELASAN STRUKTUR TREE
# ============================================================================
print("\n[STEP 8] Understanding Tree Structure")
print("-" * 80)

print("""
CARA MEMBACA DECISION TREE:

1. ROOT NODE (Atas):
   Kondisi pertama: "Feature <= Threshold?"
   Contoh: "Jam Sepi Motor Weekday <= 17.25?"
   
   - Jika TRUE (sampel <= 17.25): Ambil KIRI
   - Jika FALSE (sampel > 17.25): Ambil KANAN

2. SETIAP NODE MENAMPILKAN:
   - gini: Impuritas Gini (semakin rendah = semakin pure)
   - samples: Jumlah sampel di node ini
   - value: [jumlah kelas Rendah, Sedang, Tinggi]
   - class: Prediksi kelas untuk node ini

3. WARNA BACKGROUND:
   - Lebih gelap = class lebih dominan
   - Lebih terang = class lebih balance

4. LEAF NODE (Bawah):
   Tidak ada pertanyaan lagi
   Langsung ke prediksi kelas

CONTOH TRACE PATH:
Input: Jam_Desimal = 16.5 (pukul 16:30)

Node 1: Jam Sepi Motor Weekday <= 17.25? 
        → YES (16.5 < 17.25) → Go LEFT

Node 2: Jumlah Motor Weekday <= 150?
        → (tergantung input) → Go LEFT/RIGHT

Node 3: Kategori Jam == Ramai?
        → (tergantung logic) → Go LEFT/RIGHT

...

Leaf: Prediksi = "Tinggi" atau "Sedang" atau "Rendah"
""")

# ============================================================================
# 9. ANALISIS SPLIT POINTS
# ============================================================================
print("\n[STEP 9] Split Points Analysis")
print("-" * 80)

print(f"\nRoOT NODE SPLIT THRESHOLD (Motor Tree #0):")
tree_motor = model_motor.estimators_[0]
print(f"  - Feature: {feature_cols[tree_motor.feature[0]]}")
print(f"  - Threshold: {tree_motor.threshold[0]:.4f}")
print(f"  - Gini: {tree_motor.impurity[0]:.4f}")
print(f"  - Samples: {tree_motor.n_node_samples[0]}")

print(f"\nROOT NODE SPLIT THRESHOLD (Mobil Tree #0):")
tree_mobil = model_mobil.estimators_[0]
print(f"  - Feature: {feature_cols[tree_mobil.feature[0]]}")
print(f"  - Threshold: {tree_mobil.threshold[0]:.4f}")
print(f"  - Gini: {tree_mobil.impurity[0]:.4f}")
print(f"  - Samples: {tree_mobil.n_node_samples[0]}")

# ============================================================================
# 10. CONTOH PREDIKSI STEP-BY-STEP
# ============================================================================
print("\n[STEP 10] Prediksi Step-by-Step")
print("-" * 80)

sample = pd.DataFrame({
    'Jumlah Motor Weekday': [120],
    'Jumlah Motor Weekend': [100],
    'Jumlah Mobil Weekday': [80],
    'Jumlah Mobil Weekend': [60],
    'Jam_Desimal': [17.25]  # 17:15
})

print(f"\nSample Input: {sample.to_dict('records')[0]}")

pred_motor = model_motor.predict(sample)[0]
proba_motor = model_motor.predict_proba(sample)[0]

pred_mobil = model_mobil.predict(sample)[0]
proba_mobil = model_mobil.predict_proba(sample)[0]

print(f"\n✓ Prediksi Motor:")
print(f"  Kelas: {le_motor.classes_[pred_motor]}")
for i, kelas in enumerate(le_motor.classes_):
    print(f"  {kelas}: {proba_motor[i]*100:.2f}%")

print(f"\n✓ Prediksi Mobil:")
print(f"  Kelas: {le_mobil.classes_[pred_mobil]}")
for i, kelas in enumerate(le_mobil.classes_):
    print(f"  {kelas}: {proba_mobil[i]*100:.2f}%")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("SIMULASI SELESAI!")
print("="*80)

print("\nFile yang dihasilkan:")
print("1. motor_tree_0.png - Visualisasi decision tree Motor")
print("2. motor_tree_rules.txt - Text rules Motor tree")
print("3. mobil_tree_0.png - Visualisasi decision tree Mobil")
print("4. mobil_tree_rules.txt - Text rules Mobil tree")

print("\nDari 150 trees dalam Random Forest:")
print(f"- Motor: Tiap tree punya split points berbeda")
print(f"- Mobil: Tiap tree punya split points berbeda")
print(f"- Final prediksi: Voting dari semua 150 trees")

print("\nUntuk melihat lebih banyak trees:")
print("  - Ubah model_motor.estimators_[0] ke [1], [2], [3], dst")
print("  - Setiap tree berbeda karena training dengan bootstrap sample berbeda")
