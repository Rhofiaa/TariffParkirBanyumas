# BAB 1: PENDAHULUAN

---

## 1.1 Latar Belakang

Kabupaten Banyumas sebagai pusat perkotaan di wilayah Jawa Tengah mengalami peningkatan volume kendaraan yang signifikan seiring dengan pertumbuhan ekonomi dan mobilitas penduduk. Analisis Data Pusat Statistik Indonesia (BPS) menunjukkan peningkatan rata-rata 8-12% per tahun dalam jumlah kendaraan bermotor di area urban Banyumas, dengan distribusi yang tidak merata di berbagai zona geografis (transit hub, pusat bisnis, area residensial).

### 1.1.1 Dinamika Parkir di Kabupaten Banyumas

Sistem manajemen parkir di Kabupaten Banyumas saat ini masih menggunakan model **tarif flat-rate** (tarif datar) yang tidak membedakan karakteristik lokasi atau waktu parkir. Kondisi ini menyebabkan beberapa masalah:

1. **Inefisiensi Spasial**: Tarif yang sama di semua lokasi tidak mencerminkan perbedaan potensi revenue dan demand karakteristik antara:
   - **Central Business District (CBD)** dengan volume kendaraan tinggi (200-280 unit/hari)
   - **Commercial Corridors** dengan volume sedang (80-150 unit/hari)
   - **Peripheral Areas** dengan volume rendah (< 80 unit/hari)

2. **Manajemen Permintaan Suboptimal**: Tarif statis tidak mampu mengelola congestion pada jam puncak (peak hours 09:00-17:00) saat kapasitas parkir mencapai titik jenuh, sementara jam non-puncak (sebelum 09:00) memiliki tingkat occupancy rendah.

3. **Pendapatan Retribusi Suboptimal**: Potensi revenue dari tarif yang lebih diferensiasi tidak digali. Analisis awal menunjukkan bahwa:
   - Lokasi high-demand (e.g., Pasar Banyumas, Stasiun) dengan volume 280 motor/hari diperlakukan sama dengan area residential dengan 45 unit/hari
   - Gap revenue potential antara lokasi terbaik dan terburuk mencapai 6x lipat, tetapi struktur tarif tidak memanfaatkan ini

### 1.1.2 Kemajuan Teknologi dalam Manajemen Parkir

Penelitian terkini dalam **Transportation Demand Management (TDM)** telah menunjukkan bahwa pendekatan **dynamic progressive pricing** terbukti efektif dalam:
- Mengurangi waktu pencarian parkir (parking search time) hingga 30% [3]
- Meningkatkan occupancy rate optimal (65-85%) [4]
- Mendorong public transportation usage melalui demand elasticity [5]
- Meningkatkan revenue 15-25% dengan maintained service accessibility [6]

Teknologi **Machine Learning**, khususnya algoritma **Random Forest**, telah banyak diterapkan dalam:
- Prediksi demand dinamis untuk parkir [7]
- Classifikasi potensi revenue berdasarkan karakteristik lokasi [8]
- Optimisasi pricing strategy dengan multiple constraints [9]

Analisis spasial menggunakan **Geographic Information System (GIS)** dan pemetaan web interaktif (Folium, Leaflet) memungkinkan visualisasi spatial clustering dan decision support yang lebih baik untuk implementasi kebijakan geografis.

### 1.1.3 Gap Penelitian di Konteks Lokal

Meskipun teori dan teknik tersedia, **di konteks Kabupaten Banyumas masih belum ada penelitian yang mengintegrasikan**:

1. **Data Mining + Machine Learning** untuk klasifikasi potensi tarif berbasis karakteristik lokal
2. **Analisis temporal (weekday/weekend, jam puncak)** dengan spatial clustering untuk policy differentiation
3. **Progressive pricing mechanism** yang adaptif terhadap kondisi lokal dan implementasi practical dalam bentuk **decision support system (dashboard)**
4. **Validasi dampak revenue dan demand management** melalui systematic modeling

Hal ini menciptakan opportunity untuk melakukan penelitian yang komprehensif dan praktis.

### 1.1.4 Motivasi Penelitian

Penelitian ini dimotivasi oleh kebutuhan untuk:

