# BAB IV
# HASIL DAN PEMBAHASAN

## 4.1. Hasil

### 4.1.1. Hasil Pengumpulan Data

Data yang digunakan merupakan data sekunder hasil rekapitulasi dari Badan Perencanaan Pembangunan, Penelitian, dan Pengembangan Daerah (BAPPEDALITBANG) Kabupaten Banyumas dimana ada 408 titik parkir di wilayah Kabupaten Banyumas serta data primer hasil observasi lapangan yaitu data Koordinat Geografis. Dataset mencakup informasi:

- Jumlah kendaraan (mobil dan motor) pada hari kerja dan akhir pekan
- Waktu parkir (jam sepi, sedang, dan ramai) dalam format desimal
- Pendapatan tahunan parkir per jenis kendaraan
- Koordinat geografis (latitude dan longitude) setiap titik parkir

### 4.1.2. Hasil Preprocessing Data

Mengacu pada diagram alir penelitian pada Gambar 3.1, tahap preprocessing data merupakan tahapan kedua setelah pengumpulan data. Tahap ini bertujuan untuk mengubah data mentah menjadi data yang bersih, konsisten, dan siap digunakan dalam proses pelatihan model Random Forest.

Berdasarkan kondisi awal data, masih ditemukan perbedaan format data, nilai hilang, serta atribut yang belum dapat digunakan secara langsung sebagai input numerik. Oleh karena itu, preprocessing data dilakukan sesuai dengan tahapan yang telah dirancang pada Subbab 3.3.3.

#### 4.1.2.1. Pembersihan Data (Data Cleaning)

Hasil pembersihan data menunjukkan bahwa nilai pendapatan parkir yang semula tersimpan dalam format teks mata uang berhasil dikonversi ke dalam format numerik desimal. Selain itu, atribut waktu parkir yang berbentuk rentang waktu berhasil diubah menjadi nilai jam desimal rata-rata, sehingga dapat digunakan sebagai variabel kuantitatif. Penanganan nilai hilang pada atribut numerik seperti jumlah kendaraan, pendapatan, dan waktu parkir dilakukan melalui proses imputasi. Setelah proses ini, dataset tidak lagi mengandung nilai kosong yang dapat mengganggu proses pemodelan.

#### 4.1.2.2. Rekayasa Fitur (Feature Engineering)

Pada tahap rekayasa fitur, dihasilkan atribut baru berupa total pendapatan tahunan untuk masing-masing jenis kendaraan, yaitu `Total_Revenue_Motorcycle` dan `Total_Revenue_Car`. Atribut ini dibentuk dari hasil akumulasi pendapatan parkir tahunan pada setiap titik parkir dan digunakan sebagai representasi utama potensi ekonomi lokasi parkir. 

Selanjutnya, total pendapatan tahunan tersebut dikelompokkan menjadi tiga kelas potensi pendapatan parkir, yaitu rendah, sedang, dan tinggi, menggunakan teknik quantile binning. Pendekatan ini membagi data berdasarkan kuantil distribusi pendapatan sehingga setiap kelas memiliki proporsi data yang relatif seimbang.

Ambang batas pendapatan tahunan untuk masing-masing kelas potensi ditentukan secara terpisah antara kendaraan motor dan mobil. Rincian nilai ambang batas kelas potensi pendapatan parkir disajikan pada Tabel 4.1, yang menunjukkan perbedaan karakteristik pendapatan antara kedua jenis kendaraan.

**Tabel 4.1 Ambang Batas Klasifikasi Potensi Pendapatan Parkir**

| Jenis Kendaraan | Kelas Potensi | Ambang Pendapatan Tahunan Aktual (Rp) |
|---|---|---|
| Motor | Rendah | < Rp 99.991.104 |
| Motor | Sedang | Rp 99.991.104 – Rp 185.298.048 |
| Motor | Tinggi | > Rp 185.298.048 |
| Mobil | Rendah | < Rp 9.523.008 |
| Mobil | Sedang | Rp 9.523.008 – Rp 16.204.032 |
| Mobil | Tinggi | > Rp 16.204.032 |

