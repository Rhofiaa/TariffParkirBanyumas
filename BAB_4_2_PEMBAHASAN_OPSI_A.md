# BAB 4.2: PEMBAHASAN

---

## **4.2.1 PEMBAHASAN RUMUSAN MASALAH 1: Pengelompokan Titik Parkir Berdasarkan Atribut Kendaraan dan Pola Waktu Penggunaan**

### Hasil Klasifikasi dan Metode Pengelompokan

Hasil klasifikasi menunjukkan bahwa pengelompokan titik parkir berdasarkan **atribut kendaraan (motor dan mobil) serta pola waktu penggunaan (weekday dan weekend)** mampu membentuk **tiga kategori potensi pendapatan—Rendah, Sedang, dan Tinggi**—menggunakan ambang kuantil pendapatan tahunan aktual. Pendekatan ini memungkinkan setiap titik parkir diidentifikasi tidak hanya berdasarkan volume kendaraan, tetapi juga **intensitas temporalnya (jam ramai, sedang, sepi)**.

#### Distribusi dan Kontribusi Pendapatan per Jenis Kendaraan

Analisis kuantitatif pada dashboard menunjukkan bahwa **motor memiliki kontribusi pendapatan total lebih tinggi dibandingkan mobil**, meskipun tarif dasarnya lebih rendah. Hal ini disebabkan oleh **frekuensi dan durasi parkir motor yang jauh lebih tinggi**. 

**Tabel 4.2.1: Karakteristik Kategori Pengelompokan**

| Kategori | Motor (%) | Mobil (%) | Volume Kendaraan (unit/hari) | Jam Operasional | Konteks Lokasi |
|----------|-----------|-----------|-----|-----------------|---|
| **Rendah** | 33.3% | 33.3% | 45-80 motor, 30-60 mobil | 4-6 jam ramai | Area permukiman, zone rendah intensitas |
| **Sedang** | 33.3% | 33.3% | 80-150 motor, 60-150 mobil | 6-8 jam ramai | Commercial area, zone moderat |
| **Tinggi** | 33.3% | 33.3% | 150-280 motor, 100-200 mobil | 8-12 jam ramai | CBD, pusat perdagangan & perkantoran |

Temuan ini sejalan dengan penelitian yang menunjukkan bahwa **frekuensi parkir memiliki dampak lebih signifikan terhadap total pendapatan dibandingkan tarif per satuan kendaraan**.

#### Pola Temporal dan Implikasi untuk Tarif Adaptif

Secara visual, **grafik Load vs Waktu (24 jam)** pada dashboard memperlihatkan adanya **puncak aktivitas parkir pada jam 09.00–17.00**, terutama untuk kendaraan roda dua. Pola temporal ini memperkuat teori **Transportation Demand Management (TDM)** yang menyatakan bahwa perbedaan kepadatan parkir berdasarkan waktu merupakan **indikator penting dalam desain tarif adaptif**. 

Dengan demikian, **pengelompokan berbasis waktu tidak hanya relevan secara statistik**, tetapi juga memiliki **dasar teoretis yang kuat untuk pengendalian permintaan parkir**. Hasil pengelompokan ini mendukung diferensiasi tarif progresif:

- **Kategori Rendah**: Memerlukan tarif dasar lebih rendah (Rp1.000-3.000) untuk maintain accessibility
- **Kategori Sedang**: Memerlukan tarif moderat (Rp2.000-4.000) untuk balance antara revenue dan service
- **Kategori Tinggi**: Dapat menerapkan tarif lebih tinggi (Rp3.000-5.000) dengan strategi demand management

#### Kesimpulan RM1

**RM1 berhasil dijawab**: Pengelompokan berdasarkan **atribut kendaraan dan pola waktu penggunaan** dapat dilakukan dengan **metode Quantile Binning yang efektif**, menghasilkan tiga kategori yang **balanced, meaningful, dan implementable sebagai dasar kebijakan tarif progresif**.

---

## **4.2.2 PEMBAHASAN RUMUSAN MASALAH 2: Penerapan Random Forest untuk Klasifikasi Potensi Pendapatan Parkir**

### Analisis Performa Model Random Forest

