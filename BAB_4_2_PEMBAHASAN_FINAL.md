# BAB 4.2: PEMBAHASAN

---

## **4.2.1 Pengelompokan Titik Parkir Berdasarkan Atribut Kendaraan dan Pola Waktu Penggunaan**

Hasil klasifikasi menunjukkan bahwa pengelompokan titik parkir berdasarkan **atribut kendaraan (motor dan mobil) serta pola waktu penggunaan (weekday dan weekend)** mampu membentuk **tiga kategori potensi pendapatan — Rendah, Sedang, dan Tinggi** — menggunakan ambang kuantil pendapatan tahunan aktual. Pendekatan ini memungkinkan setiap titik parkir diidentifikasi tidak hanya berdasarkan volume kendaraan, tetapi juga **intensitas temporalnya (jam ramai, sedang, sepi)**.

### Analisis Kontribusi Pendapatan per Jenis Kendaraan

Analisis kuantitatif pada dashboard menunjukkan bahwa **motor memiliki kontribusi pendapatan total lebih tinggi dibandingkan mobil**, meskipun tarif dasarnya lebih rendah. Hal ini disebabkan oleh **frekuensi dan durasi parkir motor yang jauh lebih tinggi**. Temuan ini sejalan dengan studi yang menunjukkan bahwa **frekuensi parkir memiliki dampak lebih signifikan terhadap total pendapatan dibandingkan tarif per satuan kendaraan**.

**Tabel 4.2.1: Karakteristik Kategori Pengelompokan**

| Kategori | Motor (%) | Mobil (%) | Volume Kendaraan (unit/hari) | Jam Operasional | Konteks Lokasi |
|----------|-----------|-----------|-----|-----------------|---|
| **Rendah** | 33.3% | 33.3% | 45-80 motor, 30-60 mobil | 4-6 jam ramai | Area permukiman, zone rendah intensitas |
| **Sedang** | 33.3% | 33.3% | 80-150 motor, 60-150 mobil | 6-8 jam ramai | Commercial area, zone moderat |
| **Tinggi** | 33.3% | 33.3% | 150-280 motor, 100-200 mobil | 8-12 jam ramai | CBD, pusat perdagangan & perkantoran |

### Pola Temporal dan Teori Demand Management

Secara visual, **grafik Load vs Waktu (24 jam)** pada dashboard memperlihatkan adanya **puncak aktivitas parkir pada jam 09.00–17.00**, terutama untuk kendaraan roda dua. Pola temporal ini memperkuat teori **Transportation Demand Management (TDM)** yang menyatakan bahwa perbedaan kepadatan parkir berdasarkan waktu merupakan **indikator penting dalam desain tarif adaptif**. 

Dengan demikian, **pengelompokan berbasis waktu tidak hanya relevan secara statistik**, tetapi juga memiliki **dasar teoretis yang kuat untuk pengendalian permintaan parkir**. Hasil pengelompokan ini mendukung diferensiasi tarif progresif:

- **Kategori Rendah**: Memerlukan tarif dasar lebih rendah (Rp1.000-3.000) untuk maintain accessibility
- **Kategori Sedang**: Memerlukan tarif moderat (Rp2.000-4.000) untuk balance antara revenue dan service  
- **Kategori Tinggi**: Dapat menerapkan tarif lebih tinggi (Rp3.000-5.000) dengan strategi demand management

**Kesimpulan RM1**: RM1 berhasil dijawab — pengelompokan berdasarkan **atribut kendaraan dan pola waktu penggunaan** dapat dilakukan dengan **metode Quantile Binning yang efektif**, menghasilkan tiga kategori yang **balanced, meaningful, dan implementable sebagai dasar kebijakan tarif progresif**.

---

## **4.2.2 Penerapan Algoritma Random Forest dalam Klasifikasi Potensi Pendapatan**

Model **Random Forest Classifier** berhasil memberikan **kinerja yang sangat baik**, dengan tingkat akurasi:
- **Motor: 95.12%** 
- **Mobil: 89.02%**

Tingginya nilai **presisi dan recall** menunjukkan bahwa **model mampu membedakan kelas potensi pendapatan secara stabil**, bahkan dalam kondisi data yang heterogen. **Visualisasi confusion matrix** mengonfirmasi bahwa mayoritas prediksi berada di diagonal utama, yang berarti **tingkat salah klasifikasi relatif rendah**.

**Tabel 4.2.2: Performa Model Random Forest**

| Metrik | Motor | Mobil |
|--------|-------|-------|
| **Training Accuracy** | 97.53% | 97.22% |
| **Testing Accuracy** | 95.12% | 89.02% |
| **Train-Test Gap** | 2.41% | 8.20% |

