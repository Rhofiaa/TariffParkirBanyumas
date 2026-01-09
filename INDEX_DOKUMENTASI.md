# DOKUMENTASI LAPORAN SKRIPSI
## Sistem Prediksi Tarif Parkir Progresif Menggunakan Random Forest

Direktori ini berisi dokumentasi lengkap untuk mendukung laporan skripsi dan membantu dalam bimbingan dengan dosen.

---

## 📋 DAFTAR DOKUMEN

### 1. **RINGKASAN_JAWABAN_DOSEN.md** ⭐ START HERE
   - **Tujuan:** Ringkasan jawaban untuk semua pertanyaan dosen pembimbing
   - **Isi:**
     - Jawaban langsung untuk 8 pertanyaan utama
     - Penjelasan singkat dengan referensi dokumentasi
     - Checklist persiapan ujian/bimbingan
   - **Untuk siapa:** Persiapan bimbingan/ujian, quick reference

### 2. **BATASAN_MASALAH.md**
   - **Tujuan:** Mendefinisikan scope penelitian (Problem Limitations)
   - **Isi:**
     - 10 batasan penelitian terstruktur
     - Implikasi batasan untuk validitas hasil
     - Kejelasan apa yang berlaku vs tidak berlaku
   - **Untuk siapa:** Bab 1 (Pendahuluan) laporan
   - **Referensi:** Struktur sesuai standar penelitian akademik

### 3. **BAB_4_TRAINING_LEARNING_CURVE.md**
   - **Tujuan:** Dokumentasi proses training dan hasil pembelajaran model
   - **Isi:**
     - Penjelasan 80:20 data split
     - Proses training iteratif (10-150 pohon)
     - Learning curve results (motor 95.12%, mobil 89.02%)
     - Definisi dan rumus Accuracy, Precision, Recall, F1-Score
     - Hyperparameter tuning methodology & results
     - Confusion matrices untuk motor dan mobil
   - **Untuk siapa:** Bab 4 (Metodologi & Hasil)
   - **Jawab pertanyaan:** "Dari mana nilai accuracy/precision/recall? Ada gak grafik training?"

### 4. **BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md**
   - **Tujuan:** Penjelasan Feature Importance dan Information Gain
   - **Isi:**
     - Definisi feature importance (seberapa penting fitur)
     - Rumus Gini-based importance
     - Contoh perhitungan manual 1 sampel
     - Hasil feature importance untuk motor & mobil
     - Interpretasi: fitur mana paling berpengaruh
     - Konsep Entropy dan Information Gain
     - Rumus dan contoh perhitungan IG dengan derivasi lengkap
   - **Untuk siapa:** Bab 4 (Metodologi), untuk menjelaskan proses keputusan tree
   - **Jawab pertanyaan:** "Feature importance itu apa? Information gain untuk apa? Rumusnya gimana?"

### 5. **BAB_4_DECISION_TREE_STRUCTURE.md**
   - **Tujuan:** Penjelasan anatomi dan cara membaca decision tree
   - **Isi:**
     - Struktur pohon (root, internal nodes, leaf nodes)
     - Komponen setiap node (split criteria, entropy, samples, value, class)
     - Cara membaca dan interpretasi node
     - Decision path tracing (2 contoh: motor dan mobil)
     - Node confidence calculation
     - Karakteristik tree dalam Random Forest (depth, feature distribution)
     - Estimasi akurasi dari tree structure
   - **Untuk siapa:** Bab 4 (Hasil & Pembahasan), visualisasi tree di laporan
   - **Jawab pertanyaan:** "Pohon tree nya gimana cara membacanya? Decision path apa itu?"

### 6. **BAB_5_TARIF_IDEAL_ADAPTIF.md**
   - **Tujuan:** Penjelasan cara membangun tarif ideal dan strategi implementasi
   - **Isi:**
     - Konsep tarif ideal vs tarif adaptif
     - Metodologi pembangunan tarif berbasis kategori model
     - Rumus perhitungan tarif (3 methods)
     - Mapping: kategori prediksi → tarif ideal (dengan contoh angka)
     - Revenue estimation dan improvement calculation
     - Proses validasi dengan data historis
     - Sensitivity analysis
     - Implementation roadmap (Phase 1, 2, 3)
     - KPI monitoring framework
     - 2 case studies: kategori Rendah dan Tinggi
   - **Untuk siapa:** Bab 5 (Implementasi & Pembahasan)
   - **Jawab pertanyaan:** "Gimana cara membangun tarif ideal? Bagaimana hasil diperoleh?"

---

## 🎯 MAPPING PERTANYAAN DOSEN → DOKUMENTASI

