# 📋 CONTOH OUTPUT SIMULASI

## Scenario 1: Motor - Weekday - Volume Tinggi - Jam Ramai

```
SIMULASI #1
════════════════════════════════════════════════════════════════════════════════════════════

[1] PILIH JENIS KENDARAAN:
  1 = Motor
  2 = Mobil

Pilih jenis (1 atau 2): 1

[2] PILIH TIPE HARI:
  1 = Weekday (Hari Kerja)
  2 = Weekend (Akhir Pekan)

Pilih hari (1 atau 2): 1

[3] MASUKKAN JUMLAH MOTOR WEEKDAY:
  Jumlah Motor Weekday: 180
  Jumlah Motor Weekend: 150

[4] MASUKKAN JAM PUNCAK (Format Desimal, contoh: 17.5 untuk 17:30):
  Jam Puncak Motor Weekday: 17.25

════════════════════════════════════════════════════════════════════════════════════════════
HASIL SIMULASI #1
════════════════════════════════════════════════════════════════════════════════════════════

📊 INPUT:
  • Jenis Kendaraan    : Motor
  • Tipe Hari          : Weekday
  • Jumlah Motor Weekday    : 180 unit
  • Jumlah Motor Weekend    : 150 unit
  • Jam Puncak         : 17.25 (Kategori: Ramai)

🎯 PREDIKSI:
  • Klasifikasi Potensi: TINGGI
  • Confidence/Keyakinan: 89.32%
  • Probabilitas Kelas:
      - Rendah: 1.85%
      - Sedang: 8.83%
      - Tinggi: 89.32%

💰 REKOMENDASI TARIF:
  • Tarif Dasar        : Rp3,000 / jam
  • Tarif Progresif    : Rp4,000 / jam
  • Selisih            : Rp1,000 / jam

════════════════════════════════════════════════════════════════════════════════════════════
Apakah Anda ingin simulasi lagi? (y/n): y
```

### Interpretasi:
- ✅ Volume motor tinggi (180 weekday, 150 weekend)
- ✅ Jam ramai (17:25 = sore hari, banyak aktivitas)
- ✅ Prediksi: **TINGGI** (89% confidence)
- ✅ Rekomendasi: Pakai tarif Rp4,000/jam (bonus Rp1,000)
- 💡 Alasan: Permintaan tinggi → naikan tarif untuk optimasi revenue

---

## Scenario 2: Mobil - Weekend - Volume Sedang - Jam Sedang

```
SIMULASI #2
════════════════════════════════════════════════════════════════════════════════════════════

Pilih jenis (1 atau 2): 2
Pilih hari (1 atau 2): 2

[3] MASUKKAN JUMLAH MOBIL WEEKDAY:
  Jumlah Mobil Weekday: 95
  Jumlah Mobil Weekend: 78

[4] MASUKKAN JAM PUNCAK:
  Jam Puncak Mobil Weekend: 14.5

════════════════════════════════════════════════════════════════════════════════════════════
HASIL SIMULASI #2
════════════════════════════════════════════════════════════════════════════════════════════

📊 INPUT:
  • Jenis Kendaraan    : Mobil
  • Tipe Hari          : Weekend
  • Jumlah Mobil Weekday    : 95 unit
  • Jumlah Mobil Weekend    : 78 unit
  • Jam Puncak         : 14.50 (Kategori: Ramai)

🎯 PREDIKSI:
  • Klasifikasi Potensi: SEDANG
  • Confidence/Keyakinan: 71.45%
  • Probabilitas Kelas:
      - Rendah: 8.20%
      - Sedang: 71.45%
      - Tinggi: 20.35%

💰 REKOMENDASI TARIF:
  • Tarif Dasar        : Rp4,000 / jam
  • Tarif Progresif    : Rp4,500 / jam
  • Selisih            : Rp500 / jam

════════════════════════════════════════════════════════════════════════════════════════════
Apakah Anda ingin simulasi lagi? (y/n): y
```