Hasil ini **konsisten dengan penelitian terkini** yang menyimpulkan bahwa **Random Forest merupakan algoritma yang paling stabil** untuk prediksi okupansi dan klasifikasi tarif parkir karena mampu menangani variabel spasial-temporal secara simultan serta tahan terhadap noise.

### Analisis Feature Importance

**Analisis feature importance memperlihatkan bahwa variabel jumlah kendaraan (weekday dan weekend) merupakan faktor paling dominan** dalam menentukan kelas potensi pendapatan, diikuti oleh variabel jam ramai dan jam sedang.

**Tabel 4.2.3: Top 10 Most Important Features (Motor Model)**

| Rank | Feature | Importance (%) | Deskripsi |
|------|---------|-----------------|-----------|
| 1 | Jam Sepi Motor Weekday | 28.5% | **PALING KRITIS**: Volume pada jam sepi weekday adalah predictor terkuat |
| 2 | Total_Pend_Motor | 22.3% | Pendapatan motor tahunan sangat berpengaruh |
| 3 | Jumlah Motor Weekend | 18.7% | Volume weekend juga signifikan |
| 4 | Jam Ramai Motor Weekday | 12.5% | Peak hour volume berpengaruh sedang |
| 5 | Jam Sedang Motor Weekday | 8.9% | Moderate hour volume berpengaruh kecil |
| 6-10 | Other features | <5% each | Features lain memiliki kontribusi minimal |

**Key Insight**: Temuan menunjukkan bahwa **intensitas dan kepadatan kendaraan lebih menentukan potensi pendapatan dibandingkan lokasi semata**, serta bahwa **pola temporal (khususnya jam sepi) lebih berpengaruh daripada agregat volume keseluruhan**.

### Validasi Performa per Kelas

**Tabel 4.2.4: Classification Report - Motor Model**

| Kelas | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Rendah | 0.94 | 0.93 | 0.94 |
| Sedang | 0.96 | 0.94 | 0.95 |
| Tinggi | 0.95 | 0.99 | 0.97 |
| **Weighted Avg** | **0.95** | **0.95** | **0.95** |

Konsistensi precision dan recall menunjukkan bahwa **model tidak melakukan trade-off** antara false positive vs false negative—kedua error type diminimalkan secara bersamaan. Ini penting untuk policy application karena:
- Tinggi precision → Rekomendasi tarif tidak salah-sasaran
- Tinggi recall → Tidak banyak lokasi high-potential yang terlewatkan

**Kesimpulan RM2**: RM2 berhasil dijawab — Algoritma Random Forest **dapat membangun model klasifikasi yang reliabel, akurat (95.12% motor, 89.02% mobil), dan interpretable**, serta dapat digunakan sebagai dasar bagi **kebijakan tarif progresif adaptif**. Model menunjukkan generalisasi yang dapat diandalkan dan stabil tanpa overfitting.

---

## **4.2.3 Visualisasi Geospasial dan Sistem Pendukung Keputusan**

Analisis spasial dalam penelitian ini **berfungsi sebagai pendekatan untuk mengaitkan hasil klasifikasi potensi pendapatan parkir dengan konteks geografis** di wilayah Kabupaten Banyumas. Data koordinat (latitude–longitude) setiap titik parkir dimanfaatkan untuk membangun **visualisasi geospasial interaktif** yang memetakan distribusi kelas potensi pendapatan—Rendah, Sedang, dan Tinggi—melalui peta berbasis **Folium**. 

Peta ini menampilkan **405 titik parkir** yang diberi penanda (marker) sesuai hasil klasifikasi algoritma Random Forest, lengkap dengan atribut seperti nama lokasi, kategori potensi tarif, dan estimasi pendapatan tahunan.

### Pola Spasial dan Implikasi Geografis

Visualisasi tersebut menunjukkan **pola yang jelas**: 
- **Titik parkir dengan potensi pendapatan Tinggi** cenderung **terkonsentrasi di kawasan dengan aktivitas ekonomi padat** seperti pusat perdagangan dan perkantoran
- **Kelas Rendah** banyak ditemukan di **area permukiman atau zona dengan intensitas kendaraan rendah**

Temuan ini **memperkuat konsep bahwa faktor spasial memiliki pengaruh signifikan terhadap variasi pendapatan parkir**. Integrasi machine learning dengan GIS-based mapping memungkinkan pemetaan distribusi spasial potensi ekonomi transportasi secara lebih akurat, sebagaimana ditunjukkan dalam penelitian terkini tentang smart cities dan geospatial analysis.

### Implementasi Decision Support System (DSS)

#### Peta Interaktif Berbasis Folium

Sistem visualisasi dikembangkan menggunakan **Folium library** dengan spesifikasi teknis:

**Tabel 4.2.5: Spesifikasi Visualisasi Peta Interaktif**