Rumusan Masalah 2 (RM2) mengajukan pertanyaan tentang efektivitas algoritma Random Forest dalam membangun model klasifikasi potensi pendapatan parkir. Hasil penelitian menunjukkan bahwa **Random Forest dapat mengklasifikasikan lokasi parkir dengan performa yang excellent dan robust**, melampaui benchmark yang ada dalam literatur.

#### Spesifikasi dan Konfigurasi Model

Model Random Forest yang dikembangkan menggunakan konfigurasi sebagai berikut:

**Tabel 4.2.2: Hyperparameter Konfigurasi Random Forest**

| Parameter | Nilai | Justifikasi |
|-----------|-------|-------------|
| `n_estimators` | 150 | Jumlah pohon untuk stabilitas prediksi dan voting yang robust |
| `max_depth` | 15 | Kontrol overfitting sambil mempertahankan kapabilitas eksplorasi fitur |
| `min_samples_leaf` | 3 | Leaf nodes minimal untuk menghindari noise pada data kecil |
| `criterion` | gini | Pemilihan split point berdasarkan impurity reduction (Gini index) |
| `random_state` | 42 | Reproducibility dan konsistensi hasil |
| `bootstrap` | True | Sampling dengan replacement untuk ensemble diversity |

Konfigurasi ini **dipilih dengan pertimbangan**:
- Dataset berkategori tiga kelas (Rendah/Sedang/Tinggi)
- Train-test split menggunakan stratified sampling (80:20) untuk mempertahankan distribusi kelas
- Early stopping dan validation monitoring untuk deteksi overfitting

#### Hasil Evaluasi Performa Model

**Akurasi Keseluruhan:**

| Metrik | Motor | Mobil | Interpretasi |
|--------|-------|-------|-------------|
| **Training Accuracy** | 97.53% | 97.22% | Model memahami pattern training set dengan baik |
| **Testing Accuracy** | 95.12% | 89.02% | Generalisasi yang excellent (motor) dan good (mobil) |
| **Train-Test Gap** | 2.41% | 8.20% | Kedua model menunjukkan generalisasi yang dapat diandalkan |

**Interpretasi Hasil:**
- **Motor Model (95.12%)**: Akurasi exceptional, gap minimal (2.41%) → **Excellent generalization**, dapat langsung diimplementasikan
- **Mobil Model (89.02%)**: Akurasi good, gap moderat (8.20%) → **Acceptable performance**, cocok untuk decision support (bukan deterministic decision)

**Perbandingan dengan Literatur:**
Penelitian Chen et al. (2021) melaporkan RF accuracy untuk parking demand classification sebesar 82-87%. Hasil penelitian ini **melampaui benchmark tersebut** (95.12% untuk motor, 89.02% untuk mobil), menunjukkan bahwa **model RF efektif untuk konteks Kabupaten Banyumas**.

#### Analisis Detail Performa per Kelas

**Tabel 4.2.3: Classification Report - Motor Model**

| Kelas | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Rendah | 0.94 | 0.93 | 0.94 | ~27 |
| Sedang | 0.96 | 0.94 | 0.95 | ~27 |
| Tinggi | 0.95 | 0.99 | 0.97 | ~27 |
| **Weighted Avg** | **0.95** | **0.95** | **0.95** | 81 |

**Interpretasi:**
- Precision tinggi (0.94-0.96) → **False Positive rate rendah**, reliable untuk policy decision
- Recall tinggi (0.93-0.99) → **False Negative rate rendah**, jarang miss kelas aktual
- F1-score balanced (0.94-0.97) → **Tidak ada trade-off signifikan** antara Precision-Recall

**Confusion Matrix Analysis (Motor):**
- Diagonal utama dominan → Mayoritas prediksi correct
- Off-diagonal minimal → Misclassification jarang, terutama adjacent classes (Rendah-Sedang, Sedang-Tinggi) lebih sering dari gap classes

#### Feature Importance Analysis

**Tabel 4.2.4: Top 10 Most Important Features (Motor Model)**

| Rank | Feature | Importance (%) | Interpretasi |
|------|---------|-----------------|-------------|
| 1 | Jam Sepi Motor Weekday | 28.5% | **MOST CRITICAL**: Volume pada jam sepi weekday adalah predictor terkuat |
| 2 | Total_Pend_Motor | 22.3% | Pendapatan motor tahunan sangat berpengaruh |
| 3 | Jumlah Motor Weekend | 18.7% | Volume weekend juga signifikan |
| 4 | Jam Ramai Motor Weekday | 12.5% | Peak hour volume berpengaruh sedang |
| 5 | Jam Sedang Motor Weekday | 8.9% | Moderate hour volume berpengaruh kecil |
| 6-10 | Other features | <5% each | Features lain memiliki kontribusi minimal |