1. **Meningkatkan efisiensi manajemen parkir** melalui tarif yang lebih responsif terhadap demand spatial dan temporal
2. **Mengoptimalkan revenue retribusi** tanpa mengurangi accessibility untuk area low-demand
3. **Mendemonstrasikan aplikasi ML dalam konteks policy making lokal** yang data-driven dan transparent
4. **Memberikan template metodologi** yang replicable untuk pemerintah daerah lain dengan karakteristik urban serupa

---

## 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah dipaparkan, penelitian ini difokuskan pada permasalahan berikut:

### RM1: Pengelompokan Titik Parkir (Clustering)
**Bagaimana mengelompokkan titik parkir berdasarkan atribut kendaraan dan pola waktu penggunaan untuk mendukung penentuan klasifikasi tarif progresif retribusi parkir?**

Submasalah:
- Variabel mana yang paling signifikan dalam membedakan karakteristik lokasi parkir?
- Berapa jumlah cluster optimal yang dapat didefinisikan dalam konteks Banyumas?
- Bagaimana validasi bahwa cluster yang dihasilkan meaningful dan implementable?

### RM2: Penerapan Random Forest (Classification Modeling)
**Bagaimana penerapan algoritma Random Forest dalam membangun model klasifikasi potensi pendapatan parkir sebagai dasar kebijakan tarif progresif?**

Submasalah:
- Hyperparameter apa yang optimal untuk Random Forest pada dataset kecil (15 lokasi)?
- Berapa accuracy dan robustness model yang dapat dicapai?
- Fitur mana yang paling berpengaruh terhadap prediksi potensi revenue?
- Apakah model ini dapat digeneralisasi atau spesifik konteks Banyumas?

### RM3: Visualisasi Spasial dan Sistem Pendukung Keputusan (Decision Support System)
**Bagaimana hasil klasifikasi potensi pendapatan parkir dapat divisualisasikan dalam peta interaktif dan simulator dinamis untuk mendukung pengambilan keputusan kebijakan tarif?**

Submasalah:
- Teknologi apa yang tepat untuk visualisasi spasial yang accessible dan user-friendly untuk decision maker?
- Bagaimana mengintegrasikan simulasi what-if tarif progresif dalam platform visualisasi interaktif?
- Bagaimana sistem ini memfasilitasi pengambilan keputusan kebijakan tarif yang berbasis data?
- Apakah informasi yang ditampilkan (potensi parkir, rekomendasi tarif, simulasi) cukup komprehensif untuk policy planning?

---

## 1.3 Tujuan Penelitian

Berdasarkan rumusan masalah di atas, tujuan penelitian ini adalah:

### Tujuan Umum
Mengembangkan **sistem terintegrasi untuk penetapan tarif parkir adaptif dan progresif dinamis** di Kabupaten Banyumas menggunakan kombinasi Data Mining, Machine Learning, dan Analisis Spasial.

### Tujuan Khusus

**TK-1: Pengelompokan Lokasi** (Menjawab RM1)
- Mengidentifikasi dan mengklasifikasikan 15 titik parkir di Banyumas menjadi kategori potensi tarif (Rendah, Sedang, Tinggi) menggunakan teknik **Quantile Binning** berdasarkan atribut volume kendaraan dan pola temporal
- Validasi pengelompokan dengan analisis deskriptif dan geographic context

**TK-2: Model Prediktif** (Menjawab RM2)
- Membangun model **Random Forest Classifier** untuk prediksi potensi tarif pada lokasi baru berdasarkan karakteristik vehicular dan temporal patterns
- Mencapai akurasi minimal 80% pada test set untuk reliable decision support
- Interpretasi feature importance untuk memahami drivers utama potensi revenue
- Evaluasi generalisasi model melalui cross-validation

**TK-3: Sistem Progressive Pricing** (Menjawab RM2 lanjutan)
- Merancang **logika tarif adaptif-progresif dinamis** yang:
  - Base rate differentiated per kelas potensi (Rendah/Sedang/Tinggi)
  - Surcharge yang bersifat progresif berdasarkan waktu (peak-hour pricing)
  - Demand-responsive dengan maintained accessibility untuk low-demand areas
- Proyeksikan dampak revenue dan demand management

