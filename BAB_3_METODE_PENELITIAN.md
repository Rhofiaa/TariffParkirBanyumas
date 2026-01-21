# BAB III
# METODE PENELITIAN

Pada pembahasan metode penelitian akan dipaparkan secara berurutan mengenai subjek dan objek penelitian, alat dan bahan penelitian, desain penelitian, teknik pengumpulan data, teknik pengolahan dan analisis data, serta diagram alir penelitian yang menggambarkan alur sistematis penelitian ini.

## 3.1. Subjek dan Objek Penelitian

### 3.1.1. Subjek Penelitian

Subjek penelitian ini adalah dataset titik parkir resmi di wilayah Kabupaten Banyumas, khususnya di Purwokerto dan sekitarnya, yang berjumlah 408 titik parkir berdasarkan Laporan Akhir Kajian Potensi Parkir Kabupaten Banyumas tahun 2023. Dataset ini mencakup data spasial (koordinat geografis latitude-longitude), data temporal (pola waktu penggunaan), data operasional kendaraan (volume kendaraan tipe motor dan mobil), serta estimasi pendapatan parkir harian, mingguan, bulanan, dan tahunan. Selain itu, subjek penelitian juga mencakup algoritma Random Forest sebagai metode machine learning untuk klasifikasi potensi pendapatan parkir, serta teknik analisis spasial untuk visualisasi dan interpretasi distribusi geografis potensi pendapatan.

### 3.1.2. Objek Penelitian

Objek penelitian ini adalah:

1. Potensi pendapatan parkir di setiap titik lokasi parkir yang diklasifikasikan ke dalam tiga kategori: rendah, sedang, dan tinggi, berdasarkan atribut kendaraan, volume penggunaan, dan pola temporal aktivitas.
2. Akurasi model klasifikasi Random Forest dalam memprediksi dan mengelompokkan titik parkir ke dalam kategori potensi pendapatan yang tepat dibandingkan dengan data aktual di lapangan.
3. Distribusi geografis potensi pendapatan parkir di wilayah Kabupaten Banyumas yang divisualisasikan melalui peta interaktif berbasis koordinat geografis.
4. Kebijakan tarif progresif yang dapat ditetapkan berdasarkan hasil klasifikasi potensi pendapatan untuk optimalisasi revenue dan efisiensi penggunaan lahan parkir.

## 3.2. Alat dan Bahan Penelitian

### 3.2.1. Alat Penelitian

#### 3.2.1.1. Perangkat Keras (Hardware)

- **Laptop/PC**: Komputer dengan spesifikasi minimal Intel Core i5/AMD Ryzen 5, RAM 8GB, dan penyimpanan SSD 256GB untuk proses komputasi machine learning dan pemrosesan dataset besar.
- **Perangkat GPS/Smartphone**: Untuk verifikasi koordinat geografis titik parkir selama survei lapangan.
- **Perangkat penyimpanan**: Cloud storage atau external hard drive untuk backup data dan dokumentasi penelitian.

#### 3.2.1.2. Perangkat Lunak (Software)

1. **Sistem Operasi**: Windows 10/11 atau Ubuntu Linux untuk environment penelitian yang stabil.
2. **Bahasa Pemrograman**: Python 3.8+ sebagai bahasa utama untuk pengembangan model machine learning dan analisis data.
3. **IDE dan Development Tools**:
   - Jupyter Notebook untuk eksperimen interaktif dan dokumentasi analisis
   - Visual Studio Code untuk development aplikasi dan script
   - PyCharm Community Edition untuk development yang lebih advanced
4. **Database dan Data Storage**:
   - PostgreSQL/SQLite untuk penyimpanan data struktur parkir dan pendapatan
   - CSV/Excel untuk format intermediate data preprocessing
5. **Library dan Framework Python**:
   - **Data Processing**: Pandas (v1.3+), NumPy (v1.20+)
   - **Machine learning**: Scikit-Learn (v0.24+) untuk Random Forest dan model klasifikasi
   - **Geospatial Analysis**: Geopandas, Shapely untuk analisis spasial dan coordinate handling
   - **Visualization**: Matplotlib, Seaborn untuk visualisasi statistik; Folium untuk peta geografis interaktif
   - **Web Framework**: Streamlit (v0.80+) untuk dashboard dan aplikasi web interaktif
   - **Statistical Analysis**: SciPy, Statsmodels untuk evaluasi statistik model