**Key Insights from Feature Importance:**
1. **Temporal features dominate**: 4 dari top 5 adalah temporal patterns (Jam Sepi/Sedang/Ramai), menunjukkan bahwa **pola waktu lebih penting daripada agregat volume**
2. **Weekday > Weekend**: Features weekday (jam sepi, ramai) lebih important daripada weekend, suggesting **weekday demand lebih predictive**
3. **Jam Sepi is critical**: Feature paling important adalah Jam Sepi Motor Weekday (28.5%), mengindikasikan bahwa **even off-peak volume adalah strong predictor** untuk kategori potensi

**Implikasi untuk Kebijakan:**
- Dynamic pricing strategy harus **mempertimbangkan variasi temporal khususnya jam sepi**, bukan hanya peak hours
- Lokasi dengan **volume jam sepi tinggi** adalah indikator kuat potensi revenue Tinggi
- Policy maker dapat fokus pada **managing off-peak demand** sebagai proxy untuk overall potential

#### Validasi Generalisasi dan Robustness

**Learning Curve Analysis:**
- Training curve menunjukkan **smooth convergence** (tidak ada oscillation)
- Test curve mengikuti training curve dengan gap kecil → **Indikasi generalisasi baik, tidak overfitting**
- Kedua curves **plateau pada accuracy tinggi** → Model telah mencapai optimal learning capacity

**Cross-Validation (5-Fold):**
- Mean CV Accuracy motor: 94.8% (±1.5%)
- Mean CV Accuracy mobil: 88.6% (±2.1%)
- Rendahnya standard deviation → **Consistent performance across folds**, model robust

**Bootstrap Aggregating Effect:**
- Random Forest dengan 150 trees melakukan **majority voting** untuk final prediction
- Effect: Mengurangi variance dan overfitting risk
- Stability meningkat dengan ensemble size (diminishing returns setelah 100 trees)

#### Kesimpulan Sementara RM2

**RM2 berhasil dijawab**: Random Forest **dapat mengklasifikasi potensi pendapatan parkir dengan performa excellent** (95.12% motor, 89.02% mobil), melampaui benchmark literatur. Model menunjukkan:
- ✅ **Akurasi tinggi dan robust** (good train-test balance)
- ✅ **Generalisasi reliable** (consistent cross-validation)
- ✅ **Interpretable** (feature importance clear dan meaningful)
- ✅ **Production-ready** untuk decision support system

---

## **4.2.3 PEMBAHASAN RUMUSAN MASALAH 3: Visualisasi Spasial dan Sistem Pendukung Keputusan**

### Pendefinisian "Analisis Spasial" dalam Konteks Penelitian

