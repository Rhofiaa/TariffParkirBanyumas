# CHANGELOG: simulasi_simple.py - Update Baru

## 📋 Ringkasan Perubahan

Simulasi_simple.py telah diperbarui dengan menggabungkan fitur-fitur canggih dari app.py, termasuk:

1. ✅ **Analisis Spasial dengan Folium Map**
2. ✅ **Simulasi Interaktif dengan Input Manual**
3. ✅ **Validasi Input & Error Handling**
4. ✅ **Tarif Progresif Dinamis**
5. ✅ **Multiple Simulation Scenarios**

---

## 🔄 Detail Perubahan

### 1. **Penambahan Import & Library**

```python
import datetime
import folium
from folium import plugins
```

**Alasan**: Mendukung visualisasi peta interaktif dan fungsi tanggal.

---

### 2. **Penambahan Fungsi Helper (dari app.py)**

#### A. `kategori_jam_otomatis(jam)`
Mengkategorisasi jam desimal menjadi Sepi/Sedang/Ramai:
- **Sepi**: 00:00-06:00 & 22:00-24:00 (jam <= 6 atau >= 22)
- **Ramai**: 08:00-19:00 (jam > 8 dan <= 19)
- **Sedang**: Jam lainnya

#### B. `time_to_decimal_hour(time_obj)`
Konversi datetime.time ke jam desimal (H + M/60)

#### C. `calculate_progresif_tarif(jenis, potensi_class, jam_desimal)`
Menerapkan tarif progresif dinamis berdasarkan:
- Jenis kendaraan (Motor/Mobil)
- Klasifikasi potensi (Rendah/Sedang/Tinggi)
- Jam puncak (nilai desimal)

**Logika Progresif**:
- Jika jam > 9.0 dan potensi TINGGI: Tarif naik Rp1000
- Jika jam > 9.0 dan potensi SEDANG: Tarif naik Rp500
- Jika jam <= 9.0: Tarif dasar saja

#### D. `tarif_mapping` (Dictionary)
```python
{
    'Motor': {'Rendah': 1000, 'Sedang': 2000, 'Tinggi': 3000},
    'Mobil': {'Rendah': 3000, 'Sedang': 4000, 'Tinggi': 5000}
}
```

---

### 3. **STEP 11A: Analisis Spasial dengan Folium Map** ✨

**File Output**: `peta_potensi_tarif_parkir.html`

**Fitur**:
- 📍 Visualisasi 407 titik parkir di Banyumas
- 🗺️ Dual layer: Motor & Mobil (dapat di-toggle)
- 🎨 Warna berdasarkan kategori potensi:
  - 🟠 Orange = Rendah
  - 🟡 Gold = Sedang
  - 🔴 Tomato Red = Tinggi
- 📌 Interactive markers dengan:
  - Nama lokasi
  - Kategori potensi
  - Tarif dasar rekomendasi
- 🗺️ Multiple tile layers (OpenStreetMap & Esri Satellite)
- 📜 Legenda dengan keterangan warna
- 🎯 Zoom & pan interaktif

**Cara Menggunakan**:
1. Jalankan script: `python simulasi_simple.py`
2. Setelah selesai, buka file `peta_potensi_tarif_parkir.html` di browser
3. Klik marker untuk melihat detail lokasi
4. Toggle layer Motor/Mobil untuk melihat prediksi berbeda

---

### 4. **STEP 12: Simulasi Prediksi Interaktif** 🎯

**Fitur Utama**:
- 👤 Input manual untuk setiap simulasi
- 🔄 Loop untuk multiple scenarios (user dapat simulasi berkali-kali)
- ✅ Validasi lengkap untuk setiap input
- 🎓 Tampilan hasil yang terstruktur

**Input yang Diminta**:

```
[1] PILIH JENIS KENDARAAN
    1 = Motor
    2 = Mobil

[2] PILIH TIPE HARI
    1 = Weekday (Hari Kerja)
    2 = Weekend (Akhir Pekan)

[3] MASUKKAN JUMLAH KENDARAAN
    • Jumlah Weekday: [angka]
    • Jumlah Weekend: [angka]

[4] MASUKKAN JAM PUNCAK
    Format: Desimal (contoh: 17.5 untuk 17:30)
    Range: 0-24
```

**Output yang Ditampilkan**:

```
🎯 HASIL SIMULASI #[N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 INPUT:
  • Jenis Kendaraan    : Motor/Mobil
  • Tipe Hari          : Weekday/Weekend
  • Jumlah Weekday     : X unit
  • Jumlah Weekend     : Y unit
  • Jam Puncak         : Z.Z (Kategori: Ramai/Sedang/Sepi)

🎯 PREDIKSI:
  • Klasifikasi Potensi: Rendah/Sedang/Tinggi
  • Confidence         : XX.XX%
  • Probabilitas Kelas:
      - Rendah : XX.XX%
      - Sedang : XX.XX%
      - Tinggi : XX.XX%

💰 REKOMENDASI TARIF:
  • Tarif Dasar        : Rp X,XXX / jam
  • Tarif Progresif    : Rp X,XXX / jam
  • Selisih            : Rp XXX / jam
```

**Validasi Input**:
- ✓ Jumlah kendaraan >= 0
- ✓ Jam dalam range 0-24
- ✓ Deteksi format input yang salah
- ✓ Pesan error yang informatif

