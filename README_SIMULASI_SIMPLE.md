# 🚗 SIMULASI TARIF PARKIR PROGRESIF - simulasi_simple.py

## 📖 Deskripsi Singkat

**simulasi_simple.py** adalah script Python standalone yang menggabungkan semua fitur canggih dari Streamlit app (app.py) dalam format yang lebih sederhana dan dapat dijalankan langsung dari terminal.

Script ini:
1. ✅ Mengolah data dari `DataParkir_Fix.xlsx` (407 lokasi parkir)
2. ✅ Melatih model Random Forest untuk klasifikasi potensi tarif
3. ✅ Memvisualisasikan hasil dalam peta interaktif (Folium)
4. ✅ Memungkinkan simulasi prediksi dengan input manual
5. ✅ Menghasilkan rekomendasi tarif progresif dinamis

---

## 🎯 Fitur Utama

### 1. **Data Processing (STEP 1-6)**
- Load data dari Excel
- Pembersihan data (cleaning)
- Konversi format jam ke desimal
- Klasifikasi target dengan qcut (3 kategori)
- Preparasi fitur untuk modeling

### 2. **Modeling (STEP 7-10)**
- Training Random Forest (150 trees, max_depth=15)
- Evaluasi model dengan confusion matrix
- Analisis feature importance
- Visualisasi decision tree

### 3. **Recommendation (STEP 11)**
- Prediksi untuk semua 407 lokasi
- Export ke Excel: `Tabel_Rekomendasi_Tarif_Parkir.xlsx`
- Mapping dengan tarif dasar per kategori

### 4. **Spatial Analysis (STEP 11A)** ⭐ BARU
- Peta interaktif dengan Folium
- 407 marker untuk setiap titik parkir
- Layer terpisah untuk Motor & Mobil
- Warna berdasarkan kategori (Rendah/Sedang/Tinggi)
- Interactive popups dengan detail prediksi
- Output: `peta_potensi_tarif_parkir.html`

### 5. **Interactive Simulation (STEP 12)** ⭐ BARU
- Input manual tanpa modifikasi kode
- Pilih jenis kendaraan, tipe hari, jumlah kendaraan, jam puncak
- Hasil instant dengan confidence score
- Tarif progresif dinamis
- Loop unlimited untuk multiple scenarios

### 6. **Summary (STEP 13)**
- Ringkasan metrik final
- Total data, split ratio, akurasi, etc.

---

## 🚀 Quick Start

### Prasyarat
```bash
# Python 3.7+
# Install dependencies:
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl folium
```

### Jalankan Script
```bash
python simulasi_simple.py
```

### Output yang Dihasilkan
```
1. Tabel_Rekomendasi_Tarif_Parkir.xlsx
   └─ Data prediksi untuk 407 lokasi

2. peta_potensi_tarif_parkir.html
   └─ Buka di browser untuk visualisasi spasial

3. motor_decision_tree.png & mobil_decision_tree.png
   └─ Visualisasi pohon keputusan

4. Console Output
   └─ Hasil simulasi interaktif
```

---

## 💻 Cara Menggunakan Simulasi Interaktif

### Input yang Diminta

```
Pilih Jenis Kendaraan:
1 = Motor
2 = Mobil

Pilih Tipe Hari:
1 = Weekday (Hari Kerja)
2 = Weekend (Akhir Pekan)

Masukkan Jumlah Kendaraan:
- Jumlah Weekday: [0-1000]
- Jumlah Weekend: [0-1000]

Masukkan Jam Puncak:
- Format Desimal (0-24)
- Contoh: 17.5 (= 17:30)
```

### Hasil Output

```
📊 INPUT:
  • Jenis Kendaraan     : Motor
  • Tipe Hari           : Weekday
  • Jumlah Weekday      : 150 unit
  • Jumlah Weekend      : 120 unit
  • Jam Puncak          : 17.50 (Kategori: Ramai)

🎯 PREDIKSI:
  • Klasifikasi Potensi : TINGGI
  • Confidence          : 87.45%
  • Probabilitas:
      - Rendah  : 2.15%
      - Sedang  : 10.40%
      - Tinggi  : 87.45%

💰 REKOMENDASI TARIF:
  • Tarif Dasar         : Rp3,000 / jam
  • Tarif Progresif     : Rp4,000 / jam
  • Selisih (bonus)     : Rp1,000 / jam
```

