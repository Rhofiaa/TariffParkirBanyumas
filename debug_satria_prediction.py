import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_excel('DataParkir_Fix.xlsx')

# Preprocessing seperti di streamlit
pend_cols = ['Pendapatan Tarif Parkir Weekday Motor per tahun', 'Pendapatan Tarif Parkir Weekend Motor per tahun']
df[pend_cols] = df[pend_cols].apply(lambda x: pd.to_numeric(x, errors='coerce').fillna(0))

# Filter hanya yang punya koordinat
df = df.dropna(subset=['Titik', 'Latitude', 'Longitude'])

# Kolom fitur
jam_cols = [c for c in df.columns if 'Jam' in c and 'Motor' in c]
fitur_motor = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend'] + jam_cols

# === SIMULASI PIPELINE TRAINING ===
print("=== SIMULASI PIPELINE TRAINING ===\n")

# TAHAP 1: Split data
np.random.seed(42)
train_idx, test_idx = train_test_split(
    df.index, 
    test_size=0.2, 
    random_state=42
)

df_train = df.loc[train_idx].copy()
df_test = df.loc[test_idx].copy()

# TAHAP 2: Feature Engineering
df_train['Total_Pend'] = df_train[pend_cols[0]] + df_train[pend_cols[1]]
df_test['Total_Pend'] = df_test[pend_cols[0]] + df_test[pend_cols[1]]

# TAHAP 3: Labeling dari TRAIN
try:
    labels = pd.qcut(df_train['Total_Pend'], q=3, labels=['Rendah','Sedang','Tinggi'], duplicates='drop')
    quantiles = df_train['Total_Pend'].quantile([0.333, 0.666]).values
    
    print(f"Threshold dari TRAINING data:")
    print(f"  Rendah-Sedang: Rp{quantiles[0]:,.0f}")
    print(f"  Sedang-Tinggi: Rp{quantiles[1]:,.0f}")
    
    df_train['Class'] = labels
    df_test['Class'] = pd.cut(
        df_test['Total_Pend'], 
        bins=[-np.inf, quantiles[0], quantiles[1], np.inf],
        labels=['Rendah','Sedang','Tinggi']
    )
except Exception as e:
    print(f"Error labeling: {e}")
    exit()

# TAHAP 4: Imputasi
impute_values = {}
for col in fitur_motor:
    if df_train[col].isna().any():
        impute_values[col] = df_train[col].median()

df_train[fitur_motor] = df_train[fitur_motor].fillna(impute_values)
df_test[fitur_motor] = df_test[fitur_motor].fillna(impute_values)

# TAHAP 5: Training
le = LabelEncoder()
y_train = le.fit_transform(df_train['Class'])
y_test = le.transform(df_test['Class'])
X_train = df_train[fitur_motor]
X_test = df_test[fitur_motor]

model = RandomForestClassifier(n_estimators=150, max_depth=15, min_samples_leaf=3, random_state=42)
model.fit(X_train, y_train)

# === CEK TOKO SATRIA ===
print("\n=== CEK TOKO SATRIA ===\n")

# Cari Toko Satria di data asli
satria_idx = df[df['Titik'].str.contains('Satria', case=False, na=False)].index[0]
satria_data = df.loc[satria_idx]

print(f"Titik: {satria_data['Titik']}")
print(f"Total Pendapatan: Rp{satria_data['Pendapatan Tarif Parkir Weekday Motor per tahun'] + satria_data['Pendapatan Tarif Parkir Weekend Motor per tahun']:,.0f}")
print(f"Jumlah Motor Weekday: {satria_data['Jumlah Motor Weekday']}")
print(f"Jumlah Motor Weekend: {satria_data['Jumlah Motor Weekend']}")

# Cek apakah Toko Satria ada di train atau test
if satria_idx in train_idx:
    print("\n⚠️ Toko Satria ada di TRAINING set")
    satria_class_actual = df_train.loc[satria_idx, 'Class']
    print(f"Label Training: {satria_class_actual}")
elif satria_idx in test_idx:
    print("\n⚠️ Toko Satria ada di TEST set")
    satria_class_actual = df_test.loc[satria_idx, 'Class']
    print(f"Label Testing: {satria_class_actual}")

# Prediksi dengan model
X_satria = df.loc[[satria_idx], fitur_motor].fillna(impute_values)
pred = model.predict(X_satria)[0]
pred_class = le.inverse_transform([pred])[0]
proba = model.predict_proba(X_satria)[0]

print(f"\n=== PREDIKSI MODEL ===")
print(f"Prediksi: {pred_class}")
print(f"Probabilitas: {dict(zip(le.classes_, proba))}")

# Feature importance
importance = pd.Series(model.feature_importances_, index=fitur_motor).sort_values(ascending=False)
print(f"\nTop 5 Fitur Penting:")
for feat, imp in importance.head(5).items():
    val = X_satria[feat].values[0]
    print(f"  {feat}: {val:.2f} (importance: {imp:.4f})")