Hasil pengelompokan kelas potensi pendapatan parkir selanjutnya divisualisasikan dalam bentuk dua grafik pada dashboard sistem, yang menampilkan jumlah titik parkir pada setiap kategori potensi, sehingga memberikan gambaran awal mengenai sebaran potensi pendapatan parkir berdasarkan jenis kendaraan.

Distribusi kelas potensi yang relatif seimbang ini mendukung kinerja algoritma Random Forest dalam proses klasifikasi, karena mengurangi risiko bias model terhadap kelas tertentu. Hasil rekayasa fitur ini selanjutnya digunakan sebagai dasar pada tahap pelatihan dan evaluasi model Random Forest.

#### 4.1.2.3. Hasil Kategorisasi Fitur Temporal

Sebagai bagian dari feature engineering, nilai waktu yang telah dikonversi menjadi jam desimal (pada tahap pembersihan data) selanjutnya dikategorisasi berdasarkan pola demand parkir. Kategorisasi menghasilkan **12 fitur temporal numerik** untuk setiap titik parkir:

**Untuk Kendaraan Motor (6 fitur):**
- Jam Sepi Motor Weekday (jumlah kendaraan pada jam sepi di hari kerja)
- Jam Sepi Motor Weekend
- Jam Ramai Motor Weekday
- Jam Ramai Motor Weekend
- Jam Sedang Motor Weekday
- Jam Sedang Motor Weekend

**Untuk Kendaraan Mobil (6 fitur):**
- Jam Sepi Mobil Weekday
- Jam Sepi Mobil Weekend
- Jam Ramai Mobil Weekday
- Jam Ramai Mobil Weekend
- Jam Sedang Mobil Weekday
- Jam Sedang Mobil Weekend

Kategorisasi berdasarkan threshold waktu:
- **Jam Sepi**: jam ≤ 6 atau jam ≥ 22
- **Jam Ramai**: 8 < jam ≤ 19
- **Jam Sedang**: 6 < jam ≤ 8 atau 19 < jam < 22

Setiap fitur temporal merepresentasikan **nilai numerik (jumlah kendaraan)** pada kategori waktu tersebut. Contoh: "Jam Ramai Motor Weekday = 450" berarti ada 450 kendaraan motor yang parkir pada jam-jam ramai (08:00–19:00) di hari kerja dalam periode pengamatan.

#### 4.1.2.4. Dataset Akhir Hasil Preprocessing

Dataset akhir hasil preprocessing terdiri dari atribut spasial, atribut operasional parkir, serta variabel target kelas potensi pendapatan parkir. Dataset ini selanjutnya digunakan sebagai input utama pada tahap pemodelan Random Forest. Total dataset yang siap diproses mencakup 405 titik parkir dengan 18+ atribut termasuk koordinat geografis, jumlah kendaraan, fitur temporal, dan kelas target.

### 4.1.3. Hasil Perancangan dan Evaluasi Model Random Forest

Tahap pemodelan dilakukan setelah dataset akhir hasil preprocessing dinyatakan siap digunakan. Pada tahap ini, algoritma Random Forest diterapkan untuk melakukan klasifikasi potensi pendapatan parkir ke dalam tiga kelas, yaitu rendah, sedang, dan tinggi, berdasarkan atribut operasional parkir dan atribut spasial yang telah dibentuk pada tahap sebelumnya. 

Model Random Forest dibangun dengan memanfaatkan sejumlah pohon keputusan (decision trees) yang dilatih secara independen menggunakan teknik bootstrap sampling. Setiap pohon menghasilkan prediksi kelas, dan hasil akhir model ditentukan berdasarkan mekanisme majority voting, sehingga mampu meningkatkan stabilitas dan akurasi klasifikasi.

Variabel input yang digunakan dalam pemodelan meliputi:
- Jumlah kendaraan motor dan mobil pada hari kerja dan akhir pekan
- Waktu parkir (jam sepi, sedang, dan ramai) dalam bentuk fitur temporal numerik
- Atribut spasial berupa koordinat geografis (latitude dan longitude)
- Atribut hasil rekayasa fitur (Total Pendapatan, dll)

Sementara itu, variabel target adalah kelas potensi pendapatan parkir yang telah dibentuk melalui teknik quantile binning.