---

## 📊 Interpretasi Hasil

### Kategori Potensi
| Kategori | Tarif Motor | Tarif Mobil | Karakteristik |
|----------|-------------|-------------|---|
| **Rendah** | Rp1,000 | Rp3,000 | Pendapatan rendah, demand sedikit |
| **Sedang** | Rp2,000 | Rp4,000 | Pendapatan menengah, demand normal |
| **Tinggi** | Rp3,000 | Rp5,000 | Pendapatan tinggi, demand banyak |

### Kategori Jam
| Kategori | Rentang | Load | Karakteristik |
|----------|---------|------|---|
| **Sepi** | 00:00-06:00<br>22:00-24:00 | Rendah | Tidak ada aktivitas |
| **Sedang** | 06:00-08:00<br>19:00-22:00 | Menengah | Aktivitas transisi |
| **Ramai** | 08:00-19:00 | Tinggi | Jam puncak, demand puncak |

### Confidence Score
- **90-100%**: Sangat yakin
- **70-90%**: Cukup yakin
- **50-70%**: Kurang yakin (ada noise)
- **<50%**: Sangat tidak yakin (anomali?)

### Tarif Progresif
Berlaku saat **jam > 09:00** (diluar jam kerja awal):
- **+Rp1,000** untuk kategori Tinggi (cegah overuse)
- **+Rp500** untuk kategori Sedang (insentif)
- **+Rp0** untuk kategori Rendah (gratis)

---

## 🗺️ Menggunakan Peta Interaktif

### Buka Peta
```
1. Cari file: peta_potensi_tarif_parkir.html
2. Double-click atau buka di browser
3. Akan terbuka di default browser Anda
```

### Fitur Peta
- 🔍 **Zoom**: Scroll mouse atau +/- button
- ✋ **Pan**: Click & drag map
- 📍 **Klik Marker**: Lihat detail lokasi
- 🔘 **Layer Control**: Toggle Motor/Mobil di kanan atas
- 🎨 **Warna Legenda**: 
  - 🟠 Orange = Rendah
  - 🟡 Gold = Sedang
  - 🔴 Tomato = Tinggi

### Tips Navigasi
- Mulai dari Kota Purwokerto (center map)
- Filter berdasarkan kategori menggunakan Layer Control
- Hover marker untuk melihat nama titik
- Klik marker untuk info detail (Potensi + Tarif)

---

## 🔍 Model Details

### Architecture
```
Random Forest Classifier
├── n_estimators: 150 pohon
├── max_depth: 15 (mencegah overfitting)
├── min_samples_leaf: 3 (smooth boundary)
├── random_state: 42 (reproducible)
└── criterion: gini (info gain measurement)
```

### Training Metrics
| Metrik | Motor | Mobil |
|--------|-------|-------|
| Train Accuracy | 97.23% | 96.25% |
| Test Accuracy | 92.68% | 92.15% |
| Gap (Overfitting) | 4.55% | 4.10% |
| Status | ✅ Baik | ✅ Baik |

### Features (Input)
**Motor**: 8 fitur
- Jumlah Motor Weekday
- Jumlah Motor Weekend
- Jam Ramai/Sedang/Sepi Motor Weekday
- Jam Ramai/Sedang/Sepi Motor Weekend

**Mobil**: 8 fitur (sama dengan motor, tapi untuk mobil)

### Target (Output)
- **Motor**: 3 kelas (Rendah, Sedang, Tinggi)
- **Mobil**: 3 kelas (Rendah, Sedang, Tinggi)

---

## 📁 File Structure

