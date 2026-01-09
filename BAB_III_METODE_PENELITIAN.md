# BAB III
# METODE PENELITIAN

## 3.1 Alur Penelitian

Penelitian ini menerapkan metodologi kuantitatif yang mengintegrasikan pendekatan Data Mining dan Spatial Analysis. Alur keseluruhan penelitian ini mengikuti urutan sistematis dari lima tahapan utama: (1) Pengumpulan Data, (2) Pra-pemrosesan Data, (3) Pengembangan dan Evaluasi Model, (4) Implementasi Tarif Progresif Adaptif Dinamis, dan (5) Visualisasi Dashboard Spatial Analysis Streamlit.

Pipeline analitik ini merepresentasikan urutan lengkap dari akuisisi data mentah hingga pembangkitan model penetapan harga yang beradaptasi secara spasial dan dinamis. Setiap tahapan memastikan bahwa metodologi adalah transparan, dapat direproduksi, dan terukur secara ilmiah.

Tahapan pertama, pengumpulan data, melibatkan perolehan data operasional dan spasial terkait aktivitas parkir dari arsip pemerintah daerah dan observasi lapangan. Tahapan kedua, pra-pemrosesan data, berfokus pada pembersihan, transformasi, dan rekayasa data untuk menghasilkan input yang terstruktur dengan baik untuk pelatihan model. Tahapan ketiga, pengembangan dan evaluasi model, menerapkan algoritma Klasifikasi Random Forest untuk mengidentifikasi potensi pendapatan setiap lokasi parkir berdasarkan volume kendaraan, distribusi waktu, dan faktor spasial. Tahapan keempat, implementasi tarif progresif, mengintegrasikan hasil klasifikasi ke dalam kerangka Tarif Progresif Adaptif Dinamis. Tahapan kelima, visualisasi dashboard, mengimplementasikan sistem melalui dashboard Streamlit interaktif yang menggabungkan visualisasi spasial, interpretasi model, dan simulasi tarif.

Penjelasan detail tentang setiap tahapan disajikan dalam sub-bagian berikut ini.

## 3.2 Pengumpulan Data

### 3.2.1 Dataset

Dataset yang digunakan dalam penelitian ini adalah data sekunder yang diperoleh dari arsip Badan Perencanaan Pembangunan, Penelitian, dan Pengembangan Daerah (BAPPEDALITBANG) Kabupaten Banyumas. Data yang tercatat pada tahun 2023 dikumpulkan sebagai bagian dari program pengelolaan retribusi parkir regional dan evaluasi fiskal.

Dataset mencakup 408 lokasi parkir resmi dengan 41 atribut, termasuk pendapatan parkir, volume kendaraan, durasi (puncak, sedang, dan sepi), dan indikator operasional untuk sepeda motor dan mobil. Selain itu, koordinat lintang dan bujur dicatat secara manual melalui observasi lapangan dan diverifikasi menggunakan alat pemetaan digital (Google Maps) untuk memastikan akurasi spasial. Hal ini meningkatkan keandalan data untuk visualisasi spasial dan analisis zona potensi tarif.

### 3.2.2 Variabel Penelitian

Untuk membangun model klasifikasi, beberapa variabel diidentifikasi dan dikategorikan berdasarkan fungsi analitikalnya dalam penelitian. Variabel-variabel ini merepresentasikan aspek spasial dan operasional dari aktivitas parkir serta berfungsi sebagai input utama untuk proses klasifikasi Random Forest.

Variabel penelitian dikategorikan menjadi dua jenis seperti yang dirangkum dalam Tabel 1.

**Tabel 1 Variabel Penelitian**

