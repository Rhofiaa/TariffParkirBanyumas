#!/usr/bin/env python3
"""
Script untuk menambahkan konten lengkap ke Jupyter Notebook
"""

import json

# Load notebook yang sudah ada
with open('Analisis_Tarif_Parkir_Lengkap.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Function untuk insert cells di posisi tertentu
def insert_cell_at(cells_list, position, new_cell):
    cells_list.insert(position, new_cell)

# Find index of section header
def find_section_index(notebook, section_name):
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown' and section_name in str(cell['source']):
            return i
    return -1

# Cell untuk EDA
eda_code = """print('📊 VISUALISASI DISTRIBUSI PENDAPATAN')
print('='*60)

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

plt.tight_layout()
plt.show()

print('\\n✅ Visualisasi distribusi selesai!')"""

# Cell untuk Train-Test Split & Model Training
training_code = """print('🤖 TAHAP 1: PREPARE FEATURES & TARGET')
print('='*60)

# Fitur untuk Model
fitur_motor = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend'] + [c for c in jam_cols if 'Motor' in c]
fitur_mobil = ['Jumlah Mobil Weekday', 'Jumlah Mobil Weekend'] + [c for c in jam_cols if 'Mobil' in c]

print(f'✅ Fitur Motor: {fitur_motor}')
print(f'✅ Fitur Mobil: {fitur_mobil}')

# Prepare X dan y
X_motor = df[fitur_motor]
y_motor = df['Class_Motor']

X_mobil = df[fitur_mobil]
y_mobil = df['Class_Mobil']

print(f'\\n✅ Data Shape:')
print(f'   Motor - X: {X_motor.shape}, y: {y_motor.shape}')
print(f'   Mobil - X: {X_mobil.shape}, y: {y_mobil.shape}')"""

training_code2 = """print('\\n🔄 TAHAP 2: TRAIN-TEST SPLIT (80-20)')
print('='*60)

# Split data Motor
X_train_motor, X_test_motor, y_train_motor, y_test_motor = train_test_split(
    X_motor, y_motor, test_size=0.2, random_state=42, stratify=y_motor if y_motor.nunique() > 1 else None
)

# Split data Mobil
X_train_mobil, X_test_mobil, y_train_mobil, y_test_mobil = train_test_split(
    X_mobil, y_mobil, test_size=0.2, random_state=42, stratify=y_mobil if y_mobil.nunique() > 1 else None
)

print(f'✅ Motor - Training: {X_train_motor.shape}, Testing: {X_test_motor.shape}')
print(f'✅ Mobil - Training: {X_train_mobil.shape}, Testing: {X_test_mobil.shape}')

# Visualisasi train-test split
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

train_test_motor = [len(X_train_motor), len(X_test_motor)]
train_test_mobil = [len(X_train_mobil), len(X_test_mobil)]

axes[0].pie(train_test_motor, labels=['Training (80%)', 'Testing (20%)'], autopct='%1.1f%%', colors=['#2E86AB', '#A23B72'])
axes[0].set_title('Train-Test Split Motor')

axes[1].pie(train_test_mobil, labels=['Training (80%)', 'Testing (20%)'], autopct='%1.1f%%', colors=['#2E86AB', '#A23B72'])
axes[1].set_title('Train-Test Split Mobil')

plt.tight_layout()
plt.show()"""

training_code3 = """print('\\n🌳 TAHAP 3: TRAIN RANDOM FOREST MODELS')
print('='*60)

# Encode target labels
le_motor = LabelEncoder()
y_train_motor_enc = le_motor.fit_transform(y_train_motor)
y_test_motor_enc = le_motor.transform(y_test_motor)

le_mobil = LabelEncoder()
y_train_mobil_enc = le_mobil.fit_transform(y_train_mobil)
y_test_mobil_enc = le_mobil.transform(y_test_mobil)

# Train Random Forest Motor
print('\\nTraining Motor model...')
model_motor = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)
model_motor.fit(X_train_motor, y_train_motor_enc)
y_pred_motor = model_motor.predict(X_test_motor)
acc_motor = accuracy_score(y_test_motor_enc, y_pred_motor)
print(f'✅ Motor Model - Accuracy: {acc_motor:.4f}')

# Train Random Forest Mobil
print('\\nTraining Mobil model...')
model_mobil = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)
model_mobil.fit(X_train_mobil, y_train_mobil_enc)
y_pred_mobil = model_mobil.predict(X_test_mobil)
acc_mobil = accuracy_score(y_test_mobil_enc, y_pred_mobil)
print(f'✅ Mobil Model - Accuracy: {acc_mobil:.4f}')

print('\\n✅ Model Training Selesai!')"""

# Cell untuk Model Evaluation
evaluation_code = """print('📊 CONFUSION MATRIX & CLASSIFICATION REPORT')
print('='*60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Confusion Matrix Motor
cm_motor = confusion_matrix(y_test_motor_enc, y_pred_motor)
sns.heatmap(cm_motor, annot=True, fmt='d', cmap='Blues', xticklabels=le_motor.classes_, yticklabels=le_motor.classes_, ax=axes[0])
axes[0].set_title('Confusion Matrix - Motor')
axes[0].set_ylabel('Actual')
axes[0].set_xlabel('Predicted')

# Confusion Matrix Mobil
cm_mobil = confusion_matrix(y_test_mobil_enc, y_pred_mobil)
sns.heatmap(cm_mobil, annot=True, fmt='d', cmap='Blues', xticklabels=le_mobil.classes_, yticklabels=le_mobil.classes_, ax=axes[1])
axes[1].set_title('Confusion Matrix - Mobil')
axes[1].set_ylabel('Actual')
axes[1].set_xlabel('Predicted')

plt.tight_layout()
plt.show()

print('\\n📋 CLASSIFICATION REPORT - MOTOR:')
print(classification_report(y_test_motor_enc, y_pred_motor, target_names=le_motor.classes_))

print('\\n📋 CLASSIFICATION REPORT - MOBIL:')
print(classification_report(y_test_mobil_enc, y_pred_mobil, target_names=le_mobil.classes_))"""

# Cell untuk Feature Importance
importance_code = """print('📊 FEATURE IMPORTANCE')
print('='*60)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Motor Feature Importance
importance_motor = pd.Series(model_motor.feature_importances_, index=fitur_motor).sort_values(ascending=False)
importance_motor.plot(kind='barh', ax=axes[0], color='#2E86AB')
axes[0].set_title('Feature Importance - Motor', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Importance Score')

# Mobil Feature Importance
importance_mobil = pd.Series(model_mobil.feature_importances_, index=fitur_mobil).sort_values(ascending=False)
importance_mobil.plot(kind='barh', ax=axes[1], color='#A23B72')
axes[1].set_title('Feature Importance - Mobil', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Importance Score')

plt.tight_layout()
plt.show()

print('\\n✅ Feature importance visualization complete!')"""

# Cell untuk Decision Tree Visualization
tree_code = """print('🌳 DECISION TREE VISUALIZATION')
print('='*60)

# Ambil pohon pertama dari Motor model
sample_tree_motor = model_motor.estimators_[0]

fig, ax = plt.subplots(figsize=(20, 10))
plot_tree(sample_tree_motor, feature_names=fitur_motor, class_names=le_motor.classes_, 
          filled=True, rounded=True, fontsize=8, ax=ax)
plt.title('Sample Decision Tree #1 - Motor Model (dari 150 pohon)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print('\\n✅ Decision tree visualization complete!')"""

# Cell untuk Spatial Analysis
spatial_code = """print('🗺️ SPATIAL ANALYSIS & MAPPING')
print('='*60)

# Prediksi untuk semua data
y_pred_motor_all = le_motor.inverse_transform(model_motor.predict(X_motor))
y_pred_mobil_all = le_mobil.inverse_transform(model_mobil.predict(X_mobil))

# Tambahkan prediksi ke df_spasial
df_spasial['Class_Motor_Pred'] = y_pred_motor_all
df_spasial['Class_Mobil_Pred'] = y_pred_mobil_all

# Buat peta
map_center = [df_spasial['Latitude'].mean(), df_spasial['Longitude'].mean()]
print(f'Map Center: {map_center}')

m = folium.Map(location=map_center, zoom_start=13, tiles='OpenStreetMap')

# Add markers
color_map = {'Rendah': 'red', 'Sedang': 'orange', 'Tinggi': 'green'}

for idx, row in df_spasial.iterrows():
    motor_color = color_map.get(row['Class_Motor_Pred'], 'gray')
    mobil_color = color_map.get(row['Class_Mobil_Pred'], 'gray')
    
    popup_text = f'''
    <b>{row['Titik']}</b><br>
    Motor: {row['Class_Motor_Pred']} (Rp{tarif_mapping['Motor'].get(row['Class_Motor_Pred'], 0):,})<br>
    Mobil: {row['Class_Mobil_Pred']} (Rp{tarif_mapping['Mobil'].get(row['Class_Mobil_Pred'], 0):,})
    '''
    
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6,
        popup=folium.Popup(popup_text, max_width=300),
        color=motor_color,
        fill=True,
        fillColor=motor_color,
        fillOpacity=0.8,
        tooltip=row['Titik']
    ).add_to(m)

folium.LayerControl().add_to(m)
print('✅ Peta berhasil dibuat!')
print('\\nPreview peta akan ditampilkan dibawah:')"
"""

# Tambahkan cells ke notebook
# Cari index untuk section "6️⃣"
idx_eda = find_section_index(notebook, "6️⃣")
if idx_eda > 0:
    notebook['cells'][idx_eda + 1]['source'] = eda_code.split('\n')

idx_training = find_section_index(notebook, "7️⃣")
if idx_training > 0:
    notebook['cells'][idx_training + 1]['source'] = training_code.split('\n')
    # Insert additional training cells
    notebook['cells'].insert(idx_training + 2, {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": training_code2.split('\n')
    })
    notebook['cells'].insert(idx_training + 3, {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": training_code3.split('\n')
    })

idx_eval = find_section_index(notebook, "8️⃣")
if idx_eval > 0:
    notebook['cells'][idx_eval + 1]['source'] = evaluation_code.split('\n')

idx_importance = find_section_index(notebook, "9️⃣")
if idx_importance > 0:
    notebook['cells'][idx_importance + 1]['source'] = importance_code.split('\n')

idx_tree = find_section_index(notebook, "🔟")
if idx_tree > 0:
    notebook['cells'][idx_tree + 1]['source'] = tree_code.split('\n')

idx_spatial = find_section_index(notebook, "1️⃣1️⃣")
if idx_spatial > 0:
    notebook['cells'][idx_spatial + 1]['source'] = spatial_code.split('\n')

# Save updated notebook
with open('Analisis_Tarif_Parkir_Lengkap.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("✅ Notebook berhasil diupdate dengan konten lengkap!")