**TK-4: Sistem Visualisasi Spasial dan Simulator Dinamis** (Menjawab RM3)
- Mengembangkan **interactive web-based decision support system** berbasis Streamlit dan Folium yang:
  - Visualisasi spasial 405 lokasi parkir dalam peta interaktif dengan coordinate-based marker placement
  - Display hasil klasifikasi potensi pendapatan per lokasi (Rendah/Sedang/Tinggi) dan rekomendasi tarif dasar
  - Implementasi real-time tariff simulator untuk what-if scenario analysis dengan dynamic pricing logic
  - User interface yang intuitif dan accessible untuk decision maker (non-technical background)
  - Integration dengan predictive model output untuk rekomendasi kebijakan yang data-driven

**TK-5: Policy Recommendation** (Outcome)
- Formulasi rekomendasi kebijakan tarif parkir yang data-driven untuk implementasi fase-bertahap
- Analisis feasibility implementasi dan potential barriers
- Template metodologi untuk replikasi di kota lain dengan konteks serupa

---

## 1.4 Manfaat Penelitian

### 1.4.1 Manfaat Teoritis

1. **Kontribusi ke Literatur Transportation Planning**
   - Demonstrasi integrasi Machine Learning + Spatial Analysis dalam TDM policy formulation
   - Empirical evidence pada konteks urban kecil-menengah (perkotaan Banyumas)
   - Framework untuk dynamic pricing implementation dalam konteks developing economy

2. **Metodologi Hibrida**
   - Kombinasi statistical quantile-based classification dengan predictive ML model
   - Best practice dalam handling small dataset (n=15 lokasi) dengan machine learning
   - Dokumentasi transparent dan reproducible untuk academic standards

3. **Feature Engineering untuk Parking Demand**
   - Eksplorasi variabel temporal (weekday/weekend, peak-hour) sebagai predictor
   - Spatial feature extraction dari geographic coordinates

### 1.4.2 Manfaat Praktis

#### Bagi Pemerintah Kabupaten Banyumas
- **Decision Support System** untuk penetapan tarif parkir yang optimal dan defensible
- **Data-driven policy** menggantikan pendekatan ad-hoc
- **Revenue optimization** dengan proyeksi peningkatan 15-25% tanpa mengurangi accessibility
- **Template implementasi** yang replicable untuk area parkir baru

#### Bagi Literatur Urban Management Lokal
- **Case study** penerapan advanced analytics dalam konteks pemerintah daerah
- **Best practice documentation** untuk digitalisasi manajemen parkir
- **Proof-of-concept** bahwa algoritma ML dapat accessible untuk policy makers non-technical

#### Bagi Penelitian Selanjutnya
- **Baseline model** untuk demand prediction yang lebih advanced
- **Integrated dataset** (15 lokasi × 4 kategori × multiple features) tersedia untuk public research
- **Framework scalability** untuk kota-kota serupa di Indonesia

### 1.4.3 Manfaat Sosial

1. **Efisiensi Transportasi**
   - Mengurangi waktu pencarian parkir (parking search time) melalui better demand management
   - Alokasi ruang parkir lebih optimal
   - Potentially encourage public transportation usage di area high-demand

2. **Equity dan Accessibility**
   - Low-demand areas tetap accessible dengan tarif reasonable (tidak dibebankan surcharge agresif)
   - Revenue dari high-demand zones dapat dialokasikan untuk infrastruktur di peripheral areas
   - Transparent pricing mechanism yang dapat dipahami semua stakeholder

3. **Governance**
   - Demonstrasi pemerintah dalam adopting evidence-based policy making
   - Transparency dalam pricing mechanism
   - Participation opportunity untuk community feedback melalui interactive dashboard

---

## 1.5 Batasan Masalah

Batasan masalah penelitian mencakup ruang lingkup, kondisi, dan asumsi yang telah ditetapkan untuk memastikan bahwa solusi yang dihasilkan relevan, feasible, dan dapat diimplementasikan. Batasan ditetapkan dengan mempertimbangkan kerasionalan terhadap keadaan sebenarnya di lapangan.

### 1.5.1 Batasan Geografis dan Administrasi

1. **Wilayah Penelitian**: Kabupaten Banyumas, khususnya titik-titik parkir di wilayah Purwokerto dan sekitarnya
   - Fokus pada area urban yang memiliki infrastruktur formal dan data terintegrasi
   - Tidak mencakup area rural atau area dengan sistem parkir informal yang tidak terdata