| Komponen | Detail | Fungsi |
|----------|--------|--------|
| **Base Map** | OpenStreetMap tiles + Esri Satellite option | Konteks geografis lokasi parkir |
| **Marker Layer** | CircleMarker untuk 405 lokasi | Plot lokasi dengan coordinate accuracy |
| **Popup Information** | HTML-formatted popup on marker click | Display: Lokasi, Lat-Lon, Motor & Mobil potensi + tarif |
| **Search Plugin** | Geo-search untuk mencari lokasi by name | Facilitate user exploration |
| **Layer Control** | Toggle antara OSM dan Satellite | Flexible visualization perspective |
| **Zoom Level** | Default zoom 13 (city-level) | Optimal viewing untuk 405 lokasi |

Ketika user mengklik marker, **popup menampilkan informasi detail**: nama lokasi, potensi pendapatan (Rendah/Sedang/Tinggi), dan rekomendasi tarif dasar per jenis kendaraan.

#### Simulator Dinamis untuk What-If Analysis

Hasil pemetaan tersebut **diintegrasikan dalam dashboard berbasis Streamlit yang berfungsi sebagai Decision Support System (DSS)** untuk pengambil kebijakan. Dashboard ini tidak hanya menampilkan hasil klasifikasi dan peta potensi pendapatan, tetapi juga **menyediakan fitur simulator dinamis (what-if analysis) yang memungkinkan pengguna menguji skenario berbeda secara real-time**.

Pengambil kebijakan dapat:
1. **Pilih lokasi parkir** (dropdown dengan 405 opsi)
2. **Pilih jenis kendaraan** (Motor / Mobil)
3. **Memodifikasi jumlah kendaraan atau jam parkir** dan langsung melihat dampaknya terhadap:
   - Prediksi potensi pendapatan
   - Tarif progresif yang dihasilkan model
   - Proyeksi revenue harian/bulanan

**Pendekatan ini menjadikan sistem lebih dari sekadar alat analisis; ia berperan sebagai alat bantu keputusan berbasis data (data-driven decision system)** yang mendukung formulasi kebijakan tarif parkir secara adaptif dan objektif.

#### Algoritma Tarif Progresif Dinamis

Dashboard menerapkan **logika tarif yang adaptif dan progresif**:

```
Tarif Akhir = Tarif Dasar (berdasarkan class) + Surcharge (berdasarkan waktu)

Contoh (Motor, Potensi Tinggi):
- Jam Ramai (09:00-17:00):     Rp3.000 + Rp1.000 = Rp4.000/jam
- Jam Sedang (17:00-22:00):    Rp3.000 + Rp500   = Rp3.500/jam
- Jam Sepi (06:00-09:00):      Rp3.000 + Rp500   = Rp3.500/jam
```

Algoritma ini **adaptif** (base rate responsive terhadap potensi) dan **progresif** (surcharge meningkat dengan class dan peak hours), sehingga mendorong demand spreading tanpa mengorbankan revenue.

### Peran DSS dalam Pengambilan Keputusan Kebijakan

Konsep ini sejalan dengan penelitian terkini yang menunjukkan bahwa **smart parking DSS berbasis data spasial dan analisis prediktif mampu mempercepat proses pengambilan keputusan serta meningkatkan efisiensi manajemen parkir** di wilayah perkotaan. Dengan demikian, sistem DSS yang dikembangkan dalam penelitian ini dapat dianggap sebagai bentuk penerapan konkret prinsip **evidence-based policy making di tingkat daerah**.

**Contoh Use Case**: Dinas Perhubungan ingin meningkatkan revenue 20%. Melalui simulator, dapat ditest:
- **Skenario A**: Uniform tariff increase 10% → Revenue naik 4.75% (kurang)
- **Skenario B**: Targeted increase kelas Tinggi +30% → Revenue naik 13.5% (mendekati)
- **Skenario C**: Progressive surcharge peak hours → Revenue naik 22% ✅ (OPTIMAL)
- **Decision**: Implementasi Skenario C dengan confidence tinggi berdasarkan data

#### Desain Antarmuka dan Aksesibilitas

Dari sisi rancangan antarmuka, **visualisasi spasial dalam dashboard dirancang agar mudah diakses dan dipahami**, bahkan oleh pengambil kebijakan non-teknis. Desain antarmuka mengutamakan **kesederhanaan visual dengan peta tematik dan panel interaktif** yang memungkinkan eksplorasi hasil tanpa perlu pemahaman teknis mendalam tentang machine learning. 

Pendekatan ini meningkatkan **transparansi serta mendorong keterlibatan publik** dalam proses kebijakan karena memudahkan interpretasi data yang kompleks melalui visualisasi berbasis peta interaktif.

### Kesimpulan RM3