6. **Tools Pendukung**:
   - Git untuk version control dan collaboration
   - Google Maps untuk verifikasi koordinat dan geocoding
   - Google Colab untuk cloud-based computing jika diperlukan

#### 3.2.1.3. Teori dan Metode Analisis

- Teori machine learning: ensemble learning, decision tree, ensemble methods
- Teori analisis spasial: spatial data analysis, geographic information systems (GIS) concepts
- Teori ekonomi transportasi: demand analysis, pricing elasticity, tarif progresif
- Statistik inferensi: confusion matrix, precision-recall, ROC-AUC, cross-validation

#### 3.2.1.4. Persamaan dan Model Matematis

- Formula Gini Impurity untuk feature importance pada Random Forest
- Metrik evaluasi model: accuracy, precision, recall, F1-score, ROC-AUC
- Perhitungan potensi pendapatan berdasarkan volume dan tarif
- Normalisasi dan scaling data untuk preprocessing

### 3.2.2. Bahan Penelitian

#### 3.2.2.1. Data Primer

Data primer diperoleh melalui observasi lapangan langsung. Proses pengumpulan data primer mencakup **Survey Lapangan Koordinat Geografis**: Penandaan lokasi setiap titik parkir menggunakan GPS device dan Google Maps untuk memperoleh koordinat latitude-longitude dengan akurasi tinggi.

#### 3.2.2.2. Data Sekunder

Data sekunder diperoleh dari sumber-sumber resmi dan publikasi terkait:

1. **Laporan Pemerintah**: 
   - Laporan Akhir Kajian Potensi Parkir Kabupaten Banyumas tahun 2023 (Bappedalitbang, 2023)
   - Data PAD (Pendapatan Asli Daerah) Kabupaten Banyumas dari tahun 2020-2023
   - Laporan Dinas Perhubungan mengenai sistem retribusi parkir dan administrasi
2. **Literatur dan Penelitian Terdahulu**:
   - Penelitian tentang prediksi okupansi parkir dan klasifikasi potensi pendapatan
   - Studi tentang implementasi tarif progresif di kota-kota besar Indonesia
   - Kajian teori machine learning dan analisis spasial untuk transportasi perkotaan
3. **Data Statistik Umum**:
   - Data kependudukan dan urbanisasi dari BPS (Badan Pusat Statistik)
   - Data pertumbuhan kendaraan bermotor di Indonesia
   - Informasi geografi dan peta dasar wilayah Kabupaten Banyumas

## 3.3. Diagram Alir Penelitian

Penelitian ini menggunakan pendekatan kuantitatif yang mengintegrasikan metode Data Mining, Machine learning, dan Analisis Spasial untuk membangun sistem penetapan tarif parkir adaptif dan progresif dinamis di Kabupaten Banyumas. Diagram alir penelitian digunakan untuk menggambarkan tahapan penelitian secara sistematis sebagai acuan dalam pelaksanaan dan pembahasan penelitian. Secara konseptual, penelitian ini diawali dengan identifikasi masalah dan studi literatur yang bertujuan untuk merumuskan permasalahan, menentukan variabel penelitian, serta memilih metode yang sesuai. Tahapan teknis penelitian selanjutnya divisualisasikan dalam diagram alir pada Gambar 3.1, terdiri atas enam tahapan utama, yaitu: (1) Pengumpulan Data, (2) Preprocessing Data, (3) Perancangan Model dan Evaluasi Model Random Forest, (4) Penerapan Tarif Adaptif dan Progresif Dinamis, (5) Visualisasi Dashboard Streamlit, yang menggambarkan proses pengolahan data hingga visualisasi hasil penelitian. Diagram ini menjadi acuan utama dalam pembahasan hasil penelitian pada Bab IV.

Alur ini menggambarkan keseluruhan proses penelitian, mulai dari identifikasi masalah dan dasar teori hingga pengembangan model serta implementasi sistem dalam bentuk dashboard interaktif. Setiap tahap dijelaskan secara sistematis agar hasil penelitian bersifat transparan, replikasi, dan terukur secara ilmiah.

### 3.3.1. Identifikasi Masalah dan Studi Literatur

