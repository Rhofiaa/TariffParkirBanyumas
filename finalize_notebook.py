#!/usr/bin/env python3
"""
Script untuk menambahkan section Simulasi Interaktif dan Dashboard ke notebook
"""

import json

# Load notebook
with open('Analisis_Tarif_Parkir_Lengkap.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

def find_section_index(notebook, section_name):
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown' and section_name in str(cell['source']):
            return i
    return -1

# ==================== PROGRESSIVE TARIFF SECTION ====================
prog_tariff_code = """print('💰 PROGRESSIVE TARIFF CALCULATION')
print('='*60)

# Buat lookup table untuk tarif
tarif_df = []

for idx, row in df_spasial.iterrows():
    titik = row['Titik']
    class_motor = row['Class_Motor_Pred']
    class_mobil = row['Class_Mobil_Pred']
    
    # Tarif dasar
    tarif_motor_base = tarif_mapping['Motor'].get(class_motor, 0)
    tarif_mobil_base = tarif_mapping['Mobil'].get(class_mobil, 0)
    
    # Tarif progresif (contoh: jam 9+ dengan potensi tinggi)
    tarif_motor_prog = calculate_progresif_tarif('Motor', class_motor, 12.0)  # Jam 12 siang
    tarif_mobil_prog = calculate_progresif_tarif('Mobil', class_mobil, 12.0)
    
    tarif_df.append({
        'Titik': titik,
        'Kelas_Motor': class_motor,
        'Tarif_Motor_Base': tarif_motor_base,
        'Tarif_Motor_Peak': tarif_motor_prog,
        'Kelas_Mobil': class_mobil,
        'Tarif_Mobil_Base': tarif_mobil_base,
        'Tarif_Mobil_Peak': tarif_mobil_prog
    })

tarif_lookup = pd.DataFrame(tarif_df)

print('✅ Tarif Lookup Table:')
print(tarif_lookup.head(10))

# Visualisasi perbandingan tarif dasar vs progresif
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Motor
motor_dasar = tarif_lookup[tarif_lookup['Kelas_Motor'] == 'Tinggi']['Tarif_Motor_Base'].mean()
motor_peak = tarif_lookup[tarif_lookup['Kelas_Motor'] == 'Tinggi']['Tarif_Motor_Peak'].mean()

axes[0].bar(['Tarif Dasar', 'Tarif Peak (Jam 12)'], [motor_dasar, motor_peak], color=['#2E86AB', '#FF6B6B'])
axes[0].set_title('Perbandingan Tarif Motor (Kelas Tinggi)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Tarif (Rp)')
for i, v in enumerate([motor_dasar, motor_peak]):
    axes[0].text(i, v + 50, f'Rp{v:.0f}', ha='center', fontweight='bold')

# Mobil
mobil_dasar = tarif_lookup[tarif_lookup['Kelas_Mobil'] == 'Tinggi']['Tarif_Mobil_Base'].mean()
mobil_peak = tarif_lookup[tarif_lookup['Kelas_Mobil'] == 'Tinggi']['Tarif_Mobil_Peak'].mean()

axes[1].bar(['Tarif Dasar', 'Tarif Peak (Jam 12)'], [mobil_dasar, mobil_peak], color=['#2E86AB', '#FF6B6B'])
axes[1].set_title('Perbandingan Tarif Mobil (Kelas Tinggi)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Tarif (Rp)')
for i, v in enumerate([mobil_dasar, mobil_peak]):
    axes[1].text(i, v + 100, f'Rp{v:.0f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

print('\\n✅ Progressive tariff visualization complete!')"""

# ==================== INTERACTIVE PREDICTION SECTION ====================
interactive_code = """print('🎯 INTERACTIVE PREDICTION & SIMULATION')
print('='*60)

# Contoh simulasi
selected_titik = 'Lokasi 1'  # Ganti dengan titik yang ada
selected_class = 'Motor'
jam_input = 14.5  # 2:30 PM
jumlah_input = 80

print(f'\\nSkenario Simulasi:')
print(f'  Titik: {selected_titik}')
print(f'  Jenis: {selected_class}')
print(f'  Jam: {jam_input:.2f}')
print(f'  Jumlah: {jumlah_input}')

# Cari data lokasi
lokasi_data = df_spasial[df_spasial['Titik'] == selected_titik].iloc[0] if selected_titik in df_spasial['Titik'].values else None

if lokasi_data is not None:
    if selected_class == 'Motor':
        # Persiapan data untuk prediksi
        data_pred = pd.DataFrame([[lokasi_data['Jumlah Motor Weekday'], 
                                   lokasi_data['Jumlah Motor Weekend']]], 
                                columns=['Jumlah Motor Weekday', 'Jumlah Motor Weekend'])
        
        # Tambahkan fitur jam
        for col in fitur_motor:
            if col not in data_pred.columns:
                data_pred[col] = lokasi_data.get(col, 0)
        
        # Prediksi
        pred_class = le_motor.inverse_transform(model_motor.predict(data_pred[fitur_motor]))[0]
        proba = model_motor.predict_proba(data_pred[fitur_motor])[0]
        confidence = proba.max()
        
        # Kategori jam
        kategori_jam = kategori_jam_otomatis(jam_input)
        
        # Tarif
        tarif_dasar = tarif_mapping['Motor'].get(pred_class, 0)
        tarif_prog = calculate_progresif_tarif('Motor', pred_class, jam_input)
        
        print(f'\\n📊 HASIL PREDIKSI:')
        print(f'  Prediksi Kelas: {pred_class}')
        print(f'  Confidence: {confidence:.4f} ({confidence*100:.2f}%)')
        print(f'  Kategori Jam: {kategori_jam}')
        print(f'  Tarif Dasar: Rp{tarif_dasar:,}')
        print(f'  Tarif Progresif (Jam {jam_input:.2f}): Rp{tarif_prog:,}')
        print(f'  Selisih Tarif: Rp{tarif_prog - tarif_dasar:,}')
        
        # Visualisasi probability
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Probability bars
        axes[0].bar(le_motor.classes_, proba, color=['#FF6B6B', '#4ECDC4', '#FFC93C'])
        axes[0].set_title(f'Prediksi Probability - {selected_class}', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Probability')
        axes[0].set_ylim([0, 1])
        for i, v in enumerate(proba):
            axes[0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
        
        # Tariff comparison
        axes[1].bar(['Dasar', f'Peak (Jam {jam_input:.1f})'], [tarif_dasar, tarif_prog], 
                   color=['#2E86AB', '#FF6B6B'])
        axes[1].set_title(f'Perbandingan Tarif - {pred_class}', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Tarif (Rp)')
        for i, v in enumerate([tarif_dasar, tarif_prog]):
            axes[1].text(i, v + 50, f'Rp{v:,}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        print('\\n✅ Prediksi berhasil!')
else:
    print(f'⚠️ Lokasi {selected_titik} tidak ditemukan!')"""

# ==================== COMPREHENSIVE DASHBOARD SECTION ====================
dashboard_code = """print('📊 COMPREHENSIVE VISUALIZATION DASHBOARD')
print('='*60)

fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Distribution of Motor Classes
ax1 = fig.add_subplot(gs[0, 0])
df['Class_Motor'].value_counts().plot(kind='barh', ax=ax1, color=['#FF6B6B', '#4ECDC4', '#FFC93C'])
ax1.set_title('Distribusi Kelas Motor', fontweight='bold')
ax1.set_xlabel('Jumlah Lokasi')

# 2. Distribution of Mobil Classes
ax2 = fig.add_subplot(gs[0, 1])
df['Class_Mobil'].value_counts().plot(kind='barh', ax=ax2, color=['#FF6B6B', '#4ECDC4', '#FFC93C'])
ax2.set_title('Distribusi Kelas Mobil', fontweight='bold')
ax2.set_xlabel('Jumlah Lokasi')

# 3. Revenue Distribution
ax3 = fig.add_subplot(gs[0, 2])
ax3.hist([df['Total_Pend_Motor'], df['Total_Pend_Mobil']], bins=15, label=['Motor', 'Mobil'], color=['#2E86AB', '#A23B72'])
ax3.set_title('Distribusi Pendapatan', fontweight='bold')
ax3.set_xlabel('Pendapatan (Rp)')
ax3.legend()

# 4. Model Accuracy Comparison
ax4 = fig.add_subplot(gs[1, 0])
models = ['Motor', 'Mobil']
accuracies = [acc_motor, acc_mobil]
ax4.bar(models, accuracies, color=['#2E86AB', '#A23B72'])
ax4.set_title('Model Accuracy', fontweight='bold')
ax4.set_ylabel('Akurasi')
ax4.set_ylim([0, 1])
for i, v in enumerate(accuracies):
    ax4.text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')

# 5. Feature Importance Motor (Top 5)
ax5 = fig.add_subplot(gs[1, 1])
importance_motor.head(5).plot(kind='barh', ax=ax5, color='#2E86AB')
ax5.set_title('Top 5 Feature Importance - Motor', fontweight='bold')
ax5.set_xlabel('Importance Score')

# 6. Feature Importance Mobil (Top 5)
ax6 = fig.add_subplot(gs[1, 2])
importance_mobil.head(5).plot(kind='barh', ax=ax6, color='#A23B72')
ax6.set_title('Top 5 Feature Importance - Mobil', fontweight='bold')
ax6.set_xlabel('Importance Score')

# 7. Confusion Matrix Motor
ax7 = fig.add_subplot(gs[2, 0])
sns.heatmap(cm_motor, annot=True, fmt='d', cmap='Blues', xticklabels=le_motor.classes_, 
            yticklabels=le_motor.classes_, ax=ax7, cbar=False)
ax7.set_title('Confusion Matrix - Motor', fontweight='bold')

# 8. Confusion Matrix Mobil
ax8 = fig.add_subplot(gs[2, 1])
sns.heatmap(cm_mobil, annot=True, fmt='d', cmap='Purples', xticklabels=le_mobil.classes_, 
            yticklabels=le_mobil.classes_, ax=ax8, cbar=False)
ax8.set_title('Confusion Matrix - Mobil', fontweight='bold')

# 9. Summary Statistics
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
summary_text = f'''RINGKASAN MODEL

Motor:
  - Accuracy: {acc_motor:.4f}
  - Total Train: {len(X_train_motor)}
  - Total Test: {len(X_test_motor)}
  - Features: {len(fitur_motor)}

Mobil:
  - Accuracy: {acc_mobil:.4f}
  - Total Train: {len(X_train_mobil)}
  - Total Test: {len(X_test_mobil)}
  - Features: {len(fitur_mobil)}

Data:
  - Total Lokasi: {len(df_spasial)}
  - Kolom Jam: {len(jam_cols)}
  - Kolom Jumlah: {len(jumlah_cols)}
'''
ax9.text(0.1, 0.5, summary_text, fontsize=10, family='monospace', 
         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('COMPREHENSIVE PARKING TARIFF ANALYSIS DASHBOARD', fontsize=16, fontweight='bold', y=0.995)
plt.show()

print('\\n✅ Dashboard visualization complete!')"
print(f'\\n✅ Total Cells in Notebook: {len(notebook["cells"])}')"

# ==================== SUMMARY & RECOMMENDATIONS SECTION ====================
summary_code = """print('\\n' + '='*60)
print('📋 RINGKASAN & REKOMENDASI')
print('='*60)

print(f'''
HASIL ANALISIS:
1. Data Preprocessing:
   - Total lokasi parkir: {len(df_spasial)}
   - Kolom fitur: {len(jam_cols) + len(jumlah_cols)}
   - Nilai missing: Ditangani melalui imputation

2. Model Performance:
   - Motor Accuracy: {acc_motor:.4f} ({acc_motor*100:.2f}%)
   - Mobil Accuracy: {acc_mobil:.4f} ({acc_mobil*100:.2f}%)
   - Model Type: Random Forest (150 estimators)

3. Feature Importance:
   - Top Feature Motor: {importance_motor.index[0]}
   - Top Feature Mobil: {importance_mobil.index[0]}

4. Progressive Tariff:
   - Tarif dasar: Rp1000 - Rp5000
   - Tarif peak (+): Rp500 - Rp1000 (Jam > 09:00)

REKOMENDASI:
✅ Model dapat digunakan untuk prediksi potensi tarif
✅ Implementasi tarif progresif di jam-jam prime (> 09:00)
✅ Monitor akurasi secara berkala dengan data baru
✅ Evaluasi perlu dilakukan setiap 3 bulan untuk fine-tuning

NEXT STEPS:
1. Deploy model ke production
2. Integrate dengan sistem pemungutan tarif
3. Monitor performa di lapangan
4. Collect feedback dari pengelola parkir
''')

print('='*60)
print('✅ ANALISIS SELESAI!')
print('='*60)"

# Find and update the remaining sections
idx_prog = find_section_index(notebook, "1️⃣2️⃣")
if idx_prog > 0:
    notebook['cells'][idx_prog + 1]['source'] = prog_tariff_code.split('\n')

idx_interactive = find_section_index(notebook, "1️⃣3️⃣")
if idx_interactive > 0:
    notebook['cells'][idx_interactive + 1]['source'] = interactive_code.split('\n')

idx_dashboard = find_section_index(notebook, "1️⃣4️⃣")
if idx_dashboard > 0:
    notebook['cells'][idx_dashboard + 1]['source'] = dashboard_code.split('\n')

# Add final summary cell
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## SUMMARY & RECOMMENDATIONS"]
})

notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": summary_code.split('\n')
})

# Save final notebook
with open('Analisis_Tarif_Parkir_Lengkap.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("✅ Notebook berhasil diselesaikan!")
print(f"📊 Total cells: {len(notebook['cells'])}")
