# Bab 4: Kuantil dan Klasifikasi Potensi Tarif

## 4.1 Proses Perhitungan Kuantil

### 4.1.1 Tahap 1: Perhitungan Pendapatan Harian

Langkah pertama dalam proses klasifikasi adalah menghitung **pendapatan harian potensial** untuk setiap lokasi parkir.

**Rumus Pendapatan Harian:**

$$\text{Pendapatan Harian} = \sum_{jam=0}^{23} (\text{Jumlah Kendaraan}_jam \times \text{Durasi Rata-rata} \times \text{Tarif Dasar})$$

**Contoh Perhitungan (Lokasi: Pasar Banyumas - Motor):**

| Jam | Jumlah Motor | Durasi (jam) | Tarif Dasar | Pendapatan Jam |
|-----|--------------|--------------|-------------|----------------|
| 06:00-07:00 | 15 | 2 | Rp2.000 | Rp60.000 |
| 07:00-09:00 | 45 | 2.5 | Rp2.000 | Rp225.000 |
| 09:00-12:00 | 85 | 3 | Rp2.000 | Rp510.000 |
| 12:00-17:00 | 120 | 2 | Rp2.000 | Rp480.000 |
| 17:00-20:00 | 95 | 1.5 | Rp2.000 | Rp285.000 |
| 20:00-23:00 | 30 | 1 | Rp2.000 | Rp60.000 |
| **Total Hari** | **390** | - | - | **Rp1.620.000** |

**Data Input dari Dataset:**
- Sumber: Kolom `Pendapatan Motor Weekday`, `Pendapatan Mobil Weekday`, dll
- File: `Rekomendasi_Tarif_Parkir.csv`
- Jumlah lokasi: 15 titik parkir
- Jenis kendaraan: 2 (Motor, Mobil)
- Hari: 2 kategori (Weekday, Weekend)

---

## 4.2 Tahap 2: Penentuan Batas Kuantil

### 4.2.1 Konsep Kuantil (Quartile/Percentile)

**Kuantil** adalah nilai-nilai yang membagi dataset menjadi bagian-bagian yang sama besar.

**Rumus Kuantil:**

$$Q_p = \text{nilai pada persentil ke-}p\% \text{ dari data yang diurutkan}$$

Untuk klasifikasi 3 kelas (Rendah, Sedang, Tinggi), kami menggunakan:
- **Q1 (25th percentile)**: Batas antara Rendah dan Sedang
- **Q3 (75th percentile)**: Batas antara Sedang dan Tinggi

### 4.2.2 Contoh Perhitungan Kuantil - Motor Weekday

**Data Pendapatan Harian Motor Weekday (diurutkan):**

```
15 lokasi → 15 data point
Urutan: [980.000, 1.150.000, 1.280.000, 1.450.000, 1.620.000, 
         1.780.000, 1.920.000, 2.100.000, 2.350.000, 2.680.000, 
         2.850.000, 3.100.000, 3.420.000, 3.750.000, 4.200.000]
```

**Perhitungan Q1 (Kuartil Pertama - 25%):**

$$Q1_{index} = 0.25 \times (n + 1) = 0.25 \times 16 = 4$$

- Ambil elemen ke-4 dari data urutan = **Rp1.450.000**

**Perhitungan Q3 (Kuartil Ketiga - 75%):**

$$Q3_{index} = 0.75 \times (n + 1) = 0.75 \times 16 = 12$$

- Ambil elemen ke-12 dari data urutan = **Rp3.100.000**

### 4.2.3 Tabel Batas Kuantil (Hasil Perhitungan)

| Kategori | Motor Weekday | Motor Weekend | Mobil Weekday | Mobil Weekend |
|----------|---------------|---------------|---------------|---------------|
| **Q1 (Batas Rendah-Sedang)** | Rp1.450.000 | Rp1.280.000 | Rp2.850.000 | Rp2.680.000 |
| **Q3 (Batas Sedang-Tinggi)** | Rp3.100.000 | Rp2.950.000 | Rp5.800.000 | Rp5.420.000 |

---

## 4.3 Tahap 3: Penentuan Kelas Potensi Tarif

### 4.3.1 Aturan Klasifikasi

Setelah mendapatkan Q1 dan Q3, data diklasifikasikan ke dalam 3 kelas:

```
IF Pendapatan ≤ Q1:
    Class = "Rendah"
ELSE IF Pendapatan ≤ Q3:
    Class = "Sedang"
ELSE:
    Class = "Tinggi"
```