Tahap awal penelitian dilakukan dengan mengidentifikasi permasalahan tarif parkir di Kabupaten Banyumas yang masih bersifat statis dan belum mempertimbangkan variasi spasial maupun temporal permintaan parkir.

Selanjutnya dilakukan kajian literatur untuk memperkuat landasan teori, meliputi:

- Konsep tarif progresif dinamis dalam manajemen transportasi perkotaan
- Penggunaan algoritma Machine learning (Random Forest, Decision tree) dalam analisis potensi pendapatan
- Analisis spasial untuk pemetaan zona parkir potensial, serta
- Studi kebijakan Transport Demand Management (TDM) yang relevan dengan pengendalian tarif berbasis waktu dan kepadatan kendaraan

Tahapan ini menjadi dasar konseptual dalam merancang model penetapan tarif yang adaptif terhadap karakteristik lokasi parkir.

### 3.3.2. Pengumpulan Data

#### 3.3.2.1. Sumber Data

Data yang digunakan merupakan data sekunder hasil rekapitulasi dari Badan Perencanaan Pembangunan, Penelitian, dan Pengembangan Daerah (BAPPEDALITBANG) Kabupaten Banyumas serta data primer hasil observasi lapangan yaitu data Koordinat Geografis.

#### 3.3.2.2. Variabel Penelitian

Dalam membangun model klasifikasi, beberapa variabel diidentifikasi dan dikategorikan berdasarkan fungsi analisisnya. Variabel-variabel tersebut merepresentasikan aspek spasial dan operasional dari aktivitas parkir, dan menjadi masukan utama dalam proses klasifikasi menggunakan algoritma Random Forest.

**Tabel 3.1 Variabel Penelitian**

| Jenis Variabel | Nama Variabel | Keterangan |
|---|---|---|
| Variabel Independen (Fitur) | Data Spasial | Latitude, Longitude, dan Nama Titik Parkir |
| | Data Kuantitas | Jumlah kendaraan (motor & mobil) weekday/weekend |
| | Data Waktu | Jam sepi, sedang, dan ramai (format desimal) |
| | Data Pendapatan | Pendapatan tahunan parkir per jenis kendaraan |
| Variabel Dependen (Target) | Kelas Potensi Tarif | Klasifikasi: Rendah, Sedang, Tinggi berdasarkan kuantil pendapatan |

### 3.3.3. Preprocessing Data

Tahap ini bertujuan untuk mengubah data mentah menjadi data yang bersih, konsisten, dan siap digunakan untuk pelatihan model Machine learning.

#### 3.3.3.1. Pembersihan Data (Data Cleaning)

1. **Pengkodean Data**: Nilai pendapatan yang awalnya tersimpan dalam format teks IDR (misal, "IDR 150,000") dikonversi menjadi angka desimal (misal, 150000.0) agar kompatibel secara komputasi.
2. **Konversi Data Waktu**: Atribut rentang waktu (misal, "15.00–17.00") diubah menjadi nilai jam desimal rata-rata tunggal (misal, 16.0) menggunakan fungsi `convert_time_range()`. Nilai ini kemudian digunakan sebagai input kuantitatif pada model.
3. **Imputasi Nilai Hilang**: Nilai yang hilang (NaN) pada kolom numerik seperti jumlah kendaraan, pendapatan, dan jam (desimal) diimputasi menggunakan median atau rata-rata tergantung distribusi data, untuk menjaga integritas statistik dataset.

**Tahap Train-Test Split (Setelah Pembersihan, Sebelum Feature Engineering)**
- Setelah data dibersihkan (langkah 1–3 di atas), dilakukan pemisahan data menjadi **train 80%** dan **test 20%** dengan **stratifikasi** berbasis label sementara (kuantil pendapatan) agar distribusi kelas seimbang.
- Feature engineering (Total Pendapatan, Labeling kuantil) dan imputasi lanjutan hanya dihitung dari **data train**, lalu diaplikasikan ke data test untuk mencegah data leakage.

#### 3.3.3.2. Rekayasa Fitur (Feature Engineering)

