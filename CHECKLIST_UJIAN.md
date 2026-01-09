# ✅ CHECKLIST LENGKAP PERSIAPAN UJIAN & BIMBINGAN

---

## 📋 PHASE 1: PEMAHAMAN KONSEP DASAR

### Accuracy, Precision, Recall, F1-Score
- [ ] Paham perbedaan 4 metric ini
- [ ] Bisa jelaskan setiap metric dengan contoh
- [ ] Hafal nilai motor (95.12%) dan mobil (89.02%)
- [ ] Bisa hitung secara manual dari confusion matrix
- **Dokumentasi:** BAB_4_TRAINING_LEARNING_CURVE.md §4.1.4

### Data Split 80:20
- [ ] Paham kenapa 80:20 (training:testing)
- [ ] Paham stratified random split
- [ ] Bisa jelaskan dari mana nilai accuracy diperoleh (testing set)
- [ ] Tahu jumlah sampel training & testing untuk motor/mobil
- **Dokumentasi:** BAB_4_TRAINING_LEARNING_CURVE.md §4.1.1

### Learning Curve
- [ ] Bisa trace learning curve untuk motor dan mobil
- [ ] Paham kurva naik cepat, tapi converge di 40 pohon
- [ ] Tahu gap overfitting motor 2.41%, mobil 8.20%
- [ ] Bisa interpretasi: tidak ada overfitting berat
- **Dokumentasi:** BAB_4_TRAINING_LEARNING_CURVE.md §4.1.3

---

## 🤖 PHASE 2: RANDOM FOREST & HYPERPARAMETER

### Hyperparameter Final
- [ ] Hafal 3 hyperparameter: **n_estimators=150**, **max_depth=15**, **min_samples_leaf=3**
- [ ] Paham kenapa 150 pohon (convergence)
- [ ] Paham kenapa max_depth=15 (prevent overfitting)
- [ ] Paham kenapa min_samples_leaf=3 (avoid noise)
- **Dokumentasi:** BAB_4_TRAINING_LEARNING_CURVE.md §4.2

### Hyperparameter Tuning Process
- [ ] Bisa jelaskan testing berbagai kombinasi
- [ ] Paham comparison table (Config A-E)
- [ ] Tahu Config D adalah optimal
- [ ] Bisa compare dengan alternatives (unlimited depth = overfitting)

### Random Forest Basics
- [ ] Paham 150 pohon voting untuk prediksi
- [ ] Paham subset sampling dan feature randomness
- [ ] Paham aggregation: majority voting
- [ ] Paham OOB (Out-of-Bag) score concept

---

## 📊 PHASE 3: FEATURE IMPORTANCE & INFORMATION GAIN

### Feature Importance
- [ ] Paham: importance = ukuran kontribusi fitur
- [ ] Hafal rumus: `Importance(Xi) = Σ(weight × gini_decrease) / total_weight`
- [ ] Hafal top fitur:
  - Motor: Jumlah_Motor_Weekday **28.5%**
  - Mobil: Jumlah_Mobil_Weekday **31.2%**
- [ ] Bisa interpretasi: Volume weekday paling penting
- [ ] Paham gini-based vs permutation importance
- **Dokumentasi:** BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md §4.4

### Entropy & Information Gain
- [ ] Paham entropy = measure of disorder (0-1)
- [ ] Hafal rumus: `H(S) = -Σ(pi × log2(pi))`
- [ ] Paham information gain = entropy decrease
- [ ] Hafal rumus: `IG = H(parent) - Σ(|Sv|/|S| × H(Sv))`
- [ ] Bisa hitung manual entropy untuk contoh sederhana
- [ ] Bisa hitung manual IG dengan step-by-step
- [ ] Contoh calculation:
  - H(root) = 1.571 bits
  - After split: IG = 0.395 bits
- **Dokumentasi:** BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md §4.5

### Gini vs Entropy
- [ ] Paham Gini: `1 - Σ(pi²)` untuk splitting
- [ ] Paham Entropy: `-Σ(pi × log2(pi))` alternative
- [ ] Paham keduanya measure impurity
- [ ] Tahu Random Forest pakai Gini (default)

---