**RM3 berhasil dijawab**: Hasil klasifikasi potensi pendapatan parkir **dapat divisualisasikan secara geografis melalui peta interaktif dan simulator dinamis** yang berfungsi sebagai **Decision Support System untuk policy makers**. 

Implementasi **peta interaktif berbasis data real-time memungkinkan kebijakan tarif progresif disusun dengan mempertimbangkan perbedaan spasial dan temporal permintaan parkir**. Dengan mengintegrasikan pendekatan machine learning, analisis spasial, dan visualisasi interaktif, penelitian ini berhasil menghadirkan **model kebijakan tarif parkir yang adaptif, transparan, dan berbasis bukti empiris (data-driven policy)**.

---

## **4.2.4 Integrasi Sistem Keseluruhan**

Penelitian ini mendemonstrasikan **integrasi seamless** antara tiga komponen inti yang saling mendukung:

1. **Quantile Binning & Feature Engineering** → 3 kategori balanced
2. **Random Forest Classification** → 95.12% akurasi dengan feature importance jelas
3. **Geospatial Visualization + DSS** → Interactive dashboard untuk policy makers

Alur terintegrasi: **Data → Preprocessing → Classification → Visualization → Decision Support → Policy Implementation**

### Kekuatan Pendekatan Terintegrasi

1. **Data-Driven Foundation**: Setiap keputusan kebijakan dapat **traced back** ke data dan model yang transparent
2. **Balance Kuantitatif-Kualitatif**: Quantitative RF model (95% akurasi) + Qualitative visual exploration (interactive map)
3. **Scalability**: Sistem dapat expanded ke lebih banyak lokasi dengan model retrainable
4. **Implementability**: Output langsung actionable dengan low technical barrier untuk implementation

---

## **4.2.5 Kesimpulan Pembahasan**

### Ringkasan Jawaban terhadap 3 Rumusan Masalah

**RM1 - Pengelompokan**: Pengelompokan berhasil dilakukan menggunakan Quantile Binning menghasilkan 3 kategori balanced (33.3% each) dengan korelasi kuat terhadap atribut pembeda (volume kendaraan, pola temporal). Meaningful dan implementable sebagai dasar kebijakan tarif.

**RM2 - Random Forest**: Model RF mencapai performa excellent (95.12% motor, 89.02% mobil) dengan train-test gap kecil, menunjukkan generalisasi robust. Interpretable dengan feature importance ranking jelas. Production-ready untuk decision support.

**RM3 - Visualisasi Spasial & DSS**: Hasil klasifikasi divisualisasikan melalui interactive Folium map (405 lokasi dengan popup detail) dan tariff simulator berbasis algoritma progresif dinamis. Berfungsi sebagai Decision Support System yang accessible untuk non-technical policy makers.

### Kontribusi Penelitian

**Kontribusi Ilmiah:**
- Metodologi hibrida integrasi quantile binning + RF classification + spasial visualization
- Empirical evidence dari konteks urban menengah Indonesia (Kabupaten Banyumas)
- Transparent dan auditable algorithm logic

**Kontribusi Praktis:**
- Dashboard ready-to-use untuk local government policy making
- Proyeksi peningkatan revenue 15-25% dengan maintained accessibility
- Replicable template untuk kota lain dengan konteks serupa

### Alignment dengan Tujuan Penelitian

**Tujuan Umum**: Mengembangkan sistem terintegrasi untuk penetapan tarif parkir adaptif dan progresif dinamis.
**Hasil**: ✅ **TERCAPAI** — Sistem terintegrasi berfungsi seamlessly dengan adaptif base rate dan progresif surcharge

**Tujuan Khusus (TK-1 s/d TK-4)**: Semua tercapai
- TK-1 ✅: 405 lokasi diklasifikasi dengan metode yang jelas
- TK-2 ✅: RF model 95.12% accuracy dengan robust generalisasi
- TK-3 ✅: Tarif adaptif-progresif logic implemented
- TK-4 ✅: Dashboard interactive dengan simulator DSS berfungsi

### Penutup

Penelitian ini mendemonstrasikan bahwa **machine learning dan spasial visualization dapat efektif mendukung public policy formulation** dalam konteks manajemen parkir urban. Pendekatan terintegrasi antara **quantitative modeling (RF)** dan **qualitative visualization (interactive map)** menghasilkan decision support system yang **credible, transparent, dan actionable** untuk local government decision makers.

Sistem ini bukan hanya akademis tetapi **praktis dan implementable**, membuka peluang untuk:
- Peningkatan revenue retribusi parkir dengan objective foundation
- Demand management yang lebih baik melalui dynamic pricing
- Policy making yang lebih data-driven dan transparent
- Template metodologi untuk inovasi layanan publik di pemerintah daerah lainnya

---

**END OF BAB 4.2 PEMBAHASAN**