1. **Pendapatan Total**: Kolom baru, `Total_Revenue_Motorcycle` dan `Total_Revenue_Car`, dihitung dengan mengakumulasi data pendapatan tahunan.
2. **Pembentukan Kelas Potensi (Variabel Target)**: Dengan menggunakan teknik Quantile Binning (`pd.qcut`), total pendapatan tahunan dikelompokkan menjadi tiga kelas potensi pendapatan parkir:
   - **Kelas Rendah**: Kuantil pertama (pendapatan terendah)
   - **Kelas Sedang**: Antara kuantil pertama dan ketiga
   - **Kelas Tinggi**: Kuantil ketiga dan di atasnya (pendapatan tertinggi)

#### 3.3.3.3. Kategorisasi Fitur Temporal

Setelah nilai waktu dikonversi menjadi jam desimal pada tahap pembersihan data (3.3.3.1), tahap selanjutnya adalah **kategorisasi temporal** untuk menangkap pola demand parkir berdasarkan waktu operasional. Nilai jam desimal dikategorisasi menjadi 3 kategori berdasarkan pola demand parkir yang karakteristik di lokasi penelitian:

| Kategori | Rentang Waktu | Jam Desimal | Karakteristik Demand |
|----------|---|---|---|
| Jam Sepi | 00:00–06:00, 22:00–24:00 | jam ≤ 6 atau jam ≥ 22 | Demand rendah, kendaraan minimal, periode istirahat malam |
| Jam Ramai | 08:00–19:00 | 8 < jam ≤ 19 | Demand puncak, volume kendaraan tinggi, periode aktivitas maksimal |
| Jam Sedang | 06:00–08:00, 19:00–22:00 | 6 < jam ≤ 8 atau 19 < jam < 22 | Demand transisi, volume sedang, periode jam sibuk pagi dan sore |

**Hasil Feature Engineering Temporal**

Dari kategorisasi temporal ini, untuk setiap titik parkir dihasilkan **12 fitur temporal numerik** yang merepresentasikan jumlah kendaraan pada setiap kategori waktu:

**Untuk Kendaraan Motor:**
- Jam Sepi Motor Weekday (nilai numerik: jumlah motor pada jam sepi di hari kerja)
- Jam Sepi Motor Weekend
- Jam Ramai Motor Weekday
- Jam Ramai Motor Weekend
- Jam Sedang Motor Weekday
- Jam Sedang Motor Weekend

**Untuk Kendaraan Mobil:**
- Jam Sepi Mobil Weekday
- Jam Sepi Mobil Weekend
- Jam Ramai Mobil Weekday
- Jam Ramai Mobil Weekend
- Jam Sedang Mobil Weekday
- Jam Sedang Mobil Weekend

Setiap fitur temporal **bukan hanya label kategori**, melainkan **nilai numerik yang merepresentasikan jumlah kendaraan** pada kategori waktu tersebut. Contoh:
- "Jam Ramai Motor Weekday = 450" berarti ada 450 kendaraan motor yang parkir pada jam-jam ramai (08:00–19:00) di hari kerja dalam periode pengamatan
- "Jam Sepi Motor Weekday = 120" berarti ada 120 kendaraan motor yang parkir pada jam sepi (00:00–06:00 dan 22:00–24:00) di hari kerja

Fitur-fitur temporal ini kemudian menjadi input penting bagi model Random Forest untuk memahami bagaimana pola waktu penggunaan parkir mempengaruhi potensi pendapatan lokasi.

### 3.3.4. Perancangan Model Random Forest

#### 3.3.4.1. Model Matematika Random Forest

Random Forest Classifier (RFC) membangun banyak pohon keputusan dan menggabungkan hasilnya melalui mekanisme voting mayoritas. Pemisahan optimal pada setiap node ditentukan menggunakan Gini Impurity, yang dihitung melalui persamaan berikut. Nilai Gini yang lebih rendah menunjukkan node lebih murni dan pemisahan fitur lebih baik.

#### 3.3.4.2. Konfigurasi Pemodelan

Model Random Forest dituning menggunakan hyperparameter seperti pada Tabel 3.2.

**Tabel 3.2 Hyperparameter Random Forest**