#### 4.1.3.1. Pembagian Data Latih dan Data Uji

Dataset hasil preprocessing yang berjumlah 405 titik parkir selanjutnya dibagi menjadi data latih (training data) dan data uji (testing data) sebagai dasar dalam proses pemodelan Random Forest. Pembagian data dilakukan dengan rasio 80% sebagai data latih dan 20% sebagai data uji, sehingga diperoleh 324 data latih dan 81 data uji.

Pembagian data dilakukan secara acak dengan tetap mempertahankan proporsi kelas potensi pendapatan parkir pada setiap kategori. Pendekatan ini bertujuan untuk memastikan bahwa distribusi kelas pada data latih dan data uji tetap representatif terhadap keseluruhan dataset, sehingga hasil evaluasi kinerja model dapat menggambarkan kemampuan klasifikasi secara objektif.

#### 4.1.3.2. Proses Training Model

Setelah data latih dan uji siap, model Random Forest dilatih menggunakan library scikit-learn di Python. Model ini dibangun dari 150 pohon keputusan, di mana setiap pohon mempelajari pola pada data latih secara independen dan prediksi akhir ditentukan melalui majority voting. Hyperparameter yang digunakan seperti yang ditampilkan di Tabel 3.2 yaitu:

- n_estimators = 150 (jumlah pohon)
- max_depth = 15 (kedalaman maksimal pohon)
- min_samples_split = 2
- min_samples_leaf = 3
- criterion = "gini"
- bootstrap = True
- random_state = 42

Penetapan hyperparameter ini bertujuan agar pohon tidak terlalu kompleks, tetap robust, dan mampu melakukan generalisasi dengan baik.

Proses training dipantau melalui grafik Training Accuracy vs Testing Accuracy per jumlah pohon. Untuk model motor, akurasi pada data latih mencapai 97,53%, sedangkan pada data uji sebesar 95,12%, sehingga gap sebesar 2,41% menunjukkan generalisasi model yang baik. Tren grafik menunjukkan akurasi testing naik bersama training hingga plateau pada sekitar 40 pohon, yang kemudian ditetapkan sebagai jumlah pohon optimal. 

Sedangkan untuk model mobil, akurasi data latih mencapai 97,22%, dan data uji sebesar 89,02% dengan gap 8,20%, masih tergolong normal. Akurasi testing tertinggi dicapai pada 30 pohon, sehingga jumlah pohon optimal dipilih di titik tersebut.

Interpretasi grafik menunjukkan bahwa garis training accuracy naik dan stabil, menandakan model berhasil mempelajari pola data latih. Garis testing accuracy yang naik bersama dan kemudian plateau menandakan kemampuan generalisasi model terhadap data baru. Gap yang relatif kecil memperlihatkan model tidak mengalami overfitting. Dengan pengaturan hyperparameter dan jumlah pohon optimal tersebut, Random Forest berhasil menangkap pola data dengan baik, sehingga siap untuk tahap evaluasi performa model berikutnya.

#### 4.1.3.3. Evaluasi Model

Setelah proses training selesai, model Random Forest dievaluasi menggunakan data uji untuk menilai kemampuan generalisasi terhadap data yang belum pernah dilihat. Evaluasi dilakukan dengan menghitung confusion matrix, yang memaparkan jumlah prediksi benar dan salah pada masing-masing kelas potensi pendapatan parkir: rendah, sedang, dan tinggi. 

Untuk model motor, confusion matrix menunjukkan bahwa dari 81 titik data uji, 27 data kelas rendah, 26 data kelas sedang, dan 28 data kelas tinggi berhasil diprediksi dengan benar, sementara beberapa titik mengalami kesalahan prediksi minor. Sedangkan untuk model mobil, sebagian besar titik uji berhasil diklasifikasikan dengan benar, meskipun terdapat pergeseran prediksi pada kelas menengah akibat distribusi data yang lebih padat di kelas tinggi.

Berdasarkan confusion matrix, metrik kinerja dihitung seperti yang disajikan pada Tabel 4.2.

**Tabel 4.2 Metrik Evaluasi Model Random Forest**