## 🌳 PHASE 4: DECISION TREE STRUCTURE & INTERPRETATION

### Node Anatomy
- [ ] Hafal komponen node:
  - Split criteria (Feature ≤ Threshold)
  - Entropy/Gini
  - Samples (jumlah sampel)
  - Value (class distribution)
  - Class (predicted class)
- [ ] Paham interpretasi setiap komponen
- **Dokumentasi:** BAB_4_DECISION_TREE_STRUCTURE.md §4.6

### Decision Path Tracing
- [ ] Bisa trace path untuk motor dengan contoh konkret
- [ ] Bisa trace path untuk mobil dengan contoh berbeda
- [ ] Paham logic: `if feature ≤ threshold: go LEFT else go RIGHT`
- [ ] Bisa hitung confidence di leaf node: `max_class / total_samples`
- [ ] Contoh:
  - Motor: 250 ≤ 280? YES → 0 ≤ 0.5? YES → RENDAH (66%)
  - Mobil: 450 ≤ 380? NO → 1 ≤ 0.5? NO → 520 ≤ 510? NO → TINGGI (89%)
- **Dokumentasi:** BAB_4_DECISION_TREE_STRUCTURE.md §4.7

### Tree Characteristics
- [ ] Paham depth ≤ 15 (constraint)
- [ ] Paham feature distribution (Motor: 45% untuk motor_weekday)
- [ ] Paham threshold selection (maximize IG)
- [ ] Paham leaf node confidence estimation
- [ ] Paham aggregate dari 150 trees

### Confusion Matrix Reading
- [ ] Bisa baca confusion matrix motor
- [ ] Bisa baca confusion matrix mobil
- [ ] Tahu diagonal = correct predictions
- [ ] Bisa hitung accuracy dari matrix
- [ ] Bisa identify mana kelas paling sulit (Sedang untuk motor)
- **Dokumentasi:** BAB_4_TRAINING_LEARNING_CURVE.md §4.3

---

## 💰 PHASE 5: TARIF IDEAL & IMPLEMENTASI

### Tarif Ideal Concept
- [ ] Paham perbedaan tarif ideal vs tarif flat
- [ ] Paham mapping: kategori prediksi → tarif dasar
- [ ] Hafal mapping motor:
  - RENDAH: Rp 1.000-2.000/jam
  - SEDANG: Rp 2.500-4.000/jam
  - TINGGI: Rp 5.000-8.000/jam
- [ ] Hafal mapping mobil (lebih tinggi dari motor)
- **Dokumentasi:** BAB_5_TARIF_IDEAL_ADAPTIF.md §5.2

### Revenue Calculation
- [ ] Bisa hitung revenue: `Tarif × Volume × Durasi × Days`
- [ ] Paham demand elasticity (volume turun jika tarif naik)
- [ ] Contoh motor TINGGI:
  - Current: Rp 2.000 × 500 × 3 × 26 = Rp 78 juta
  - Proposed: Rp 4.500 × 400 × 3 × 26 = Rp 140.4 juta
  - Improvement: +80%
- [ ] Paham optimal occupancy 80-85%
- **Dokumentasi:** BAB_5_TARIF_IDEAL_ADAPTIF.md §5.3

### Implementation Roadmap
- [ ] Paham 3 phase:
  - Phase 1: Pilot di kategori TINGGI (1-3 bulan)
  - Phase 2: Expand ke SEDANG (3-6 bulan)
  - Phase 3: Full implementation (6+ bulan)
- [ ] Paham KPI monitoring: revenue, occupancy, satisfaction
- [ ] Paham review cycle: setiap 3 bulan
- **Dokumentasi:** BAB_5_TARIF_IDEAL_ADAPTIF.md §5.5

### Case Studies
- [ ] Paham case study kategori RENDAH:
  - Saat ini underutilized
  - Tarif turun → lebih banyak pengunjung
  - Win-win
- [ ] Paham case study kategori TINGGI:
  - Saat ini oversupply (98% occupancy)
  - Tarif naik → terkontrol
  - Revenue meningkat, akses lebih mudah
- **Dokumentasi:** BAB_5_TARIF_IDEAL_ADAPTIF.md §5.7

---