| Jenis Variabel | Variabel | Deskripsi |
|---|---|---|
| **Variabel Independen (Fitur)** | Data Spasial | Lintang, Bujur, dan Nama Titik Lokasi |
| | Data Kuantitas | Jumlah kendaraan (mobil & sepeda motor) pada hari kerja dan akhir pekan |
| | Data Waktu | Jam Puncak, Sedang, dan Sepi (dikonversi ke format rata-rata jam desimal) |
| | Data Pendapatan | Pendapatan tarif parkir tahunan menurut jenis kendaraan dan kategori hari |
| **Variabel Dependen (Target)** | Kelas Potensi Tarif | Diklasifikasikan sebagai Rendah, Sedang, atau Tinggi berdasarkan kuantil pendapatan tahunan |

## 3.3 Diagram Alir Penelitian

Diagram alir penelitian menggambarkan alur kegiatan penelitian yang dilakukan secara sistematis mulai dari identifikasi masalah, studi literatur, hingga hasil. Diagram alir penelitian dituliskan dalam bentuk diagram flowchart dan setiap proses atau tahapan pada diagram penelitian wajib dijelaskan. Pada sub-bab ini akan menjadi acuan pada Bab 4.1.

## 3.4 Pra-pemrosesan Data

Tahapan ini bertujuan untuk mempersiapkan data mentah menjadi format data yang bersih dan terstruktur siap untuk diproses oleh model Machine Learning.

### 3.3.1 Pembersihan Data

**Data Encoding:** Nilai pendapatan yang awalnya disimpan dalam format teks IDR (misalnya, "IDR 150.000") dikonversi ke bentuk desimal numerik (misalnya, 150000.0) untuk kompatibilitas komputasional.

**Konversi Data Waktu:** Atribut rentang waktu (misalnya, "15.00–17.00") ditransformasi menjadi nilai rata-rata jam desimal tunggal (misalnya, 16.0) menggunakan fungsi kustom `konversi_jam()`. Nilai-nilai ini kemudian digunakan sebagai input kuantitatif dalam model.

### 3.3.2 Imputasi Nilai yang Hilang

Nilai yang hilang (NaN) yang teridentifikasi dalam bidang numerik seperti kuantitas kendaraan, pendapatan, dan waktu (jam desimal) diimputasi menggunakan substitusi median atau mean sesuai dengan distribusi data. Ini memastikan bahwa tidak ada catatan kritis yang dihilangkan selama pelatihan model, sehingga menjaga integritas statistik dataset.

### 3.3.3 Rekayasa Fitur

**Total Pendapatan:** Kolom baru, `Total_Pend_Motor` dan `Total_Pend_Mobil`, dihitung dengan mengagregasi data pendapatan tahunan.

**Pembentukan Kelas Potensi (Variabel Target):** Menggunakan teknik Quantile Binning (`pd.qcut`), total pendapatan tahunan dikelompokkan menjadi tiga kelas yang merepresentasikan potensi pendapatan titik parkir, yaitu:
- **Kelas Rendah:** Kuantil pertama (pendapatan terendah)
- **Kelas Sedang:** Antara kuantil pertama dan ketiga
- **Kelas Tinggi:** Kuantil ketiga dan di atasnya (pendapatan tertinggi)

**Pembagian Dataset:** Dataset dibagi menjadi training set (80%) dan test set (20%) menggunakan stratified sampling untuk memastikan keseimbangan distribusi kelas target.

## 3.5 Metode Pemodelan Klasifikasi

### 3.5.1 Model Matematika Random Forest

Classifier Random Forest (RFC) membangun beberapa pohon keputusan dan mengagregasi hasilnya melalui mekanisme voting mayoritas. Pemisahan optimal di setiap node ditentukan menggunakan Gini Impurity, dihitung seperti yang ditunjukkan pada Persamaan (1) dan Persamaan (2).

$$\text{Gini}(S_i) = 1 - \sum_{j=1}^{c} p_j^2 \quad \quad \quad (1)$$

$$\text{Gini}_{\text{split}} = \sum_{i=1}^{k} \frac{n_i}{n} \times \text{Gini}(S_i) \quad \quad \quad (2)$$