| Hyperparameter | Nilai | Deskripsi |
|---|---|---|
| n_estimators | 150 | Jumlah pohon dalam hutan, untuk hasil voting stabil dan generalisasi model |
| max_depth | 15 | Membiarkan pohon berkembang penuh untuk menangkap hubungan kompleks |
| min_samples_split | 2 | Minimum sampel untuk membagi node internal |
| min_samples_leaf | 3 | Minimum sampel pada setiap leaf node |
| bootstrap | TRUE | Mengaktifkan sampling dengan pengembalian, meningkatkan robustitas model |
| random_state | 42 | Menjamin reproduktibilitas |
| criterion | "gini" | Fungsi Gini untuk mengukur kualitas split |

#### 3.3.4.3. Evaluasi Model

Proses pemodelan dilakukan melalui beberapa tahap sistematis untuk menjamin keandalan hasil klasifikasi. Dataset dibagi menjadi subset training dan testing dengan rasio 80:20. Subset training digunakan untuk membangun model, sementara subset testing digunakan untuk mengevaluasi performa model pada data yang belum pernah dilihat.

Random Forest Classifier dilatih secara terpisah untuk setiap kategori kendaraan (motor dan mobil) menggunakan fitur prediktif seperti jumlah kendaraan dan durasi parkir rata-rata. Model ini memprediksi variabel target Class_Motorcycle dan Class_Car, yang merepresentasikan kelas potensi tarif parkir: Rendah, Sedang, dan Tinggi. Kinerja model dievaluasi menggunakan metrik klasifikasi standar dari confusion matrix: True Positive (TP), True Negative (TN), False Positive (FP), dan False Negative (FN).

### 3.3.5. Penetapan Tarif Adaptif dan Tarif Dinamis Progresif

Hasil klasifikasi (potensi_class) digunakan sebagai input untuk fungsi penetapan tarif, sehingga harga bersifat dinamis dan progresif.

#### 3.3.5.1. Logika Harga Dasar Adaptif

Setiap kelas potensi (Rendah, Sedang, Tinggi) diberikan Harga Dasar (Static Base Price) berbeda:

**Tabel 3.3 Logika Dasar Tarif Adaptif**

| Jenis Kendaraan | Kelas Potensi | Tarif Dasar |
|---|---|---|
| Motor | Tinggi | Rp 3.000 |
| Motor | Sedang | Rp 2.000 |
| Motor | Rendah | Rp 1.000 |
| Mobil | Tinggi | Rp 5.000 |
| Mobil | Sedang | Rp 4.000 |
| Mobil | Rendah | Rp 3.000 |

Model memprediksi kelas potensi titik parkir, dan Harga Dasar yang sesuai diambil secara adaptif dari peta tarif.

#### 3.3.5.2. Logika Tambahan Tarif Progresif Waktu

Tahap ini merupakan implementasi dari model Dynamic Progressive Pricing. Setelah harga dasar ditetapkan, logika tarif progresif diterapkan melalui surcharge berbasis waktu untuk mengatur permintaan parkir pada jam sibuk.

- **Kondisi Surcharge**: Jika waktu parkir aktual (jam desimal) memasuki periode tertentu (misal, setelah pukul 09.00), dikenakan biaya tambahan.
- **Jumlah Surcharge**: Besarnya biaya tambahan disesuaikan berdasarkan kelas potensi lokasi (potensi_class), sehingga kenaikan harga lebih agresif di lokasi berpotensi tinggi pada jam sibuk.

**Tabel 3.4 Sistem Progresif Dinamis**

| Kelas Potensi | Kondisi Waktu (jam_desimal > 9.0) | Surcharge Progresif |
|---|---|---|
| Tinggi | Ya | Rp 1.000 |
| Sedang | Ya | Rp 500 |
| Rendah | Ya | Rp 0 |

Logika ini menjadi dasar sistem Dynamic Progressive Pricing yang direkomendasikan.

### 3.3.6. Analisis dan Visualisasi Spasial

Teknik analisis spasial digunakan untuk memvisualisasikan data dan hasil model:

- **Pemetaan Distribusi**: Menggunakan koordinat lintang–bujur untuk memetakan titik parkir pada peta interaktif
- **Visualisasi Tematik**: Membuat peta yang menunjukkan klaster spasial potensi tarif (Rendah–Sedang–Tinggi) dengan menggunakan marker dan warna yang berbeda
- **Integrasi Dashboard**: Alur lengkap diimplementasikan dalam dashboard web berbasis Streamlit, yang menggabungkan tampilan data mentah, metrik evaluasi model, pemetaan spasial, dan simulasi tarif secara real-time