## 📚 PHASE 6: BATASAN PENELITIAN

### 10 Batasan
- [ ] Hafal minimum 5 batasan utama:
  1. Geografis: hanya Banyumas
  2. Jenis kendaraan: motor & mobil
  3. Periode: 2023-2024
  4. Fitur: hanya dari dataset
  5. Akurasi: 89-95%, bisa berubah
- [ ] Paham implikasi: apa yang berlaku, apa tidak
- [ ] Paham: model TIDAK bisa langsung apply ke daerah lain
- **Dokumentasi:** BATASAN_MASALAH.md

---

## 🎤 PHASE 7: READY FOR PRESENTATION

### Jawaban Siap Untuk 8 Pertanyaan Utama
- [ ] "Ada gak data train nya, grafik train nya?"
  - **Jawab:** Ya, learning curve motor 95%, mobil 89%, kurva stabil di 40 pohon
- [ ] "Dari mana accuracy/precision/recall?"
  - **Jawab:** Dari testing set (20%), confusion matrix menunjukkan detail
- [ ] "Berapa hyperparameter? Hasilnya berapa?"
  - **Jawab:** n=150, depth=15, leaf=3. Hasil motor 95%, mobil 89%
- [ ] "Feature importance itu apa?"
  - **Jawab:** Ukuran kontribusi fitur, top: motor_weekday 28.5%, mobil_weekday 31.2%
- [ ] "Information gain untuk apa?"
  - **Jawab:** Measure entropy decrease, algorithm pilih split terbaik based on IG
- [ ] "Pohon gimana cara membacanya?"
  - **Jawab:** Trace dari root follow split criteria sampai leaf, bisa jelaskan contoh
- [ ] "Tarif ideal gimana?"
  - **Jawab:** Map kategori ke tarif, expect +50-80% revenue, implement bertahap
- [ ] "Batasan penelitian apa?"
  - **Jawab:** 10 batasan, terutama geografis (hanya Banyumas), tidak generalize

---

## 🖥️ PHASE 8: STREAMLIT DASHBOARD FAMILIARIZATION

- [ ] Bisa operate Streamlit di http://localhost:8501
- [ ] Tahu masing-masing tab:
  - [ ] Motor Model → Lihat confusion matrix, feature importance
  - [ ] Car Model → Hasil untuk mobil
  - [ ] Training Graphs → Learning curve visualization
  - [ ] Tree Visualization → Sample tree structure
  - [ ] Tariff Recommendations → Hasil mapping ke tarif
- [ ] Bisa screenshot untuk laporan
- [ ] Bisa show ke dosen saat bimbingan
- [ ] Tahu data flow: raw → processing → model → output

---

## 📝 PHASE 9: WRITING PREPARATION

### Bahan untuk Laporan
- [ ] Bab 1 (Pendahuluan):
  - [ ] Copy-paste BATASAN_MASALAH.md untuk §1.5
  
- [ ] Bab 4 (Metodologi & Hasil):
  - [ ] Data split 80:20 → BAB_4_TRAINING_LEARNING_CURVE.md §4.1.1
  - [ ] Learning curve & metrics → BAB_4_TRAINING_LEARNING_CURVE.md §4.1.3-4.1.4
  - [ ] Hyperparameter tuning → BAB_4_TRAINING_LEARNING_CURVE.md §4.2
  - [ ] Confusion matrices → BAB_4_TRAINING_LEARNING_CURVE.md §4.3
  - [ ] Feature importance → BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md §4.4
  - [ ] Entropy/IG → BAB_4_FEATURE_IMPORTANCE_INFORMATION_GAIN.md §4.5
  - [ ] Tree structure → BAB_4_DECISION_TREE_STRUCTURE.md §4.6-4.7
  
- [ ] Bab 5 (Implementasi & Pembahasan):
  - [ ] Tarif ideal methodology → BAB_5_TARIF_IDEAL_ADAPTIF.md §5.2-5.4
  - [ ] Revenue calculation → BAB_5_TARIF_IDEAL_ADAPTIF.md §5.3
  - [ ] Implementation roadmap → BAB_5_TARIF_IDEAL_ADAPTIF.md §5.5

---