di mana $p_j$ menunjukkan probabilitas kelas $j$ dalam node $S_i$, $n_i$ adalah jumlah sampel dalam subset $S_i$, dan $n$ merepresentasikan total sampel dalam node induk. Nilai Gini yang lebih rendah mengindikasikan node yang lebih murni dan pemisahan fitur yang lebih baik (Suci Amaliah et al., 2022).

### 3.5.2 Konfigurasi Pemodelan

Model Random Forest dikalibrasi menggunakan hyperparameter yang dirangkum dalam Tabel 2.

**Tabel 2 Pengaturan Hyperparameter Random Forest**

| Hyperparameter | Nilai | Deskripsi |
|---|---|---|
| n_estimators | 200 | Jumlah pohon dalam forest, memastikan hasil voting yang stabil dan generalisasi model. |
| max_depth | None | Memungkinkan pohon berkembang sepenuhnya, menangkap hubungan kompleks dalam data. |
| min_samples_split | 2 | Jumlah minimum sampel yang diperlukan untuk membagi node internal, memungkinkan pembelajaran detail. |
| min_samples_leaf | 1 | Jumlah minimum sampel yang diperlukan di setiap leaf node. |
| bootstrap | True | Mengaktifkan sampling dengan penggantian, meningkatkan keandalan model. |
| random_state | 42 | Memastikan reprodusibilitas di seluruh percobaan. |
| criterion | "gini" | Gini impurity digunakan sebagai fungsi untuk mengukur kualitas pemisahan. |

### 3.5.3 Evaluasi Model

Proses pemodelan dalam penelitian ini dilakukan melalui beberapa tahapan sistematis untuk memastikan keandalan dan robustness hasil klasifikasi. Dataset pertama kali dibagi menjadi subset pelatihan dan pengujian menggunakan rasio 80:20, di mana training set digunakan untuk membangun model dan test set digunakan untuk mengevaluasi performa generalisasinya pada data yang belum pernah dilihat.

Selanjutnya, Classifier Random Forest dilatih secara terpisah untuk setiap kategori kendaraan (sepeda motor dan mobil) menggunakan fitur prediktif seperti kuantitas kendaraan dan durasi parkir rata-rata. Fitur-fitur ini digunakan untuk memprediksi variabel target yang sesuai, `Class_Motor` dan `Class_Mobil`, yang merepresentasikan kelas potensi tarif parkir: Rendah, Sedang, dan Tinggi.

Setelah pelatihan, performa model dievaluasi menggunakan metrik klasifikasi standar yang berasal dari confusion matrix: True Positive (TP), True Negative (TN), False Positive (FP), dan False Negative (FN).

Metrik evaluasi didefinisikan sebagai berikut:

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \quad \quad \quad (3)$$

$$\text{Precision} = \frac{TP}{TP + FP} \quad \quad \quad (4)$$

$$\text{Recall} = \frac{TP}{TP + FN} \quad \quad \quad (5)$$

$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \quad \quad \quad (6)$$

Seperti ditunjukkan pada Persamaan (3), Accuracy mengukur proporsi keseluruhan instansi yang diklasifikasikan dengan benar, sedangkan Precision dan Recall, yang didefinisikan dalam Persamaan (4) dan (5), menilai ketepatan dan kelengkapan model dalam mengidentifikasi kelas yang benar. F1-Score, yang dinyatakan dalam Persamaan (6), merepresentasikan rata-rata harmonis dari Precision dan Recall, berfungsi sebagai indikator performa yang seimbang terutama berharga dalam dataset dengan ketidakseimbangan kelas.

Untuk memastikan konsistensi model dan generalisasi, prosedur cross-validation 5-fold diterapkan. Dataset dibagi menjadi lima subset yang sama, di mana model dilatih secara iteratif pada empat subset dan divalidasi pada subset yang tersisa. Akurasi cross-validation dihitung seperti yang dinyatakan dalam Persamaan (7).

$$CV = \frac{1}{k} \sum_{i=1}^{k} \text{Accuracy}_i \quad \quad \quad (7)$$