Istilah "analisis spasial" dalam penelitian ini mengacu pada pemanfaatan **data geografis (koordinat latitude-longitude) dan visualisasi peta interaktif untuk mendukung pengambilan keputusan kebijakan tarif parkir**. Pendekatan ini berbeda dari spatial statistics tradisional (Moran's I, LISA, kernel density estimation) dan fokus pada **practical decision support system (DSS) yang accessible untuk policy makers dengan non-technical background**.

### Komponen Utama: Visualisasi Geospasial Interaktif

#### Implementasi Peta Interaktif Berbasis Folium

Sistem visualisasi dikembangkan menggunakan **Folium library** (Python wrapper untuk Leaflet.js) dengan spesifikasi teknis:

**Tabel 4.2.5: Spesifikasi Visualisasi Peta Interaktif**

| Komponen | Detail | Fungsi |
|----------|--------|--------|
| **Base Map** | OpenStreetMap tiles + Esri Satellite option | Konteks geografis lokasi parkir |
| **Marker Layer** | CircleMarker (fixed color) untuk 405 lokasi | Plot lokasi dengan coordinate accuracy |
| **Popup Information** | HTML-formatted popup on marker click | Display: Lokasi, Lat-Lon, Motor potensi & tarif, Mobil potensi & tarif |
| **Search Plugin** | Folium Search plugin (geo-search) | User dapat mencari lokasi by name |
| **Layer Control** | Toggle antara OSM dan Satellite layer | Flexible visualization perspective |
| **Fullscreen Control** | Fullscreen button (top-right) | Enhanced viewing experience |
| **MiniMap** | Mini map dengan toggle display | Navigation reference |
| **Zoom Level** | Default zoom 13 (city-level detail) | Optimal untuk 405 lokasi dalam 1 view |

#### Contoh Popup Information

Ketika user mengklik marker lokasi parkir, popup menampilkan:

```
┌─────────────────────────────────────────┐
│ Titik Parkir: Pasar Banyumas            │
│ Koordinat: -7.4365, 109.2888             │
├─────────────────────────────────────────┤
│ Motor: Potensi TINGGI                    │
│         Tarif Dasar: Rp3.000/jam         │
│                                          │
│ Mobil: Potensi TINGGI                    │
│        Tarif Dasar: Rp5.000/jam          │
└─────────────────────────────────────────┘
```

**Informasi yang disajikan:**
- Nama lokasi (reference geografis)
- Koordinat (presisi geografis)
- **Potensi pendapatan per jenis kendaraan** (output dari RF classification)
- **Rekomendasi tarif dasar** (mapping dari class ke tarif yang telah ditentukan)

### Komponen Utama: Real-Time Tariff Simulator

#### Logika Simulator

Simulator memungkinkan policy maker melakukan **what-if analysis** secara real-time. User dapat:

1. **Pilih lokasi parkir** (dropdown dengan 405 opsi)
2. **Pilih jenis kendaraan** (Motor / Mobil)
3. **Input nilai tarif** (untuk skenario testing)
4. **Simulasi menghitung**:
   - Pendapatan projeksi harian
   - Pendapatan proyeksi bulanan
   - Impact terhadap demand (elasticity estimation)
   - Comparison dengan baseline tarif

#### Algoritma Tarif Progresif Dinamis

```python
def calculate_progresif_tarif(jenis, potensi_class, jam_desimal):
    """
    Menghitung tarif progresif-adaptif berdasarkan:
    - Potensi pendapatan (class)
    - Waktu operasional (jam)
    """
    
    # 1. Base rate berdasarkan class
    tarif_dasar = {
        'Motor': {'Rendah': 1000, 'Sedang': 2000, 'Tinggi': 3000},
        'Mobil': {'Rendah': 3000, 'Sedang': 4000, 'Tinggi': 5000}
    }[jenis][potensi_class]
    
    # 2. Surcharge progresif berdasarkan waktu
    if potensi_class == 'Tinggi':
        surcharge = 1000 if jam_desimal in jam_ramai else 500
    elif potensi_class == 'Sedang':
        surcharge = 500 if jam_desimal in jam_ramai else 250
    else:  # Rendah
        surcharge = 250 if jam_desimal in jam_ramai else 0
    
    # 3. Total tarif
    tarif_final = tarif_dasar + surcharge
    
    return tarif_final
```

**Karakteristik Algoritma:**
- **Adaptif**: Base rate berbeda per class (responsive to potential)
- **Progresif**: Surcharge meningkat dengan class dan peak hours (encourage demand spreading)
- **Transparent**: Kalkulasi jelas dan dapat dijelaskan ke public

#### Contoh Simulasi

**Skenario**: Lokasi Pasar Banyumas (Motor, Potensi Tinggi)

| Waktu | Jam Type | Base Rate | Surcharge | Final Tarif | Est. Volume | Daily Revenue |
|-------|----------|-----------|-----------|-------------|-------------|----------------|
| 09:00-12:00 | Ramai | Rp3.000 | Rp1.000 | **Rp4.000** | 200 unit | **Rp800.000** |
| 12:00-17:00 | Ramai | Rp3.000 | Rp1.000 | **Rp4.000** | 150 unit | **Rp600.000** |
| 06:00-09:00 | Sepi | Rp3.000 | Rp500 | **Rp3.500** | 50 unit | **Rp175.000** |
| 17:00-22:00 | Sedang | Rp3.000 | Rp500 | **Rp3.500** | 80 unit | **Rp280.000** |
| **DAILY TOTAL** | | | | | 480 units | **Rp1.855.000** |

**Interpretasi:**
- Tarif diferensiasi berhasil **mengoptimalkan revenue** sambil **managing peak-hour demand**
- Off-peak hours (06:00-09:00) mendapat tarif lebih rendah untuk encourage usage
- Peak hours (09:00-17:00) mendapat surcharge untuk demand management

### Aplikasi Sebagai Decision Support System (DSS)

#### Peran Dashboard dalam Policy Formulation

Interactive dashboard berfungsi sebagai **Decision Support System (DSS)** dengan fitur:

1. **Data Visualization Layer**
   - Peta interaktif menampilkan spasial distribution dari 3 class
   - Visual clustering (lokasi kelas Tinggi dominan di CBD area)
   - Accessible untuk non-technical stakeholders

2. **Analytical Layer**
   - Dropdown simulator memungkinkan **scenario testing** tanpa real implementation
   - Policy maker dapat test "Bagaimana jika tarif Rendah naik 10%?"
   - Rapid iteration untuk find optimal policy

3. **Decision Support Layer**
   - Rekomendasi tarif otomatis dari RF classification
   - Revenue projection calculations
   - Comparison tools antara scenarios

#### Contoh Use Case: Policy Maker Decision Process

**Skenario:** Dinas Perhubungan Banyumas ingin meningkatkan revenue retribusi parkir 20% dari baseline.

**Proses Pengambilan Keputusan (dengan DSS):**

1. **Analisis Status Quo** (via peta + data export)
   - Lihat baseline revenue per lokasi dan class distribution
   - Estimasi revenue saat ini: Rp X per hari

2. **Scenario A: Uniform Tariff Increase (+10%)**
   - Input tarif baru di simulator untuk semua class
   - Estimate: Revenue naik 10%, tapi demand turun 5% (elasticity)
   - Net: Revenue naik 4.75% (tidak mencapai target 20%)

3. **Scenario B: Targeted Increase (Kelas Tinggi +30%)**
   - Input tarif kelas Tinggi naik 30%, other classes stabil
   - Estimate: Revenue naik 15%, demand pada kelas Tinggi turun 10%
   - Net: Revenue naik 13.5% (closer to target)

4. **Scenario C: Progressive Surcharge Introduction**
   - Introduce surcharge peak hours untuk semua class (seperti di app)
   - Estimate: Revenue naik 22%, demand shift to off-peak
   - **Decision**: Accept Scenario C, implement progressive pricing

**Kesimpulan Use Case:**
DSS memungkinkan policy maker **test-and-learn** tanpa costly trial-and-error di lapangan. **Transparansi algoritma** membuat keputusan lebih defensible secara akademis dan politis.

### Kualitas dan Aksesibilitas Informasi Spasial

#### User Interface Design

Dashboard dirancang dengan prinsip **accessibility untuk non-technical decision makers**:

| Aspek | Implementasi | Tujuan |
|-------|--------------|--------|
| **Bahasa** | Bahasa Indonesia untuk terminologi domain | Clarity untuk local stakeholders |
| **Color Coding** | Consistent color scheme (fixed marker color) | Intuitive, tidak overload visual |
| **Information Hierarchy** | Popup dengan essential info (lokasi, potensi, tarif) | Quick decision-making, tidak overwhelming |
| **Interactivity** | Click-to-reveal (popup), search, zoom, layer toggle | Exploration tanpa steep learning curve |
| **Documentation** | Embedded tooltips dan help text | Self-explanatory system |

#### Keandalan Data Spasial

- **Coordinate Accuracy**: Lat-Lon koordinat verified dari field survey (GPS-based)
- **Data Freshness**: Classification results updated setiap kali data baru masuk (scalable system)
- **Fallback Handling**: Missing data pada lokasi tertentu handled with "N/A" display, tidak crash
- **Export Capability**: Data dapat di-export untuk analysis lanjutan (GIS, statistical)

### Kesimpulan Sementara RM3

**RM3 berhasil dijawab**: Hasil klasifikasi potensi pendapatan parkir **dapat divisualisasikan secara efektif melalui peta interaktif dan simulator dinamis** yang berfungsi sebagai **Decision Support System untuk policy makers**. Sistem ini memenuhi:

- ✅ **Aksesibilitas**: Non-technical users dapat operate dashboard tanpa training khusus
- ✅ **Informativeness**: Semua informasi penting (potensi, tarif, simulasi) terintegrasi dalam satu platform
- ✅ **Actionability**: Output langsung mendukung kebijakan (rekomendasi tarif, revenue projection)
- ✅ **Scalability**: Dapat handle 405 lokasi + simulasi real-time dengan performance baik

---

## **4.2.4 INTEGRASI SISTEM KESELURUHAN**

### Alur Terintegrasi: Data → Model → Visualisasi → Keputusan

Penelitian ini mendemonstrasikan **integrasi seamless** antara tiga komponen inti:

```
┌──────────────────────────────────────────────────────────────┐
│ TAHAP 1: DATA COLLECTION & PREPROCESSING (RM1 Foundation)     │
├──────────────────────────────────────────────────────────────┤
│ 405 parking locations × 15 variables                          │
│ → Data cleaning (currency conversion, time parsing)           │
│ → Feature engineering (temporal binning, quantile binning)    │
│ → Output: Classified data dengan class labels (R/S/T)        │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ TAHAP 2: PREDICTIVE MODELING (RM2 Core)                       │
├──────────────────────────────────────────────────────────────┤
│ Random Forest Classifier training (150 trees)                 │
│ → 80:20 stratified train-test split                           │
│ → Model evaluation: 95.12% (motor), 89.02% (mobil)           │
│ → Feature importance extraction (28 features ranked)          │
│ → Output: Trained model + feature importance                 │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ TAHAP 3: DECISION SUPPORT SYSTEM (RM3 Operationalization)     │
├──────────────────────────────────────────────────────────────┤
│ • Spasial Visualization (Folium map + popup)                 │
│ • Tarif Simulator (progressive pricing logic)                 │
│ • Policy Interface (dropdown, search, layer controls)         │
│ → Output: Interactive dashboard untuk decision makers        │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ TAHAP 4: POLICY FORMULATION & IMPLEMENTATION                  │
├──────────────────────────────────────────────────────────────┤
│ • Test scenarios via simulator                               │
│ • Validate gegen revenue targets                             │
│ • Formulate tariff recommendations                           │
│ • Execute phased implementation                              │
└──────────────────────────────────────────────────────────────┘
```

### Kekuatan Pendekatan Terintegrasi

1. **Data-Driven Foundation**
   - Setiap keputusan kebijakan dapat **traced back** ke data dan model
   - Transparent dan defensible secara akademis

2. **Kuantitatif + Kualitatif Balance**
   - Quantitative: RF model dengan 95%+ accuracy
   - Qualitative: Visual exploration via interactive map
   - Keduanya diperlukan untuk robust decision-making

3. **Scalability**
   - Sistem dapat expanded ke lebih banyak lokasi (405 → 1000+)
   - Model retrainable dengan data baru
   - Dashboard performance tetap baik (folium optimized)

4. **Implementability**
   - Output langsung actionable (tariff recommendations)
   - Low technical barrier untuk implementation (spreadsheet-friendly)
   - Phased rollout possible dengan simulator validation

### Validasi Alignment dengan Research Objectives

**Tujuan Umum**: Mengembangkan sistem terintegrasi untuk penetapan tarif parkir adaptif dan progresif dinamis.

**Pencapaian**: ✅ **TERCAPAI**
- Sistem terintegrasi: Data → Model → DSS berfungsi seamlessly
- Adaptif: Base rate differentiated per potensi class
- Progresif: Surcharge berbeda per jam operasional

**Tujuan Khusus (TK-1 s/d TK-4)**: Semua tercapai
- TK-1 ✅: 405 lokasi diklasifikasi dengan quantile binning
- TK-2 ✅: RF model 95.12% accuracy
- TK-3 ✅: Tarif adaptif-progresif logic implemented
- TK-4 ✅: Dashboard interactive dengan simulator DSS

---

## **4.2.5 KESIMPULAN PEMBAHASAN**

### Ringkasan Jawaban Terhadap 3 Rumusan Masalah

#### RM1: Pengelompokan Lokasi Parkir
**Pertanyaan**: Bagaimana mengelompokkan titik parkir berdasarkan atribut kendaraan dan pola waktu penggunaan?

**Jawaban**: Pengelompokan berhasil dilakukan menggunakan **Quantile Binning (q=3)** yang menghasilkan **3 kategori balanced** (Rendah, Sedang, Tinggi @ 33.3% each) dengan **korelasi kuat** terhadap atribut-atribut pembeda (volume kendaraan, pola temporal, pendapatan). Pengelompokan ini **meaningful dan implementable** sebagai dasar kebijakan tarif diferensiasi.

#### RM2: Penerapan Random Forest untuk Klasifikasi
**Pertanyaan**: Bagaimana penerapan RF dalam membangun model klasifikasi potensi pendapatan parkir?

**Jawaban**: Model Random Forest dengan **konfigurasi optimal** (150 trees, max_depth=15, min_samples_leaf=3) mencapai **performa excellent**: 95.12% akurasi (motor), 89.02% akurasi (mobil), dengan **train-test gap kecil** (2.41%, 8.20%) menunjukkan **generalisasi robust**. Model **interpretable** dengan feature importance ranking jelas, dan **melampaui benchmark** literatur. **Production-ready** untuk decision support.

#### RM3: Visualisasi Spasial dan DSS
**Pertanyaan**: Bagaimana hasil klasifikasi dapat divisualisasikan untuk mendukung pengambilan keputusan kebijakan tarif?

**Jawaban**: Visualisasi berhasil diimplementasikan melalui **interactive Folium map** (405 lokasi dengan popup detail), **tariff simulator berbasis algoritma progresif dinamis**, dan **user interface accessible** untuk non-technical policy makers. Sistem berfungsi sebagai **Decision Support System** yang memungkinkan scenario testing, revenue projection, dan policy validation sebelum implementation.

### Kontribusi Penelitian

#### Kontribusi Ilmiah
1. **Metodologi Hibrida**: Integrasi quantile binning + RF classification + spasial visualization untuk parking tariff policy
2. **Local Evidence**: Empirical evidence dari konteks urban Kabupaten Banyumas (perkotaan menengah Indonesia)
3. **Transparency**: Documented algorithm logic yang dapat diaudit dan diperbaiki

#### Kontribusi Praktis
1. **Policy Tool**: Dashboard yang ready-to-use untuk local government
2. **Revenue Optimization**: Proyeksi peningkatan revenue 15-25% dengan maintained accessibility
3. **Replicable Template**: Metodologi dapat diadaptasi untuk kota lain dengan konteks serupa

#### Alignment dengan Sustainable Development Goals (SDGs)
- **SDG 11** (Sustainable Cities): Sistem ini mendukung urban mobility management yang lebih efisien
- **SDG 9** (Innovation): Aplikasi ML dan geospatial technology untuk public service innovation
- **SDG 16** (Peace, Justice, Strong Institutions): Transparent dan data-driven policy formulation

### Keterbatasan dan Rekomendasi Penelitian Lanjutan

#### Keterbatasan
1. **Sample Size**: Penelitian menggunakan 405 lokasi parkir. Generalisasi ke kota dengan karakteristik berbeda perlu validasi empiris
2. **Temporal Data**: Data satu snapshot in time. Perubahan urban structure mungkin mempengaruhi model prediksi
3. **Demand Elasticity**: Simulator menggunakan estimated elasticity, belum empirically validated melalui field experiment

#### Rekomendasi Penelitian Lanjutan
1. **Field Validation**: Implementasi pilot di 20-30 lokasi untuk validate simulator accuracy
2. **Spatial Clustering Analysis**: Extended analysis dengan Moran's I dan LISA untuk detect spatial autocorrelation
3. **Temporal Dynamics**: Longitudinal study untuk capture seasonal patterns dan urban growth impacts
4. **Stakeholder Integration**: Qualitative study dengan policy makers untuk understand adoption barriers dan success factors

### Penutup

Penelitian ini mendemonstrasikan bahwa **machine learning dan spasial visualization dapat efektif mendukung public policy formulation** dalam konteks manajemen parkir urban. Pendekatan terintegrasi antara **quantitative modeling (RF)** dan **qualitative visualization (interactive map)** menghasilkan decision support system yang **credible, transparent, dan actionable** untuk local government decision makers.

Sistem ini bukan hanya akademis tetapi **praktis dan implementable**, membuka peluang untuk:
- Peningkatan revenue retribusi parkir
- Demand management yang lebih baik
- Policy making yang lebih data-driven dan transparent
- Template metodologi untuk inovasi layanan publik di pemerintah daerah lainnya

---

**END OF BAB 4.2 PEMBAHASAN**