## 🏆 PHASE 10: FINAL CHECKS

### Sebelum Bimbingan
- [ ] Sudah baca semua dokumentasi utama
- [ ] Sudah paham setiap rumus dan bisa jelaskan
- [ ] Sudah hitung manual 1-2 contoh entropy/IG
- [ ] Sudah trace 2 contoh decision path (motor & mobil)
- [ ] Sudah hafal semua nilai penting (95%, 89%, 150, 15, 3)
- [ ] Sudah siap jawab 8 pertanyaan utama dengan detail
- [ ] Sudah lihat Streamlit dashboard, bisa show feature penting
- [ ] Sudah print/save dokumentasi untuk bawa ke bimbingan

### Sebelum Ujian Komprehensif
- [ ] Semua di atas PLUS:
- [ ] Sudah tahu jawaban untuk masing-masing pertanyaan dengan percaya diri
- [ ] Sudah practice presentasi minimal 1 kali
- [ ] Sudah siap untuk pertanyaan follow-up (dosen mungkin explore lebih dalam)
- [ ] Hafal rumus-rumus key (lihat QUICK_REFERENCE_RUMUS.md)
- [ ] Bisa visualisasi setiap konsep (learning curve, tree, confusion matrix)
- [ ] Bisa jelaskan trade-off & limitations dengan jujur

---

## 📊 PROGRESS TRACKER

Copy-paste dan isi tracking Anda:

```
PHASE 1: Accuracy/Precision/Recall        ___/3 tasks done
PHASE 2: Random Forest & Hyperparameter   ___/3 tasks done
PHASE 3: Feature Importance & IG          ___/4 tasks done
PHASE 4: Decision Tree Structure          ___/5 tasks done
PHASE 5: Tarif Ideal & Implementasi       ___/3 tasks done
PHASE 6: Batasan Penelitian               ___/3 tasks done
PHASE 7: Ready for Presentation           ___/8 jawaban ready
PHASE 8: Streamlit Familiarization        ___/5 tasks done
PHASE 9: Writing Preparation              ___/3 bab ready
PHASE 10: Final Checks                    ___/8 tasks done

TOTAL: ___/45 TASKS DONE

Siap untuk:
- [ ] Bimbingan (min 30/45 tasks)
- [ ] Ujian Komprehensif (min 40/45 tasks)
- [ ] Defense (min 43/45 tasks)
```

---

## 🎯 TIPS AKHIR

### Saat Bimbingan/Ujian:

1. **Jangan hafal teks, pahami konsep** - Dosen bisa mendeteksi memorization
2. **Jika ditanya yang tidak tahu, bilang dengan jujur** - "Saya belum detail di bagian itu, boleh saya lihat dokumentasi?" lebih baik dari nebak
3. **Gunakan contoh konkret** - Jangan hanya teori, selalu kasih contoh angka
4. **Pahami trade-off** - Model 95% vs 89%, kenapa? Paham elasticity demand dll
5. **Tunjukkan Streamlit** - Visual yang bagus bisa membantu explain
6. **Validasi dengan logika** - Penjelasan harus masuk akal bisnis (Tarif tinggi → occupancy turun wajar)

### Jika Dosen Tanya Tambahan:

- "Kalau hyperparameter berubah, apa yang akan happen?" 
  - Jawab: "Jika depth unlimited akan overfit, jika leaf=1 juga, ada sensitivity analysis di dokumentasi"
  
- "Gimana kalau data tahun depan berbeda pola?"
  - Jawab: "Model harus di-retrain dengan data baru, atau pakai sliding window retraining"
  
- "Apakah model sudah optimal?"
  - Jawab: "Gap overfitting kecil (2.4%), accuracy baik, bisa explore ensemble methods lain di future work"

---

**Status:** 
- [ ] BELUM MULAI
- [ ] SEDANG PROGRESS
- [ ] PHASE XX DONE
- [ ] ✅ SIAP BIMBINGAN
- [ ] ✅ SIAP UJIAN
- [ ] ✅ SIAP DEFENSE

**Last Check:** 24 Desember 2025

---

**💪 You got this! Semua dokumentasi sudah lengkap. Tinggal execute dengan percaya diri!**