2. **Jumlah Lokasi Parkir**: 405 titik parkir berdasarkan Laporan Akhir Kajian Potensi Parkir Kabupaten Banyumas tahun 2023
   - Penelitian terbatas pada lokasi parkir yang tercatat secara resmi oleh BAPPEDALITBANG
   - Tidak termasuk parkir on-street informal atau parkir di area tidak terdaftar

### 1.5.2 Batasan Jenis Kendaraan

Penelitian mencakup **dua kategori kendaraan**:
- **Kendaraan Bermotor Roda Dua (Motor)**: mencakup sepeda motor, skuter, dan kendaraan roda dua bermotor lainnya
- **Kendaraan Bermotor Roda Empat (Mobil)**: mencakup mobil penumpang dan minibus

**Tidak termasuk**:
- Kendaraan berat (truk, bus besar)
- Kendaraan khusus (ambulans, kendaraan dinas pemerintah)
- Roda tiga dan kendaraan non-standar
- Kendaraan ramah lingkungan dengan insentif khusus

Pembatasan ini dilakukan karena kategori motor dan mobil merupakan mayoritas volume parkir di Kabupaten Banyumas (>95%) dan memiliki pola demand yang dapat dimodelkan.

### 1.5.3 Batasan Data dan Temporal

1. **Sumber Data**: Data sekunder dari BAPPEDALITBANG (2023) dan data primer koordinat geografis dari survei lapangan
   - Data historis (bukan real-time streaming atau forecast)
   - Periode observasi: 1 tahun (2023) untuk coverage seasonal

2. **Temporal Features**: Kategorisasi waktu berdasarkan pola demand lokal:
   - Jam Sepi: 00:00–06:00 dan 22:00–24:00
   - Jam Sedang: 06:00–08:00 dan 19:00–22:00
   - Jam Ramai: 08:00–19:00
   - Weekday/Weekend differentiation

**Asumsi**: Pola temporal yang diamati pada tahun 2023 diasumsikan tetap konsisten untuk periode implementasi awal. Variasi musiman atau event khusus tidak secara eksplisit dimodelkan.

### 1.5.4 Batasan Metode dan Model

1. **Algoritma Machine Learning**: Penelitian menggunakan **Random Forest Classifier** sebagai primary method
   - Tidak membandingkan secara mendalam dengan algoritma alternatif (SVM, Neural Network, Gradient Boosting)
   - Hyperparameter ditentukan berdasarkan best practice literature dan limited tuning

2. **Analisis Spasial**: Menggunakan visualisasi geografis dan spatial distribution mapping
   - **Tidak termasuk**: statistical spatial analysis (spatial autocorrelation, clustering coefficient), spatial econometric modeling, atau network analysis yang lebih advanced
   - Fokus pada pemetaan dan visualisasi interaktif untuk decision support, bukan analisis statistik spatial yang kompleks

3. **Penetapan Tarif**: Mengimplementasikan **adaptive base tariff + progressive time-based surcharge**
   - Tidak termasuk: dynamic real-time pricing berdasarkan real-time occupancy, machine learning-based price optimization dengan multiple constraints, atau complex revenue management algorithms

### 1.5.5 Batasan Implementasi Sistem

1. **Platform Dashboard**: Web-based Streamlit application
   - **Tidak termasuk**: Mobile application, edge computing, IoT integration, atau real-time sensor-based system

2. **Skalabilitas**: Sistem dirancang untuk 405 lokasi parkir di Kabupaten Banyumas
   - Tidak divalidasi untuk skalabilitas ke provinsi atau nasional tanpa modification
   - Implementasi diasumsikan di environment dengan infrastructure dan governance yang stabil

3. **User Interface**: Dashboard interaktif untuk administrator/decision maker
   - **Tidak termasuk**: fitur enforcement teknologi (automated toll collection, ANPR), integration dengan existing payment system, atau automated tariff adjustment

### 1.5.6 Batasan Analisis Dampak

Penelitian ini fokus pada:
- **Classification accuracy** dari model terhadap data testing
- **Feasibility implementasi** dari proposed tariff system
- **Illustrative scenarios** melalui simulation module

**Tidak termasuk**:
- Empirical field validation (A/B testing di lapangan)
- Long-term impact study terhadap actual revenue, demand behavior, atau modal shift
- Social welfare analysis atau equity impact assessment terhadap different user groups
- Behavioral economics analysis terhadap pricing elasticity

---

## 1.6 Ruang Lingkup Penelitian

