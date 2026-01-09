# 1.5 Batasan Masalah

## Definisi Batasan Masalah
Batasan penelitian mencakup ruang lingkup dalam penelitian, kondisi dan/atau asumsi yang telah ada pada rumusan masalah. Batasan tidak terlalu melebar ataupun terlalu sempit dengan kerasionalan untuk keadaan sebenarnya. Batasan penelitian ini digunakan untuk menentukan keadaan-keadaan apa suatu penyelesaian masalah (solusi/hasil penelitian) dikatakan berlaku.

## Batasan Penelitian Sistem Prediksi Tarif Parkir Progresif Banyumas

### 1. **Batasan Geografis**
Penelitian ini hanya berfokus pada data tarif parkir di wilayah **Kabupaten Banyumas**, Jawa Tengah. Hasil dan model yang dikembangkan hanya berlaku untuk konteks parkir kendaraan di daerah Banyumas dan tidak dapat digeneralisasi secara langsung untuk daerah lain tanpa penyesuaian.

### 2. **Batasan Jenis Kendaraan**
Penelitian hanya menganalisis dua jenis kendaraan, yaitu:
- **Sepeda Motor (Roda Dua)**
- **Mobil Penumpang (Roda Empat)**

Jenis kendaraan lain seperti truk, bus, atau kendaraan khusus tidak termasuk dalam ruang lingkup penelitian ini.

### 3. **Batasan Data dan Periode Waktu**
- Data yang digunakan adalah data historis tarif parkir dan volume kendaraan yang tersedia dari sumber resmi (dinas terkait Kabupaten Banyumas).
- Periode data yang dianalisis adalah **tahun 2023-2024** atau sesuai dengan ketersediaan data yang valid dan lengkap.
- Data yang hilang (missing data) atau tidak konsisten akan dihilangkan atau diimputasi dengan metode yang sesuai.

### 4. **Batasan Fitur dan Variabel**
Model pembelajaran mesin hanya menggunakan fitur yang tersedia dari dataset, yang mencakup:
- Volume kendaraan (motor dan mobil) pada hari kerja dan akhir pekan
- Waktu (jam operasional parkir)
- Data historis tarif yang tercatat

Faktor eksternal lainnya seperti kondisi cuaca, event khusus, atau situasi ekonomi makro tidak dipertimbangkan dalam model ini, meskipun dapat mempengaruhi hasil prediksi di dunia nyata.

### 5. **Batasan Fenomena Masalah**
Penelitian ini menggunakan pendekatan **probabilistik** dalam mengembangkan model Random Forest. Prediksi tarif parkir bersifat kemungkinan (probabilitas), bukan kepastian determinatif. Oleh karena itu, hasil prediksi dapat memiliki margin error dan tidak menjamin akurasi 100% dalam semua kasus.

### 6. **Batasan Kategori Output**
Model memprediksi tarif parkir dalam tiga kategori ketegori potensi tarif:
- **Tarif Rendah (Rendah):** Wilayah dengan permintaan parkir rendah
- **Tarif Sedang (Sedang):** Wilayah dengan permintaan parkir sedang
- **Tarif Tinggi (Tinggi):** Wilayah dengan permintaan parkir tinggi

Sistem ini tidak memprediksi nilai tarif absolut dalam rupiah, tetapi klasifikasi potensi level tarif berdasarkan pola data historis.

### 7. **Batasan Implementasi dan Sistem**
- Model dikembangkan menggunakan algoritma **Random Forest Classifier** dengan parameter optimal yang telah diuji (n_estimators=150, max_depth=15, min_samples_leaf=3).
- Dashboard interaktif dibangun menggunakan framework **Streamlit** untuk visualisasi data dan hasil prediksi.
- Implementasi terbatas pada environment Python 3.10+ dengan library-library yang tersedia di `requirements.txt`.

### 8. **Batasan Waktu dan Sumber Daya**
- Penelitian ini dilakukan dengan menggunakan sumber daya yang tersedia dari data publik dan open-source tools.
- Model dilatih dan divalidasi menggunakan dataset yang ada tanpa pengumpulan data primer tambahan (survei langsung atau observasi lapangan).

### 9. **Batasan Akurasi dan Generalisasi**
- Akurasi prediksi model didasarkan pada data historis yang tersedia. Perubahan pola signifikan di masa depan dapat mengurangi akurasi prediksi.
- Model tidak dapat memprediksi situasi yang belum pernah terjadi dalam data historis (black swan events).
- Akurasi model pada data uji mencapai **89-95%** (tergantung jenis kendaraan), namun dapat bervariasi untuk data baru di masa depan.

### 10. **Batasan Asumsi**
- Diasumsikan bahwa data yang digunakan adalah **akurat dan representatif** dari kondisi sesungguhnya.
- Diasumsikan bahwa pola historis tarif dan volume kendaraan akan terus berlanjut dengan tren yang serupa.
- Diasumsikan tidak ada perubahan kebijakan tarif parkir yang drastis selama periode penelitian.

## Implikasi Batasan Penelitian

Dengan batasan-batasan di atas, hasil penelitian ini **berlaku untuk**:
- Prediksi potensi tarif parkir untuk kendaraan roda dua dan roda empat di Kabupaten Banyumas.
- Penentuan strategi tarif progresif yang rasional berdasarkan pola demand.
- Rekomendasi kebijakan tarif parkir untuk dinas terkait Kabupaten Banyumas.
- Analisis tren dan pola volume kendaraan serta permintaan parkir di wilayah Banyumas.

Sementara hasil **TIDAK berlaku untuk**:
- Prediksi tarif parkir di daerah lain tanpa penyesuaian model (overgeneralisasi).
- Prediksi situasi ekstrem atau kondisi yang tidak terdapat dalam data historis.
- Penentuan nilai tarif absolut (hanya prediksi kategori/level tarif).
- Analisis faktor eksternal di luar data yang disediakan (cuaca, event, ekonomi global).

---

**Dokumen ini merupakan bagian dari laporan skripsi:**  
*Sistem Prediksi Tarif Parkir Progresif Menggunakan Random Forest untuk Optimalisasi Pendapatan Parkir Kabupaten Banyumas*