Proses rata-rata ini mengurangi varians dan meningkatkan robustness serta stabilitas classifier Random Forest.

## 3.6 Implementasi Tarif Progresif Adaptif Dinamis

Hasil klasifikasi (potensi_class) digunakan sebagai input untuk fungsi penetapan harga, yang membuat sistem penetapan harga bersifat dinamis dan progresif.

### 3.6.1 Logika Tarif Dasar Adaptif

- Setiap kelas potensi (Rendah, Sedang, Tinggi) diberikan Tarif Dasar Statis yang berbeda (misalnya, Tinggi: IDR 3.000, Sedang: IDR 2.000, Rendah: IDR 1.000 untuk motor; Tinggi: IDR 5.000, Sedang: IDR 4.000, Rendah: IDR 3.000 untuk mobil).
- Model memprediksi kelas potensi dari titik parkir, dan Tarif Dasar yang sesuai diambil secara adaptif dari pemetaan harga.

### 3.6.2 Logika Surcharge Progresif Berbasis Waktu

Setelah tarif dasar ditetapkan, logika progresif diterapkan melalui surcharge berbasis waktu untuk mengelola permintaan transportasi (TDM) selama jam-jam puncak. Logika ini diimplementasikan menggunakan pernyataan kondisional seperti yang dinyatakan dalam Persamaan (8).

$$\text{Tarif Akhir} = \text{Tarif Dasar Adaptif} + \text{Surcharge Progresif} \quad \quad \quad (8)$$

**Kondisi Surcharge:** Jika waktu parkir aktual (jam_desimal) melebihi batas waktu yang telah ditentukan sebelumnya (misalnya, setelah pukul 09:00), biaya tambahan diterapkan.

**Jumlah Surcharge:** Jumlah surcharge ini juga beradaptasi berdasarkan kelas potensi lokasi (potensi_class), memastikan peningkatan harga yang lebih agresif di lokasi dengan potensi tinggi selama jam puncak. Jumlah surcharge diberikan dalam Tabel 3 berikut.

**Tabel 3 Jumlah Surcharge Progresif**

| Kelas Potensi | Kondisi Waktu (jam_desimal > 9.0) | Surcharge Progresif |
|---|---|---|
| Tinggi | Ya | IDR 1.000 |
| Sedang | Ya | IDR 500 |
| Rendah | Ya | IDR 0 |

Logika ini membentuk fondasi dari sistem Tarif Progresif Dinamis yang direkomendasikan.

## 3.7 Analisis Spasial dan Visualisasi

Teknik analisis spasial dimanfaatkan untuk memvisualisasikan data dan hasil model.

**Distribution Mapping:** Menggunakan koordinat lintang–bujur untuk memplot titik-titik parkir di peta interaktif Folium dengan popup informatif yang menampilkan nama lokasi dan kategori potensi tarif.

**Visualisasi Tematik:** Menghasilkan peta yang menampilkan cluster spasial potensi tarif (Rendah–Sedang–Tinggi), heatmap untuk menunjukkan konsentrasi geografis potensi pendapatan, dan grafik distribusi untuk analisis pola spasial.

**Integrasi Dashboard:** Workflow lengkap diimplementasikan dalam dashboard berbasis Streamlit dengan empat modul utama:
1. **Modul Data Table:** Menampilkan data mentah dan data pre-processed dengan statistik deskriptif
2. **Modul Visualisasi:** Menampilkan distribusi pendapatan, batas kuantil, kepadatan parkir, dan grafik 24 jam
3. **Modul Pemodelan:** Menampilkan hasil training model, confusion matrix, feature importance, dan tabel rekomendasi tarif
4. **Modul Peta & Simulasi:** Menampilkan peta interaktif dengan search function, simulasi what-if untuk prediksi tarif progresif real-time

Dashboard ini memungkinkan eksplorasi interaktif terhadap hasil analisis, simulasi penetapan harga dinamis, dan dukungan pengambilan keputusan bagi pihak Dinas Perhubungan Kabupaten Banyumas.
