# 🎯 ONE-PAGE STUDY GUIDE (Print ini & bawa ke bimbingan!)

---

## 8 PERTANYAAN DOSEN & JAWABAN SINGKAT

### ❓ 1. "Ada gak data train nya? Grafik train nya?"
**JAWAB:** 
- ✅ Ya ada! Learning curve tersedia di Streamlit tab "Training Graphs"
- **Data split:** 80% training, 20% testing
- **Motor curve:** 10 trees→95%, 40 trees→95.5%, 150 trees→95.12% (stabil ✓)
- **Mobil curve:** 10 trees→88%, 40 trees→89%, 150 trees→89.02% (converge ✓)
- **NO OVERFITTING:** Gap motor 2.41%, mobil 8.20% (kecil ✓)

---

### ❓ 2. "Dari mana dapat nilai accuracy/precision/recall?"
**JAWAB:**
- Dari **testing set** (20% data yang TIDAK pernah di-training)
- Proses: Model predict → bandingkan dengan actual → hitung metrics
- **Formula:**
  - Accuracy = (TP+TN) / Total
  - Precision = TP / (TP+FP)  
  - Recall = TP / (TP+FN)
- **Contoh:** Motor accuracy 95.12% = 354 benar dari 372 total

---

### ❓ 3. "Berapa hyperparameternya? Hasilnya berapa?"
**JAWAB:**
- **Final hyperparameter:**
  - `n_estimators = 150` pohon ← testing 50→94%, 100→95%, 150→95.12% (STOP)
  - `max_depth = 15` ← prevent overfit (unlimited=100% train/85% test, 15=97/95%)
  - `min_samples_leaf = 3` ← avoid noise (1=overfit, 3=optimal)
  - `random_state = 42` ← reproducibility
- **Hasil:**
  - Motor: 95.12% test, 97.53% train, gap 2.41%
  - Mobil: 89.02% test, 97.22% train, gap 8.20%

---

### ❓ 4. "Feature importance itu apa? Rumusnya?"
**JAWAB:**
- **Definisi:** Ukuran kontribusi fitur dalam keputusan model
- **Rumus:** `Importance(Xi) = Σ(weight × gini_decrease) / total_weight`
- **Hasil Motor:**
  1. Jumlah_Motor_Weekday: **28.5%** ← MOST IMPORTANT
  2. Jumlah_Mobil_Weekday: **19.5%**
  3. Jam_Puncak_Pagi: **15.5%**
- **Hasil Mobil:**
  1. Jumlah_Mobil_Weekday: **31.2%** ← MOST IMPORTANT
  2. Jumlah_Motor_Weekday: **22.8%**
  3. Jam_Puncak_Siang: **16.7%**
- **Interpretasi:** Volume weekday adalah faktor utama → decide tarif

---

### ❓ 5. "Information gain untuk apa? Rumusnya gimana?"
**JAWAB:**
- **Definisi:** Ukuran penurunan entropy (uncertainty) setelah split
- **Rumus:** `IG = H(parent) - Σ(|Sv|/|S| × H(Sv))`
- **Entropy rumus:** `H(S) = -Σ(pi × log2(pi))` (0=pure, 1=mixed)
- **Contoh konkret (10 samples: 3 Rendah, 3 Sedang, 4 Tinggi):**
  - H(root) = 1.571 bits
  - Setelah split: H(left)=1.421, H(right)=0.811
  - IG = 1.571 - (0.6×1.421 + 0.4×0.811) = **0.395 bits** ← significant!
- **Gunaan:** Algoritma pilih split dengan IG terbesar → optimal tree

---

### ❓ 6. "Pohon tree gimana cara membacanya?"
**JAWAB:**
- **Node components:** 
  - Split criteria (Feature ≤ Threshold)
  - Entropy/samples
  - Value (class distribution) & class (majority)
- **Cara trace:** Mulai root, follow split sampai leaf
  - If feature ≤ threshold: go LEFT | else: go RIGHT
- **Contoh Motor (Trace Path):**
  ```
  1. Jumlah_Motor_Weekday ≤ 280.5?  250 ≤ 280.5? YES → LEFT
  2. Jam_Puncak_Pagi ≤ 0.5?         0 ≤ 0.5? YES → LEFT
  3. LEAF: value=[140,50,20] → RENDAH (66% confidence)
  ```
- **Contoh Mobil (Trace Path):**
  ```
  1. Jumlah_Mobil_Weekday ≤ 380.5?  450 ≤ 380? NO → RIGHT
  2. Jam_Puncak_Siang ≤ 0.5?        1 ≤ 0.5? NO → RIGHT
  3. Jumlah_Motor_Weekday ≤ 510?    520 ≤ 510? NO → RIGHT
  4. LEAF: value=[5,15,165] → TINGGI (89% confidence)
  ```

---

### ❓ 7. "Gimana cara membangun tarif ideal?"
**JAWAB:**
- **Process:** Kategori prediksi → mapping ke tarif → estimasi revenue
- **Mapping Motor:**
  - RENDAH: Rp 1.000-2.000/jam ← low volume, tepi
  - SEDANG: Rp 2.500-4.000/jam ← medium volume
  - TINGGI: Rp 5.000-8.000/jam ← high volume, central ← UTAMA