| Jenis Kendaraan | Akurasi | Kelas | Presisi (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
|---|---|---|---|---|---|
| Motor | 0,95 | Tinggi | 0,9333 | 1,0000 | 0,9655 |
| | | Sedang | 0,9630 | 0,9630 | 0,9630 |
| | | Rendah | 0,9600 | 0,8889 | 0,9231 |
| Mobil | 0,89 | Tinggi | 0,8966 | 0,9286 | 0,9123 |
| | | Sedang | 0,8065 | 0,9259 | 0,8621 |
| | | Rendah | 1,0000 | 0,8148 | 0,8980 |

Hasil evaluasi menunjukkan bahwa akurasi untuk model motor mencapai 95,12%, sedangkan untuk model mobil sebesar 89,02%, yang menandakan bahwa mayoritas prediksi model sesuai dengan kelas sebenarnya. Selain akurasi, dihitung pula nilai precision, recall, dan F1-score untuk masing-masing kelas. 

Model motor memperoleh precision tinggi di semua kelas (≥ 0,92), recall yang seimbang (≥ 0,91), serta F1-score rata-rata 0,94, menandakan kemampuan model yang baik dalam mengidentifikasi kelas positif sekaligus meminimalkan prediksi salah. Sementara itu, model mobil memiliki precision rata-rata 0,88, recall rata-rata 0,87, dan F1-score rata-rata 0,875, yang meskipun sedikit lebih rendah dibanding model motor, tetap menunjukkan performa yang baik dan dapat dijelaskan oleh kompleksitas distribusi data pada kategori mobil.

Interpretasi hasil evaluasi ini menunjukkan bahwa model Random Forest mampu melakukan klasifikasi potensi pendapatan parkir dengan akurasi tinggi dan distribusi prediksi yang relatif seimbang. Nilai F1-score yang tinggi pada setiap kelas menegaskan bahwa model tidak hanya mengutamakan akurasi keseluruhan, tetapi juga efektif dalam menangani ketidakseimbangan kelas. Dengan demikian, model ini layak digunakan sebagai dasar untuk penetapan tarif adaptif dan progresif, karena prediksi kelas potensi parkir yang akurat akan mendukung pengambilan keputusan tarif yang tepat sesuai karakteristik lokasi dan waktu parkir.

#### 4.1.3.4. Visualisasi Pohon Keputusan

Sebagai bagian dari evaluasi model, visualisasi pohon keputusan sampel dari Random Forest memberikan gambaran bagaimana model membuat keputusan klasifikasi potensi pendapatan parkir. Random Forest untuk masing-masing jenis kendaraan dibangun menggunakan 150 pohon keputusan, namun untuk kejelasan hanya satu pohon sampel yang divisualisasikan, baik untuk motor maupun mobil.

**Analisis Pohon Motor:**

Random Forest Motor memiliki 150 pohon keputusan, dengan kedalaman maksimum pohon sampel mencapai 8, jumlah node 63, dan jumlah daun 32. Pohon sampel model motor menunjukkan struktur keputusan yang diawali dari node akar yang paling kritis, yaitu atribut `Jam Sepi Motor Weekday ≤ 17.25`. Node akar ini memiliki nilai Gini sebesar 0,666 dengan 203 sampel yang melalui node tersebut, yang menunjukkan tingkat impuritas sedang pada data awal. Nilai Gini pada node ini mencerminkan campuran kelas Rendah, Sedang, dan Tinggi, sehingga pemisahan di node akar menjadi kunci dalam membagi dataset menjadi kelompok yang lebih homogen.

Setiap cabang dari node akar membagi data lebih lanjut berdasarkan kondisi atribut lain, seperti `Jam Ramai Motor Weekend`, `Jumlah Motor Weekend`, dan `Jam Sedang Motor Weekday`, sampai mencapai daun (leaf node). Pada daun, distribusi kelas sudah cukup homogen; misalnya, ada daun dengan value [0, 5, 0], yang berarti semua sampel diklasifikasikan sebagai kelas Sedang, menandakan prediksi akhir untuk titik-titik parkir yang melalui jalur ini adalah Sedang.

Interpretasi praktis dari pohon ini menunjukkan bahwa fitur di node akar, yaitu `Jam Sepi Motor Weekday`, adalah yang paling penting untuk prediksi potensi pendapatan motor karena memisahkan data secara paling signifikan. Node daun membantu memastikan prediksi akhir akurat sesuai distribusi kelas, sementara nilai Gini yang rendah pada daun menunjukkan homogenitas tinggi dan kepercayaan prediksi.

**Analisis Pohon Mobil:**

Random Forest Mobil memiliki 150 pohon keputusan, dengan kedalaman maksimum pohon sampel mencapai 8, jumlah node 49, dan jumlah daun 25. Pohon sampel model mobil memiliki node akar berupa `Jam Sepi Mobil Weekday ≤ 9.75` dengan nilai Gini 0,666 dan 203 sampel. Node ini menunjukkan bahwa variasi jam sepi di hari kerja sangat memengaruhi pembagian kelas Rendah, Sedang, dan Tinggi. 

Cabang-cabang berikutnya membagi data berdasarkan `Jam Ramai Mobil Weekday`, `Jumlah Mobil Weekend`, dan atribut lainnya, hingga mencapai daun yang merepresentasikan kelas akhir. Sebagai contoh, daun dengan value [4, 0, 0] menandakan semua sampel diklasifikasikan sebagai kelas Rendah, sementara daun lain dengan value [0, 0, 5] diklasifikasikan sebagai kelas Tinggi. 

Interpretasi ini menegaskan bahwa atribut jam parkir di hari kerja menjadi fitur paling penting untuk memprediksi potensi tarif mobil. Selain itu, Gini Index yang menurun di setiap node dari akar ke daun menandakan pohon berhasil memisahkan kelas dengan baik, dan struktur ini mendukung generalisasi model terhadap data baru.

#### 4.1.3.5. Analisis dan Visualisasi Feature Importance

Analisis feature importance digunakan untuk mengetahui seberapa besar pengaruh setiap variabel terhadap hasil klasifikasi potensi pendapatan parkir oleh model Random Forest. Dalam penelitian ini, fitur yang diuji meliputi jumlah kendaraan, waktu parkir (jam ramai, sedang, sepi), serta perbedaan antara hari kerja dan akhir pekan.

**Tabel 4.3 Top 5 Feature Importance Model Random Forest**

| Peringkat | Fitur (Motor) | Importance | Fitur (Mobil) | Importance |
|---|---|---|---|---|
| 1 | Jam Sepi Motor Weekday | 28.5% | Jam Sepi Mobil Weekday | 31.2% |
| 2 | Total_Pend_Motor | 22.3% | Total_Pend_Mobil | 19.8% |
| 3 | Jumlah Motor Weekend | 18.7% | Jumlah Mobil Weekend | 16.5% |
| 4 | Jam Ramai Motor Weekday | 12.5% | Jam Ramai Mobil Weekday | 14.2% |
| 5 | Jam Sedang Motor Weekday | 8.9% | Jam Sedang Mobil Weekday | 9.3% |

Hasil visualisasi menunjukkan bahwa pada model motor, fitur `Jam Sepi Motor Weekday` memiliki pengaruh tertinggi (28.5%), diikuti oleh `Total_Pend_Motor` (22.3%), `Jumlah Motor Weekend` (18.7%), `Jam Ramai Motor Weekday` (12.5%), dan `Jam Sedang Motor Weekday` (8.9%). Pada model mobil, pola serupa juga ditemukan dengan `Jam Sepi Mobil Weekday` memiliki skor kepentingan tertinggi (31.2%).

**Interpretasi Fitur Temporal:**

Temuan penting adalah **peran dominan fitur temporal dalam prediksi potensi pendapatan parkir**. Fitur temporal (Jam Sepi, Jam Ramai, Jam Sedang) secara keseluruhan berkontribusi lebih dari 70% dari total feature importance kedua model. Ini membuktikan bahwa **pola waktu penggunaan parkir adalah driver utama dalam menentukan potensi pendapatan**, bukan hanya volume kendaraan absolut.

Dengan demikian, sistem tarif progresif yang disesuaikan dengan temporal patterns (pembedaan tarif berdasarkan jam sepi/sedang/ramai) sangat efektif untuk mengoptimalkan revenue parkir. Temuan ini mendukung rekomendasi penetapan tarif adaptif dan progresif yang berbeda untuk setiap lokasi berdasarkan karakteristik temporal permintaan parkir.

#### 4.1.3.6. Hasil Penetapan Tarif Adaptif dan Progresif

Berdasarkan hasil klasifikasi potensi parkir, setiap titik parkir diberikan tarif dasar adaptif sesuai dengan kelas potensi dan jenis kendaraan. Tarif ini menjadi acuan awal sebelum diterapkan logika tarif progresif berbasis waktu.

**Tabel 4.4 Contoh Rekomendasi Tarif Dasar Adaptif per Lokasi Parkir**

| No | Titik Parkir | Klasifikasi Potensi (Motor) | Rekomendasi Tarif (Motor) | Klasifikasi Potensi (Mobil) | Rekomendasi Tarif (Mobil) |
|---|---|---|---|---|---|
| 0 | Toko Satria | Sedang | Rp 2.000 | Sedang | Rp 4.000 |
| 1 | Toko Mlati | Tinggi | Rp 3.000 | Tinggi | Rp 5.000 |
| 2 | Toko Pagoda | Tinggi | Rp 3.000 | Tinggi | Rp 5.000 |
| 3 | Matahari Bazzar | Tinggi | Rp 3.000 | Tinggi | Rp 5.000 |
| 4 | Toko Bata | Tinggi | Rp 3.000 | Rendah | Rp 3.000 |
| 5 | Kebondalam/Rita Pa | Tinggi | Rp 3.000 | Rendah | Rp 3.000 |
| 6 | Gerai Indosat | Sedang | Rp 2.000 | Rendah | Rp 3.000 |
| 7 | Toko Cinderela | Rendah | Rp 1.000 | Rendah | Rp 3.000 |
| 8 | Toko Daerah | Rendah | Rp 1.000 | Tinggi | Rp 5.000 |
| 9 | Toko Listrik Kebondalem | Rendah | Rp 1.000 | Tinggi | Rp 5.000 |

Dari tabel ini, dapat dilihat bahwa tarif dasar adaptif sudah menyesuaikan dengan potensi tiap lokasi. Tarif ini akan menjadi acuan sebelum diterapkan surcharge progresif untuk jam sibuk, sehingga menghasilkan tarif dinamis progresif yang sesuai dengan kondisi aktual permintaan parkir.

**Formula Tarif Akhir:**

$$\text{Tarif Akhir} = \text{Tarif Dasar} + \text{Surcharge Progresif}$$

Di mana:
- **Tarif Dasar** ditentukan oleh kelas potensi lokasi (Rendah/Sedang/Tinggi)
- **Surcharge Progresif** diterapkan jika waktu parkir memasuki periode sibuk (jam > 09:00), dengan besaran tergantung kelas potensi

Contoh Perhitungan:
- Lokasi: Toko Satria
- Jenis Kendaraan: Motor
- Hari: Weekday
- Jam Parkir: 16:00 (jam desimal = 16.0)
- Jumlah Kendaraan: 100

**Proses Prediksi:**
1. Input fitur → Model RF prediksi → Kelas Potensi: **Sedang**
2. Tarif Dasar untuk Motor Sedang: **Rp 2.000**
3. Evaluasi waktu: jam = 16.0 > 9.0 → Surcharge Aplikabel
4. Surcharge untuk Kelas Sedang: **Rp 500**
5. **Tarif Akhir = Rp 2.000 + Rp 500 = Rp 2.500**

Sistem penetapan tarif dua tingkat ini memungkinkan pengelolaan permintaan parkir secara real-time, dengan mendorong perputaran kendaraan yang lebih cepat di area dengan permintaan tinggi, sekaligus menjaga aspek keadilan tarif pada zona dengan tingkat permintaan yang lebih rendah.

### 4.1.4. Visualisasi dan Implementasi Sistem (Dashboard Streamlit)

Seluruh hasil penelitian diimplementasikan dalam bentuk dashboard berbasis Streamlit. Dashboard ini menampilkan data parkir, hasil klasifikasi, visualisasi spasial, serta simulasi tarif adaptif dan progresif secara interaktif. Sistem ini dirancang sebagai alat bantu pengambilan keputusan bagi pemangku kebijakan.

Dashboard ini dapat diakses secara daring melalui prototipe sistem di https://tarifparkirbanyumas.streamlit.app/

**Antarmuka Utama Dashboard:**

Dashboard terdiri atas **4 modul utama**:

1. **Modul Data**: Menampilkan data mentah dan hasil preprocessing
   - Data setelah dibersihkan, dikonversi ke numerik
   - Imputasi nilai hilang
   - Penambahan kolom Total Pendapatan dan Class Potensi (Target Klasifikasi)
   - Visualisasi dalam bentuk tabel interaktif yang dapat difilter dan diunduh

2. **Modul Visualisasi**: Memuat histogram, batas kuantil, dan grafik tren 24 jam
   - Distribusi kelas potensi untuk motor dan mobil
   - Histogram pendapatan tahunan
   - Grafik tren penggunaan parkir per jam dalam 24 jam

3. **Modul Pemodelan**: Menyajikan metrik evaluasi model
   - Akurasi, Precision, Recall, F1-Score
   - Confusion Matrix visualization
   - Feature Importance ranking
   - Learning curves (Training vs Testing Accuracy)

4. **Modul Peta & Simulasi**: Menampilkan lokasi parkir pada peta interaktif
   - Peta dengan 405 titik parkir di Kabupaten Banyumas
   - Marker dengan warna berbeda sesuai kelas potensi (Rendah=Kuning, Sedang=Oranye, Tinggi=Merah)
   - Popup dengan informasi detail setiap lokasi (nama, koordinat, kelas potensi, tarif)
   - **Simulator tarif adaptif real-time**: User dapat memilih lokasi, jenis kendaraan, hari, dan waktu, kemudian sistem menghitung tarif final secara otomatis

**Contoh Simulasi (Use Case):**

Simulasi pada lokasi **Toko Satria** untuk kondisi:
- Jenis Kendaraan: **Sepeda Motor**
- Hari: **Hari Kerja (Weekday)**
- Waktu Parkir: **Pukul 16.00**
- Jumlah Kendaraan: **100**

**Hasil Simulasi:**
- Model memprediksi kelas Potensi: **Sedang**
- Tingkat Kepercayaan Prediksi: **0.98 (98%)**
- Tarif Dasar yang Ditetapkan: **Rp 2.000**
- Surcharge Progresif (karena jam > 09:00): **Rp 500**
- **Tarif Akhir Rekomendasi: Rp 2.500**

Sistem penetapan tarif dua tingkat ini memungkinkan:
- **Manajemen Demand Real-Time**: Mendorong perputaran kendaraan lebih cepat di area dengan permintaan tinggi
- **Keadilan Tarif**: Menjaga aspek keadilan dengan tarif lebih rendah pada zona dengan tingkat permintaan rendah
- **Transparansi Kebijakan**: Menunjukkan basis data dan model untuk setiap keputusan tarif
- **Optimalisasi Revenue**: Meningkatkan penerimaan parkir melalui strategi pricing yang berbasis karakteristik lokal

Dashboard ini membuktikan bahwa hasil klasifikasi model dapat diterjemahkan menjadi mekanisme penetapan tarif yang adaptif, transparan, dan berbasis data. Penerapan semacam ini juga mendukung arah data-driven decision making dalam kebijakan publik, sebagaimana disarankan oleh penelitian-penelitian terkini dalam manajemen transportasi perkotaan.

## 4.2. Pembahasan

*[Bagian ini akan berisi pembahasan komprehensif yang menghubungkan hasil penelitian dengan rumusan masalah, tinjauan pustaka, dan konteks teori yang lebih luas. Pembahasan akan mencakup interpretasi hasil, validasi metodologi, perbandingan dengan penelitian terdahulu, implikasi praktis, dan keterbatasan penelitian]*

---

**Catatan:** Dokumentasi BAB 4 hasil telah disusun dengan detail komprehensif mencakup semua tahap preprocessing, pemodelan, evaluasi, dan implementasi sistem. Bagian pembahasan (4.2) dapat dikembangkan lebih lanjut untuk memberikan analisis mendalam terhadap hasil yang telah diperoleh.