### Interpretasi:
- ⚠️ Volume mobil sedang (95 weekday, 78 weekend)
- ⚠️ Jam ramai siang (14:30 = siang hari, aktivitas menengah)
- ⚠️ Prediksi: **SEDANG** (71% confidence) - ada ambiguitas
- ⚠️ Rekomendasi: Pakai tarif Rp4,500/jam (bonus Rp500)
- 💡 Alasan: Permintaan menengah → naikan sedikit untuk revenue optimization

---

## Scenario 3: Motor - Weekday - Volume Rendah - Jam Sepi

```
SIMULASI #3
════════════════════════════════════════════════════════════════════════════════════════════

Pilih jenis (1 atau 2): 1
Pilih hari (1 atau 2): 1

[3] MASUKKAN JUMLAH MOTOR WEEKDAY:
  Jumlah Motor Weekday: 35
  Jumlah Motor Weekend: 25

[4] MASUKKAN JAM PUNCAK:
  Jam Puncak Motor Weekday: 3.0

════════════════════════════════════════════════════════════════════════════════════════════
HASIL SIMULASI #3
════════════════════════════════════════════════════════════════════════════════════════════

📊 INPUT:
  • Jenis Kendaraan    : Motor
  • Tipe Hari          : Weekday
  • Jumlah Motor Weekday    : 35 unit
  • Jumlah Motor Weekend    : 25 unit
  • Jam Puncak         : 3.00 (Kategori: Sepi)

🎯 PREDIKSI:
  • Klasifikasi Potensi: RENDAH
  • Confidence/Keyakinan: 94.72%
  • Probabilitas Kelas:
      - Rendah: 94.72%
      - Sedang: 4.15%
      - Tinggi: 1.13%

💰 REKOMENDASI TARIF:
  • Tarif Dasar        : Rp1,000 / jam
  • Tarif Progresif    : Rp1,000 / jam
  • Selisih            : Rp0 / jam

════════════════════════════════════════════════════════════════════════════════════════════
Apakah Anda ingin simulasi lagi? (y/n): n

✓ Total simulasi yang dilakukan: 3
```

### Interpretasi:
- ❌ Volume motor rendah (35 weekday, 25 weekend)
- ❌ Jam sepi (03:00 = tengah malam, tidak ada aktivitas)
- ✅ Prediksi: **RENDAH** (95% confidence - sangat yakin)
- ✅ Rekomendasi: Pakai tarif dasar Rp1,000/jam saja
- 💡 Alasan: Permintaan rendah → jaga tarif murah untuk attract customers

---

## Scenario 4: Mobil - Weekend - Volume Tinggi - Jam Ramai

```
SIMULASI #4
════════════════════════════════════════════════════════════════════════════════════════════

Pilih jenis (1 atau 2): 2
Pilih hari (1 atau 2): 2

[3] MASUKKAN JUMLAH MOBIL WEEKDAY:
  Jumlah Mobil Weekday: 145
  Jumlah Mobil Weekend: 165

[4] MASUKKAN JAM PUNCAK:
  Jam Puncak Mobil Weekend: 12.0

════════════════════════════════════════════════════════════════════════════════════════════
HASIL SIMULASI #4
════════════════════════════════════════════════════════════════════════════════════════════

📊 INPUT:
  • Jenis Kendaraan    : Mobil
  • Tipe Hari          : Weekend
  • Jumlah Mobil Weekday    : 145 unit
  • Jumlah Mobil Weekend    : 165 unit
  • Jam Puncak         : 12.00 (Kategori: Ramai)

🎯 PREDIKSI:
  • Klasifikasi Potensi: TINGGI
  • Confidence/Keyakinan: 86.55%
  • Probabilitas Kelas:
      - Rendah: 2.75%
      - Sedang: 10.70%
      - Tinggi: 86.55%

💰 REKOMENDASI TARIF:
  • Tarif Dasar        : Rp5,000 / jam
  • Tarif Progresif    : Rp6,000 / jam
  • Selisih            : Rp1,000 / jam

════════════════════════════════════════════════════════════════════════════════════════════
Apakah Anda ingin simulasi lagi? (y/n): n

✓ Total simulasi yang dilakukan: 4
════════════════════════════════════════════════════════════════════════════════════════════
TERIMA KASIH TELAH MENGGUNAKAN SIMULASI TARIF PARKIR PROGRESIF!
════════════════════════════════════════════════════════════════════════════════════════════
```