### 1.6.1 Cakupan Geografis dan Temporal
- **Lokasi**: 15 titik parkir di Kabupaten Banyumas
- **Periode Data**: 1 tahun (2023) untuk coverage seasonal dan temporal
- **Coverage Temporal di Model**: Weekday/Weekend, peak-hour dan off-peak patterns

### 1.5.2 Cakupan Metodologis
- **Data Mining**: Preprocessing, cleaning, feature engineering
- **Statistical Analysis**: Quantile binning, descriptive statistics
- **Machine Learning**: Random Forest classifier dengan 80:20 train-test split
- **Spatial Analysis**: Clustering identification, geographic visualization
- **System Development**: Web-based dashboard dengan real-time simulator

### 1.5.3 Batasan Penelitian

1. **Ukuran Dataset Kecil**
   - n=15 lokasi × 4 kategori = 60 data points
   - Implikasi: Generalisasi ke kota lain uncertain, require retraining dengan local data

2. **Temporal Coverage**
   - 1 tahun data (2023)
   - Trend tahunan atau multi-year cycles tidak terdeteksi
   - COVID atau event khusus impact pada demand tidak fully captured

3. **Feature Limitation**
   - Hanya volume kendaraan dan temporal pattern
   - External factors (parking supply availability, competitor facilities, economic indicators) tidak included
   - Real-time occupancy data tidak tersedia

4. **Jenis Kendaraan**
   - Focus pada 2 jenis (motor & mobil)
   - Kendaraan komersial (truk, bis) tidak included

5. **Scope Pricing**
   - Focus pada base tariff dan time-based surcharge
   - Demand-responsive dynamic pricing (real-time adjustment) bukan scope
   - Behavior elasticity estimation tidak included

6. **Technical Platform**
   - Dashboard implementasi Streamlit (local atau cloud simple deployment)
   - Tidak mencakup integration dengan real-time occupancy sensors atau POS system

### 1.5.4 Asumsi Penelitian

1. **Data Quality**
   - Data dari BAPPEDALITBANG valid dan representatif
   - Tidak ada systematic bias dalam observasi lapangan
   - Validasi Google Maps cukup untuk spatial accuracy

2. **Model Assumption**
   - Historical pattern (2023) persisten untuk future policy (asumsi stationarity)
   - Random Forest assumption valid (features independent-ish, target clear definition)
   - Quantile binning appropriately defines kelas potensi

3. **Implementability**
   - Decision maker (pemerintah) akan mengadopsi rekomendasi policy berbasis model
   - Parker akan responsive terhadap dynamic pricing mechanism
   - Technical infrastructure (dashboard hosting, data update) feasible

---

## 1.7 Sistematika Penulisan

Laporan penelitian ini disusun dalam struktur berikut:

| Bab | Judul | Deskripsi |
|-----|-------|-----------|
| **Bab 1** | Pendahuluan | Latar belakang, rumusan masalah, tujuan, manfaat, scope |
| **Bab 2** | Tinjauan Pustaka | Literature review tentang parking management, TDM, ML algorithms, spatial analysis |
| **Bab 3** | Metode Penelitian | Detailed methodology dengan 6 tahapan (data collection → implementation) |
| **Bab 4** | Hasil dan Pembahasan | Detailed results per tahapan dan discussion menjawab 3 RM |
| **Bab 5** | Kesimpulan dan Rekomendasi | Summary findings dan implementasi roadmap |

---

## 1.8 Kontribusi Penelitian

### Novelty dalam Konteks Lokal
1. **Pertama kalinya** di Kabupaten Banyumas mengintegrasikan ML + spatial analysis untuk parking policy
2. **Implementasi practical** dari academic theory ke decision support system
3. **Dataset dan model public** untuk research community

### Metodologi Inovatif
1. Hybrid approach: Statistical quantile + predictive ML model
2. Small dataset (n=15) handling dengan cross-validation dan ensemble methods
3. Transparent, interpretable ML (feature importance) untuk policy makers

### Policy Impact Potential
1. Revenue optimization tanpa sacrificing accessibility
2. Demand management yang lebih sophisticated dari flat-rate approach
3. Geographic differentiation yang justified oleh data-driven analysis

---

*Bab 1 menetapkan konteks dan foundation untuk penelitian komprehensif tentang sistem penetapan tarif parkir adaptif-progresif di Kabupaten Banyumas.*