| Pertanyaan Dosen | Jawaban Singkat | Dokumentasi |
|---|---|---|
| "Ada gak data train nya, grafik train nya?" | Ya, learning curve motor 95.12%, mobil 89.02% | BAB_4_TRAINING_LEARNING_CURVE.md §4.1.3 |
| "Dari mana dapat accuracy/precision/recall?" | Dari confusion matrix di testing set (80/20 split) | BAB_4_TRAINING_LEARNING_CURVE.md §4.1.4 |
| "Hyperparameter berapa? Hasilnya berapa?" | n_est=150, max_d=15, min_samp=3 → hasil di atas | BAB_4_TRAINING_LEARNING_CURVE.md §4.2 |
| "Feature importance itu apa? Rumusnya?" | Importance = Gini decrease average di semua tree | BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md §4.4 |
| "Information gain untuk apa? Rumusnya?" | IG = penurunan entropy setelah split, rumus detail | BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md §4.5 |
| "Pohon tree gimana cara membacanya?" | Node punya split criteria, ikuti True→Left/False→Right | BAB_4_DECISION_TREE_STRUCTURE.md §4.6-4.7 |
| "Gimana cara bangun tarif ideal?" | Map kategori (Rendah/Sedang/Tinggi) ke tarif dasar | BAB_5_TARIF_IDEAL_ADAPTIF.md §5.2-5.3 |
| "Batasan penelitian apa aja?" | 10 batasan terstruktur: geografis, jenis kendaraan, dll | BATASAN_MASALAH.md |

---

## 📊 STRUKTUR LOGIS UNTUK LAPORAN

Urutan membaca/menulis laporan yang disarankan:

```
BAB 1: Pendahuluan
├─ BATASAN_MASALAH.md (sebagai bahan untuk menulis §1.5)

BAB 4: Metodologi & Hasil
├─ BAB_4_TRAINING_LEARNING_CURVE.md (data split, training process, metrics)
├─ BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md (how model learns)
├─ BAB_4_DECISION_TREE_STRUCTURE.md (tree visualization & interpretation)

BAB 5: Implementasi & Pembahasan
├─ BAB_5_TARIF_IDEAL_ADAPTIF.md (how to use model results)
```

---

## 🔑 KEY METRICS & RESULTS RINGKAS

### Model Performance (Testing Data):

**Motor Model:**
- Accuracy: 95.12%
- Training curve converges at 40 trees
- Feature importance: Motor_Weekday 28.5%

**Car Model:**
- Accuracy: 89.02%
- Training curve converges at 40 trees
- Feature importance: Car_Weekday 31.2%

### Hyperparameter Optimal:
- n_estimators: 150
- max_depth: 15
- min_samples_leaf: 3

### Tarif Ideal Mapping (Motor):
- Rendah: Rp 1.000-2.000/jam → Low volume areas
- Sedang: Rp 2.500-4.000/jam → Medium volume areas
- Tinggi: Rp 5.000-8.000/jam → High volume areas

---

## ✅ CHECKLIST PERSIAPAN UJIAN

- [ ] Baca RINGKASAN_JAWABAN_DOSEN.md sebagai overview
- [ ] Pahami learning curve (motor 95%, mobil 89%)
- [ ] Bisa jelaskan dari mana accuracy diperoleh
- [ ] Hafal hyperparameter: 150, 15, 3
- [ ] Tahu feature importance top 3 untuk tiap model
- [ ] Bisa trace decision path (contoh motor & mobil)
- [ ] Pahami mapping kategori → tarif ideal
- [ ] Siap hitung manual 1 contoh information gain
- [ ] Fahami implementasi bertahap (Phase 1, 2, 3)
- [ ] Review case studies di BAB_5

---

## 🖥️ DASHBOARD STREAMLIT

Visualisasi interaktif tersedia di: **http://localhost:8501**

**Tabs yang relevan:**

| Tab | Gunakan untuk | Dokumentasi terkait |
|---|---|---|
| Motor Model | Lihat confusion matrix, feature importance | BAB_4_TRAINING_LEARNING_CURVE.md |
| Car Model | Lihat hasil untuk mobil | BAB_4_TRAINING_LEARNING_CURVE.md |
| Training Graphs | Learning curve visualization | BAB_4_TRAINING_LEARNING_CURVE.md §4.1.3 |
| Tree Visualization | Lihat sample tree structure | BAB_4_DECISION_TREE_STRUCTURE.md |
| Tariff Recommendations | Lihat hasil mapping ke tarif | BAB_5_TARIF_IDEAL_ADAPTIF.md |

---

## 📝 CATATAN PENTING

1. **Data Split:** Pastikan jelaskan 80:20 split dengan jelas saat presentasi
2. **Konvergensi:** Model converges pada 40 pohon, tapi pakai 150 untuk stability
3. **Hyperparameter:** Semua parameter sudah di-tune dan di-compare dengan alternatives
4. **Feature Importance:** Bisa jelaskan dengan contoh di dashboard
5. **Decision Tree:** Punya sample tree visualization di dashboard (screenshot bisa pakai di laporan)
6. **Tarif Ideal:** Bukan prediksi nilai rupiah, tapi kategori potensi tarif

---

## 📚 REFERENSI RUMUS

Untuk quick lookup:

- **Accuracy:** `(TP+TN) / Total`
- **Precision:** `TP / (TP+FP)`
- **Recall:** `TP / (TP+FN)`
- **Entropy:** `-Σ(p_i * log₂(p_i))`
- **Gini:** `1 - Σ(p_i²)`
- **Information Gain:** `H(parent) - Σ(|child|/|parent| * H(child))`
- **Feature Importance:** `Σ(weight * gini_decrease) / total_weight`

Detail penuh ada di masing-masing dokumen.

---

**Last Updated:** 24 Desember 2025
**Status:** ✅ LENGKAP - Semua pertanyaan dosen sudah dijawab
**Siap untuk:** Bimbingan, Ujian Komprehensif, Penyelesaian Laporan