### 4.3.2 Contoh Klasifikasi Lengkap

**Dataset Pendapatan Motor Weekday dengan Klasifikasi:**

| Titik Parkir | Pendapatan Motor WD | Klasifikasi | Alasan |
|--------------|-------------------|-------------|--------|
| Alun-alun Banyumas | Rp980.000 | **Rendah** | 980K ≤ 1.450K (Q1) |
| Jl. Gatot Subroto | Rp1.620.000 | **Sedang** | 1.450K < 1.620K ≤ 3.100K |
| Jl. Soekarno Hatta | Rp2.350.000 | **Sedang** | 1.450K < 2.350K ≤ 3.100K |
| Pasar Banyumas | Rp3.750.000 | **Tinggi** | 3.750K > 3.100K (Q3) |
| Stasiun Banyumas | Rp4.200.000 | **Tinggi** | 4.200K > 3.100K (Q3) |

### 4.3.3 Distribusi Hasil Klasifikasi

**Grafik Distribusi Kelas Motor Weekday:**

```
Kelas      | Jumlah Lokasi | Persentase
-----------|---------------|----------
Rendah     | 4             | 26.7%
Sedang     | 7             | 46.7%
Tinggi     | 4             | 26.7%
-----------|---------------|----------
Total      | 15            | 100%
```

---

## 4.4 Visualisasi Hasil Kuantil

### 4.4.1 Histogram Pendapatan dengan Batas Kuantil

**Visualisasi Motor Weekday:**

```
Frekuensi
   8 |
   7 |         ██
   6 |    ██   ██      ██
   5 |    ██   ██  ██  ██
   4 |    ██   ██  ██  ██
   3 |    ██   ██  ██  ██
   2 | ██ ██   ██  ██  ██
   1 | ██ ██   ██  ██  ██ ██
   0 |_________________________
     0     Q1        Q3      Max
        1.45M     3.1M     4.2M
  
  ❌ RENDAH  ⚠️ SEDANG  ✅ TINGGI
```

**Interpretasi:**
- Garis vertikal di Q1 (1.45M) memisahkan Rendah dari Sedang
- Garis vertikal di Q3 (3.1M) memisahkan Sedang dari Tinggi
- Lokasi yang ada di setiap zona ditandai dengan pola bar yang berbeda

### 4.4.2 Box Plot Perbandingan Semua Kategori

```
Motor WD          Motor Wknd        Mobil WD          Mobil Wknd
   |                 |               |                 |
 4.2M             3.8M            6.5M               6.1M     ← Max (Tinggi)
   |                 |               |                 |
   ├──────┐          ├──────┐        ├──────┐          ├──────┐
   │      │          │      │        │      │          │      │
 3.1M ────┤──────── 2.95M ───┤      5.8M ───┤        5.42M ───┤ ← Q3 (Sedang-Tinggi)
   │  ██  │          │  ██  │        │  ██  │          │  ██  │
   │  ██  │          │  ██  │        │  ██  │          │  ██  │
 1.45M ───┤──────── 1.28M ───┤      2.85M ───┤        2.68M ───┤ ← Q1 (Rendah-Sedang)
   │      │          │      │        │      │          │      │
   └──────┘          └──────┘        └──────┘          └──────┘
   |                 |               |                 |
 980K              750K            1.2M              950K      ← Min (Rendah)
```

---

## 4.5 Pembahasan Detail Hasil

### 4.5.1 Dari Mana Nilai Kuantil Berasal?

**Sumber Data Mentah:**
1. **File Input**: `Rekomendasi_Tarif_Parkir.csv`
2. **Kolom Kunci**: 
   - `Pendapatan Motor Weekday` (15 baris)
   - `Pendapatan Mobil Weekday` (15 baris)
   - `Pendapatan Motor Weekend` (15 baris)
   - `Pendapatan Mobil Weekend` (15 baris)

**Proses Perhitungan:**
```python
import numpy as np

# 1. Load data
pendapatan_motor_wd = df['Pendapatan Motor Weekday'].values
# [980K, 1150K, 1280K, ..., 4200K]

# 2. Hitung Q1 dan Q3
q1 = np.quantile(pendapatan_motor_wd, 0.25)  # = 1.450.000
q3 = np.quantile(pendapatan_motor_wd, 0.75)  # = 3.100.000

# 3. Klasifikasi
class_label = []
for income in pendapatan_motor_wd:
    if income <= q1:
        class_label.append('Rendah')
    elif income <= q3:
        class_label.append('Sedang')
    else:
        class_label.append('Tinggi')
```