- **Revenue contoh (Motor TINGGI):**
  - Current: Rp 2.000 × 500/hari × 3jam × 26hari = Rp 78 juta
  - Proposed: Rp 4.500 × 400 × 3 × 26 = Rp 140.4 juta
  - **Improvement: +80%** (dengan elasticity 20%)
- **Implementation:** Phase 1 (pilot TINGGI 1-3 bulan) → Phase 2 (SEDANG) → Phase 3 (ALL)

---

### ❓ 8. "Batasan penelitian apa?"
**JAWAB:**
- **10 Batasan utama:**
  1. **Geografis:** Hanya Banyumas (tidak generalize ke daerah lain)
  2. **Jenis kendaraan:** Motor & mobil saja (tidak truck, bus, dll)
  3. **Periode:** 2023-2024 data historis
  4. **Fitur:** Hanya variabel yang ada di dataset
  5. **Fenomena:** Probabilistik (bukan deterministic, ada error margin)
  6. **Output:** Kategori tarif (bukan rupiah absolut)
  7. **Model:** Random Forest classifier dengan parameter fixed
  8. **Akurasi:** 89-95% (bisa berubah dengan data baru)
  9. **Asumsi:** Data akurat, pola berkelanjutan
  10. **Aplikasi:** Sesuai untuk Banyumas, perlu tuning untuk daerah lain

---

## 📊 KEY METRICS YANG HARUS HAFAL

| Metric | Value | Status |
|---|---|---|
| **Motor Accuracy** | 95.12% | ✅ EXCELLENT |
| **Mobil Accuracy** | 89.02% | ✅ GOOD |
| **Motor Gap** | 2.41% | ✅ NO OVERFITTING |
| **Mobil Gap** | 8.20% | ✅ ACCEPTABLE |
| **n_estimators** | 150 | ✅ OPTIMAL |
| **max_depth** | 15 | ✅ BALANCED |
| **min_samples_leaf** | 3 | ✅ ROBUST |
| **Converge Point** | 40 trees | ✅ STABLE |
| **Motor Top Feature** | 28.5% (Motor_Weekday) | ✅ CLEAR |
| **Mobil Top Feature** | 31.2% (Mobil_Weekday) | ✅ CLEAR |

---

## 🎯 TIPS SAAT BIMBINGAN/UJIAN

✅ **DO:**
- Jelaskan dengan CONTOH konkret (angka real dari model)
- Tunjukkan Streamlit dashboard untuk visualisasi
- Pahami KENAPA (bukan hanya WHAT)
- Jujur jika tidak tahu → "Let me check dokumentasi"

❌ **DON'T:**
- Jangan hafal tekstual (dosen bakal ketahuan)
- Jangan nebak-nebak kalau tidak tahu
- Jangan panik → semua sudah prepared
- Jangan lupa feature importance meaning

---

## 📱 QUICK FORMULAS (Untuk print & hafal)

```
Accuracy  = (TP+TN) / Total
Precision = TP / (TP+FP)
Recall    = TP / (TP+FN)
F1        = 2 × (P×R) / (P+R)

Entropy   = -Σ(p × log2(p))
Gini      = 1 - Σ(p²)
IG        = H(parent) - Σ(|Sv|/|S| × H(Sv))

Importance = Σ(weight × gini_decrease) / total_weight

Revenue = Tarif × Volume × Durasi × Days
```

---

## 🚀 PERSIAPAN CHECKLIST (Sebelum Bimbingan)

- [ ] Baca file **RINGKASAN_JAWABAN_DOSEN.md** (20 min)
- [ ] Hafal 8 jawaban di atas (30 min)
- [ ] Lihat Streamlit dashboard (10 min) - http://localhost:8501
- [ ] Trace 2 contoh decision path manual (20 min)
- [ ] Hitung 1 contoh Information Gain (10 min)
- [ ] Print file ini untuk reference saat bimbingan (5 min)

**TOTAL: ~1.5 JAM, SIAP UNTUK BIMBINGAN! ✅**

---

## 📚 DOKUMENTASI LENGKAP TERSEDIA DI:

1. **00_MULAI_DARI_SINI.md** ← Ringkasan semua file
2. **RINGKASAN_JAWABAN_DOSEN.md** ← Detail untuk 8 pertanyaan
3. **QUICK_REFERENCE_RUMUS.md** ← Formula quick lookup
4. **BAB_4_TRAINING_LEARNING_CURVE.md** ← Training detail
5. **BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md** ← Feature & IG
6. **BAB_4_DECISION_TREE_STRUCTURE.md** ← Tree anatomy
7. **BAB_5_TARIF_IDEAL_ADAPTIF.md** ← Tarif ideal detail
8. **CHECKLIST_UJIAN.md** ← Full preparation guide
9. **BATASAN_MASALAH.md** ← Research boundaries

---

**Print halaman ini dan bawa ke bimbingan!**  
**Sudah siap! Tinggal execute dengan percaya diri! 💪**