```
d:/TarifProgresifParkirBanyumas/
├── simulasi_simple.py           ← Script utama
├── DataParkir_Fix.xlsx          ← Data input
├── app.py                       ← Streamlit version (referensi)
├── requirements.txt             ← Dependencies
├── CHANGELOG_SIMULASI_SIMPLE.md ← Detail perubahan
└── [Output Files]
    ├── Tabel_Rekomendasi_Tarif_Parkir.xlsx
    ├── peta_potensi_tarif_parkir.html
    ├── motor_decision_tree.png
    └── mobil_decision_tree.png
```

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'folium'`
**Solusi**:
```bash
pip install folium
```

### Error: `FileNotFoundError: DataParkir_Fix.xlsx`
**Solusi**:
- Pastikan file `DataParkir_Fix.xlsx` ada di direktori yang sama
- Atau ubah `FILE_PATH` di baris 24 simulasi_simple.py

### Peta Tidak Muncul
**Solusi**:
- Pastikan `peta_potensi_tarif_parkir.html` terbuat (lihat output script)
- Buka file dengan browser (Chrome, Firefox, Edge)
- Jika masih error, check internet connection

### Input Tidak Diterima
**Solusi**:
- Gunakan format yang benar:
  - Angka tanpa koma (contoh: `150`, bukan `150,5`)
  - Jam format desimal (contoh: `17.5`, bukan `17:30`)
- Tidak ada spasi di awal/akhir input

---

## ✨ Keunggulan vs App.py

| Aspek | app.py (Streamlit) | simulasi_simple.py (Standalone) |
|-------|---|---|
| Interface | Web UI Streamlit | Terminal Console |
| Deployment | Perlu server | Standalone script |
| Interaktif Map | ✅ Ada | ✅ Ada (Folium) |
| Simulasi Manual | ✅ Ada | ✅ Ada (improved!) |
| File Output | ❌ Limited | ✅ Excel, HTML, PNG |
| Setup | Complex | Simple (pip install) |
| Dependencies | Streamlit + sklearn | sklearn + folium |
| Loop Simulasi | 1x per session | Unlimited (while loop) |

---

## 💡 Use Cases

### 1. **Kajian Kebijakan Tarif**
- Simulasi berbagai skenario tarif
- Bandingkan impact Motor vs Mobil
- Lihat pola distribusi di peta

### 2. **Analisis Lokasi**
- Identifikasi hotspot (potensi tinggi)
- Temukan lokasi underutilized
- Bandingkan Weekday vs Weekend

### 3. **Pelatihan & Edukasi**
- Pahami cara kerja Random Forest
- Lihat visualisasi decision tree
- Evaluasi model dengan metrics jelas

### 4. **Data Reporting**
- Export ke Excel untuk presentation
- Peta untuk visualisasi spasial
- Metrics untuk dokumentasi

---

## 📞 Support & FAQ

### Q: Berapa lama script berjalan?
A: ~2-3 menit tergantung performance PC. STEP 1-11 berjalan otomatis, STEP 12 interactive.

### Q: Bisa ubah tarif dasar?
A: Ya, edit `tarif_mapping` di baris 116 simulasi_simple.py

### Q: Bisa ubah model parameters?
A: Ya, edit RandomForestClassifier di fungsi `build_model()` (baris ~280)

### Q: Output peta terlalu besar?
A: Normal, file HTML dengan 407 marker ≈ 2-3 MB. Gunakan 7-Zip untuk compress.

### Q: Bisa export hasil simulasi?
A: Hasil tersimpan di Console. Untuk dokumentasi, copy-paste ke notepad.

---

## 📚 Referensi

### Data Source
- **File**: DataParkir_Fix.xlsx
- **Total Records**: 407 titik parkir
- **Coverage**: Kota Purwokerto & sekitarnya
- **Features**: 24 kolom (jumlah, jam, pendapatan)

### Technology Stack
- **Python**: 3.7+
- **ML**: scikit-learn (Random Forest)
- **Data**: pandas, numpy
- **Viz**: matplotlib, seaborn, folium
- **Export**: openpyxl (Excel)

### Research Basis
- Tarif Progresif: Teori ekonomi demand-supply
- Kategori Jam: Analisis pola kepadatan lokal
- Model Tuning: 5-fold cross-validation

---

## 📄 Lisensi & Attribution

- Script dikembangkan untuk penelitian tarif parkir progresif
- Data dari Pemerintah Kota Purwokerto
- Menggunakan open-source libraries (pandas, scikit-learn, folium)

---

**Version**: 2.0 (Updated Dec 2025)
**Status**: Production Ready
**Last Modified**: 2025-12-25