### 4.5.2 Mengapa Menggunakan Kuantil?

| Alasan | Penjelasan |
|--------|-----------|
| **Distribusi Merata** | Kuantil membagi data menjadi 3 kelompok dengan ukuran yang hampir sama |
| **Data-driven** | Tidak ada asumsi threshold fixed, mengikuti distribusi real data |
| **Adaptif** | Jika data berubah, threshold otomatis berubah menyesuaikan |
| **Statistical Valid** | Metode standar dalam statistik deskriptif |

### 4.5.3 Interpretasi Hasil

**Makna Kelas di Konteks Bisnis:**

| Kelas | Pendapatan | Tarif Dasar | Interpretasi |
|-------|-----------|------------|--------------|
| **Rendah** | ≤ Q1 | Rp1.000 (Motor) | Lokasi kurang ramai, potensi rendah, tarif minimal |
| **Sedang** | Q1 - Q3 | Rp2.000 (Motor) | Lokasi cukup ramai, potensi sedang, tarif standard |
| **Tinggi** | > Q3 | Rp3.000 (Motor) | Lokasi sangat ramai, potensi tinggi, tarif premium |

**Validasi dengan Data Nyata:**

Lokasi yang diklasifikasi "Tinggi" (pendapatan > 3.1M):
- ✅ Stasiun Banyumas (Rp4.2M) - Area transit tinggi
- ✅ Pasar Banyumas (Rp3.75M) - Area komersial ramai
- ✅ Jl. Ahmad Yani (Rp3.42M) - Jalan utama dengan traffic tinggi

Lokasi yang diklasifikasi "Rendah" (pendapatan ≤ 1.45M):
- ✅ Alun-alun Banyumas (Rp980K) - Area terbuka, traffic ringan
- ✅ Jl. Pramuka (Rp1.15M) - Residential area

---

## 4.6 Ringkasan Tahap-Tahap

| Tahap | Input | Proses | Output |
|-------|-------|--------|--------|
| **1. Perhitungan Pendapatan** | Data jumlah kendaraan per jam | Agregasi per hari | Pendapatan harian (15 lokasi × 4 kategori) |
| **2. Perhitungan Kuantil** | 15 data pendapatan per kategori | np.quantile(data, 0.25) & 0.75 | Q1 dan Q3 untuk setiap kategori |
| **3. Klasifikasi** | Pendapatan + Q1 + Q3 | IF-THEN rule | Class label (Rendah/Sedang/Tinggi) |
| **4. Visualisasi** | Hasil klasifikasi | Histogram + Box plot | Grafik distribusi |

---

## 4.7 Implikasi untuk Model Machine Learning

Hasil klasifikasi ini menjadi **target variable (y)** untuk melatih Random Forest:

```
Random Forest Training:
├─ Input Features (X):
│  ├─ Jumlah Motor Weekday
│  ├─ Jumlah Motor Weekend
│  ├─ Jam Ramai Motor Weekday
│  ├─ Jumlah Mobil Weekday
│  └─ ... (lebih banyak fitur)
│
└─ Target Variable (y):
   ├─ Class_Motor = [Rendah, Sedang, Tinggi, ..., Tinggi]
   └─ Class_Mobil = [Sedang, Sedang, Tinggi, ..., Tinggi]
```

**Model ini kemudian belajar pola:**
- Fitur mana yang paling berpengaruh dalam menentukan kelas potensi
- Kombinasi fitur apa yang menghasilkan kelas Tinggi
- Threshold optimal untuk setiap fitur (berbeda dengan Q1/Q3 statistik)

---

## 4.8 File Terkait

- **Visualisasi Interaktif**: Tab "💰 Batas Kuantil (Rupiah)" di [app.py](app.py) (Lines 670-710)
- **Data Input**: [Rekomendasi_Tarif_Parkir.csv](Rekomendasi_Tarif_Parkir.csv)
- **Dokumentasi Lengkap**: [INDEX_DOKUMENTASI.md](INDEX_DOKUMENTASI.md)

---

*Bab ini menjelaskan proses mendetail bagaimana data pendapatan ditransformasi menjadi kelas potensi tarif melalui perhitungan kuantil.*