**Flow Simulasi**:
1. User diminta input jenis kendaraan
2. Memilih tipe hari
3. Memasukkan jumlah kendaraan (Weekday & Weekend)
4. Memasukkan jam puncak
5. Sistem menampilkan hasil prediksi
6. Tanya apakah ingin simulasi lagi (y/n)
7. Lanjut simulasi atau exit

---

## 📊 Perbandingan Sebelum vs Sesudah

| Aspek | Sebelum | Sesudah |
|-------|---------|---------|
| **Simulasi** | 3 contoh hardcoded | Unlimited (user input) |
| **Input Method** | Langsung di code | Interactive input() |
| **Spasial Analysis** | ❌ Tidak ada | ✅ Folium map dengan 407 lokasi |
| **Tarif Dinamis** | ❌ Hanya dasar | ✅ Progresif berdasarkan jam |
| **Validasi** | ❌ Minimal | ✅ Lengkap dengan error handling |
| **Loop Simulasi** | ❌ Fixed 3 sample | ✅ While loop (repeat as needed) |
| **Map Output** | ❌ Tidak ada | ✅ HTML interaktif |

---

## 🚀 Cara Menggunakan Script

### 1. **Jalankan Script**
```bash
python simulasi_simple.py
```

### 2. **Tunggu hingga STEP 12**
Script akan menyelesaikan STEP 1-11 terlebih dahulu, kemudian masuk ke simulasi interaktif.

### 3. **Ikuti Prompt Input**
- Pilih jenis kendaraan (1 atau 2)
- Pilih tipe hari (1 atau 2)
- Masukkan jumlah kendaraan
- Masukkan jam puncak

### 4. **Baca Hasil Prediksi**
Output akan menampilkan:
- Klasifikasi potensi (Rendah/Sedang/Tinggi)
- Confidence score
- Distribusi probabilitas
- Rekomendasi tarif (dasar dan progresif)

### 5. **Simulasi Lagi atau Exit**
- Input `y` untuk simulasi lagi
- Input `n` untuk keluar

### 6. **Buka Peta Hasil**
Setelah script selesai:
1. Buka file: `peta_potensi_tarif_parkir.html`
2. Jelajahi titik-titik parkir di peta
3. Klik marker untuk melihat detail

---

## 📁 File Output

| File | Deskripsi |
|------|-----------|
| `Tabel_Rekomendasi_Tarif_Parkir.xlsx` | Tabel hasil prediksi semua 407 lokasi |
| `peta_potensi_tarif_parkir.html` | Peta interaktif dengan marker lokasi |
| `motor_decision_tree.png` | Visualisasi pohon keputusan Motor |
| `mobil_decision_tree.png` | Visualisasi pohon keputusan Mobil |

---

## 🔧 Fitur Teknis

### **Model & Training**
- RandomForest: 150 trees, max_depth=15, min_samples_leaf=3
- Train-Test Split: 80-20
- Akurasi Motor: ~97% training, ~93% testing
- Akurasi Mobil: ~96% training, ~92% testing

### **Feature Engineering**
- Konversi jam dari format string ke desimal
- Klasifikasi target dengan qcut (Rendah/Sedang/Tinggi)
- Pendapatan tahunan sebagai basis klasifikasi

### **Spatial Analysis**
- Folium library untuk interaktif map
- GeoJSON untuk marker positioning
- Layer control untuk toggle Motor/Mobil
- Custom legend dengan HTML

---

## 💡 Tips Penggunaan

1. **Input Jam Desimal**: 
   - 17:30 = 17.5
   - 14:15 = 14.25
   - 09:45 = 9.75

2. **Interpretasi Kategori Jam**:
   - **Sepi**: 00:00-06:00 & 22:00-24:00 (vol rendah)
   - **Ramai**: 08:00-19:00 (vol tinggi)
   - **Sedang**: 06:00-08:00 & 19:00-22:00 (vol menengah)

3. **Tarif Progresif**:
   - Berlaku saat jam > 09:00
   - Bonus: +Rp1000 untuk potensi Tinggi, +Rp500 untuk Sedang
   - Tujuan: Mencegah penyalahgunaan di jam puncak

4. **Multiple Simulasi**:
   - Lakukanlah beberapa simulasi untuk membandingkan skenario
   - Contoh: Motor vs Mobil, Weekday vs Weekend, Morning vs Evening

---

## ✨ Keunggulan Update Ini

✅ **Interaktif**: User dapat input parameter sendiri tanpa modifikasi kode
✅ **Spasial**: Visualisasi semua lokasi dalam satu peta
✅ **Fleksibel**: Unlimited simulasi dalam satu sesi
✅ **Robust**: Input validation dan error handling
✅ **Progresif**: Tarif dinamis berdasarkan jam dan potensi
✅ **Comprehensive**: Gabungan fitur dari app.py dalam format standalone

---

## 📝 Catatan

- Script ini menggunakan data dari `DataParkir_Fix.xlsx`
- Semua fitur telah terintegrasi dari `app.py`
- Tidak perlu Streamlit atau web framework apapun
- Output berupa file Excel, PNG, dan HTML (portable)

---

**Terakhir Diupdate**: Desember 2025
**Kompatibilitas**: Python 3.7+