### Interpretasi:
- ✅ Volume mobil tinggi (145 weekday, 165 weekend) - even higher on weekend
- ✅ Jam ramai siang (12:00 = lunch time, peak activity)
- ✅ Prediksi: **TINGGI** (87% confidence)
- ✅ Rekomendasi: Pakai tarif Rp6,000/jam (bonus Rp1,000)
- 💡 Alasan: Permintaan SANGAT tinggi → maksimalkan revenue dengan tarif tertinggi

---

## 📊 Summary Comparison

### Pola Output:

| Scenario | Volume | Jam | Potensi | Confidence | Tarif Dasar | Tarif Progresif | Status |
|----------|--------|-----|---------|------------|-------------|-----------------|--------|
| **#1** | Tinggi | Ramai | TINGGI | 89.32% | Rp3,000 | Rp4,000 | ✅ Naik |
| **#2** | Sedang | Ramai | SEDANG | 71.45% | Rp4,000 | Rp4,500 | ⚠️ Ambigous |
| **#3** | Rendah | Sepi | RENDAH | 94.72% | Rp1,000 | Rp1,000 | ❌ Flat |
| **#4** | Tinggi | Ramai | TINGGI | 86.55% | Rp5,000 | Rp6,000 | ✅ Naik |

### Insight:
1. **Volume + Jam = Strong Predictor**
   - High volume + Ramai jam → TINGGI (High confidence)
   - Low volume + Sepi jam → RENDAH (High confidence)

2. **Confidence Score Pattern**
   - Clear cases (Tinggi/Rendah): 85-95% confidence
   - Ambiguous cases (Sedang): 60-75% confidence

3. **Tarif Progresif Impact**
   - Hanya berlaku saat jam > 09:00
   - Bonus Rp1000 untuk TINGGI, Rp500 untuk SEDANG
   - Tarif RENDAH tidak ada bonus

4. **Decision Factors**
   - **Jumlah kendaraan**: Primary factor (high importance)
   - **Jam puncak**: Secondary factor (affects category)
   - **Tipe hari**: Tertiary (but still significant)

---

## 🔍 Error Handling Examples

### Invalid Input: Non-numeric

```
Pilih jenis (1 atau 2): abc
❌ Input tidak valid! Silakan masukkan angka 1 atau 2.

Pilih jenis (1 atau 2): 1
```

### Invalid Input: Out of Range

```
Jam Puncak Motor Weekday: 25
❌ Jam harus antara 0-24!

Jam Puncak Motor Weekday: 17.5
```

### Invalid Input: Negative Number

```
Jumlah Motor Weekday: -50
❌ Jumlah kendaraan tidak boleh negatif!

Jumlah Motor Weekday: 150
```

---

## 💾 File Outputs After Running

Setelah menjalankan simulasi, akan ada:

```
d:/TarifProgresifParkirBanyumas/
├── simulasi_simple.py (modified)
├── [STEP 1-11 Outputs]
│   ├── Tabel_Rekomendasi_Tarif_Parkir.xlsx
│   ├── motor_decision_tree.png
│   ├── mobil_decision_tree.png
│   └── peta_potensi_tarif_parkir.html ← BUKA DI BROWSER
├── [Console Output dari STEP 12]
│   └── (Lihat di terminal saat simulasi)
└── [Documentation Files]
    ├── SUMMARY_UPGRADE.md
    ├── README_SIMULASI_SIMPLE.md
    └── CHANGELOG_SIMULASI_SIMPLE.md
```

---

## 🎯 Tips Menggunakan Output

### 1. **Dari Console (STEP 12)**
- Copy-paste hasil ke notepad untuk dokumentasi
- Screenshot untuk presentation
- Bandingkan hasil berbagai scenario

### 2. **Dari Excel (STEP 11)**
- Filter berdasarkan kategori potensi
- Hitung revenue projection
- Analisis distribusi spasial

### 3. **Dari Map (STEP 11A)**
- Identifikasi hotspot (Tinggi concentration)
- Temukan underutilized areas (Rendah)
- Lihat pola Motor vs Mobil
- Export screenshot untuk report

---

**Version**: 2.0
**Last Updated**: 25 Desember 2025
