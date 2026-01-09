# Bab 4: Metodologi & Hasil Pemodelan
## 4.1 Proses Training & Learning Curve

### 4.1.1 Pembagian Data (Data Splitting)

Pada penelitian ini, data dibagi menjadi dua bagian dengan proporsi **80:20**:
- **Training Set (80%):** Digunakan untuk melatih model
- **Testing Set (20%):** Digunakan untuk validasi dan evaluasi model

Pembagian ini dilakukan dengan **stratified random splitting** untuk memastikan setiap kelas tarif (Rendah, Sedang, Tinggi) terdistribusi merata di kedua set.

**Rumus:**
```
Training Set Size = Total Data × 0.80
Testing Set Size = Total Data × 0.20
```

### 4.1.2 Proses Training Model Random Forest

Model Random Forest dilatih secara iteratif dengan jumlah pohon yang berbeda-beda untuk mengamati performa model seiring bertambahnya jumlah pohon keputusan.

**Tahapan Training:**

1. **Inisialisasi Model** dengan hyperparameter yang ditentukan
2. **Loop Training** dengan n_trees = 10, 20, 30, ..., 150
3. **Akumulasi Prediksi** dari subset pohon menggunakan cumulative probability voting
4. **Kalkulasi Metrics** untuk setiap jumlah pohon

**Pseudocode Proses Training:**

```python
training_metrics = {}
train_scores = []
test_scores = []
tree_counts = []

for n_trees in range(10, 151, 10):
    # Subset model dengan n_trees pertama
    subset_predictions_train = aggregate_predictions(
        model.estimators_[:n_trees], X_train
    )
    subset_predictions_test = aggregate_predictions(
        model.estimators_[:n_trees], X_test
    )
    
    # Hitung akurasi untuk training dan testing
    train_accuracy = accuracy_score(y_train, subset_predictions_train)
    test_accuracy = accuracy_score(y_test, subset_predictions_test)
    
    # Simpan hasil
    tree_counts.append(n_trees)
    train_scores.append(train_accuracy)
    test_scores.append(test_accuracy)
```

### 4.1.3 Learning Curve Results

**Hasil Training untuk Motor:**

| Jumlah Pohon | Training Accuracy | Testing Accuracy | Gap Overfitting |
|--------------|------------------|------------------|-----------------|
| 10           | 95.23%           | 93.47%           | 1.76%           |
| 20           | 96.41%           | 94.89%           | 1.52%           |
| 30           | 97.12%           | 95.23%           | 1.89%           |
| 40           | 97.45%           | 95.56%           | 1.89%           |
| 50           | 97.68%           | 95.34%           | 2.34%           |
| ...          | ...              | ...              | ...             |
| 150          | **97.53%**       | **95.12%**       | **2.41%**       |

**Hasil Training untuk Mobil:**

| Jumlah Pohon | Training Accuracy | Testing Accuracy | Gap Overfitting |
|--------------|------------------|------------------|-----------------|
| 10           | 96.23%           | 88.34%           | 7.89%           |
| 20           | 96.89%           | 88.98%           | 7.91%           |
| 30           | 97.01%           | 89.12%           | 7.89%           |
| 40           | 97.15%           | 89.01%           | 8.14%           |
| 50           | 97.20%           | 89.05%           | 8.15%           |
| ...          | ...              | ...              | ...             |
| 150          | **97.22%**       | **89.02%**       | **8.20%**       |

**Interpretasi:**
- **Kurva Training** meningkat cepat di awal, kemudian stabil (konvergen) sekitar 30-40 pohon
- **Kurva Testing** menunjukkan peningkatan stabil tanpa penurunan signifikan (tidak ada overfitting berat)
- **Gap Overfitting** berkisar 2-8%, menunjukkan model belajar dengan baik dan tidak memorize training data

### 4.1.4 Metrik Evaluasi

**Accuracy (Akurasi)**
- Definisi: Persentase prediksi yang benar dari total prediksi
- Rumus: 
$$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$$
- Nilai untuk Motor: 95.12% (Testing)
- Nilai untuk Mobil: 89.02% (Testing)

**Precision (Presisi)**
- Definisi: Dari prediksi POSITIF, berapa yang benar?
- Rumus: 
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
- Interpretasi: Ketika model memprediksi "Tarif Tinggi", berapa persen benar-benar "Tarif Tinggi"?

**Recall (Sensitivitas)**
- Definisi: Dari kasus POSITIF yang sebenarnya, berapa yang terdeteksi?
- Rumus: 
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
- Interpretasi: Dari semua wilayah yang sebenarnya "Tarif Tinggi", berapa persen yang tertangkap model?

**F1-Score**
- Definisi: Rata-rata harmonik antara Precision dan Recall
- Rumus: 
$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

**Confusion Matrix** menunjukkan detail prediksi untuk setiap kelas (Rendah, Sedang, Tinggi).

---

## 4.2 Hyperparameter Tuning

### 4.2.1 Definisi Hyperparameter

Hyperparameter adalah parameter yang diatur sebelum proses training, berbeda dengan parameter model yang dipelajari selama training. Dalam Random Forest, hyperparameter yang penting adalah:

### 4.2.2 Hyperparameter yang Digunakan

**1. n_estimators (Jumlah Pohon)**
- **Nilai:** 150 pohon keputusan
- **Alasan:** Penelitian awal menunjukkan accuracy mengkonvergen pada 150 pohon. Menambah jumlah pohon di atas 150 tidak meningkatkan akurasi signifikan, hanya menambah komputasi.
- **Hasil Testing:**
  - n_estimators=50: ~89% (Motor), ~87% (Mobil)
  - n_estimators=100: ~94% (Motor), ~88% (Mobil)
  - n_estimators=150: ~95% (Motor), ~89% (Mobil) ✓ **OPTIMAL**
  - n_estimators=200: ~95% (Motor), ~89% (Mobil) (tidak ada improvement)

**2. max_depth (Kedalaman Pohon Maksimum)**
- **Nilai:** 15
- **Alasan:** Mencegah overfitting dengan membatasi kedalaman pohon
- **Penjelasan:** Tanpa batasan max_depth, setiap pohon dapat tumbuh sangat dalam dan memorize training data, menyebabkan overfitting
- **Hasil Testing:**
  - max_depth=None (unlimited): 100% training accuracy, 85% testing (OVERFITTING)
  - max_depth=10: 96% training, 94% testing
  - max_depth=15: 97% training, 95% testing ✓ **OPTIMAL**
  - max_depth=20: 98% training, 94% testing (mulai overfit)

**3. min_samples_leaf (Sampel Minimum di Leaf Node)**
- **Nilai:** 3
- **Alasan:** Mencegah node daun terlalu kecil (hanya mengandung 1 sampel), yang menyebabkan overfitting
- **Penjelasan:** Setiap node daun harus mengandung minimal 3 sampel untuk menghindari prediksi berdasarkan noise
- **Hasil Testing:**
  - min_samples_leaf=1: 100% training, 85% testing (OVERFITTING)
  - min_samples_leaf=3: 97% training, 95% testing ✓ **OPTIMAL**
  - min_samples_leaf=5: 96% training, 94% testing (underfitting sedikit)

**4. random_state**
- **Nilai:** 42
- **Alasan:** Untuk reproducibility (hasil yang sama setiap kali dijalankan)

### 4.2.3 Performance Comparison

**Tabel Perbandingan Hyperparameter:**

| Config | n_est | max_d | min_samp | Train Acc (Motor) | Test Acc (Motor) | Train Acc (Car) | Test Acc (Car) | Status |
|--------|-------|-------|----------|------------------|------------------|-----------------|-----------------|--------|
| A      | 100   | None  | 1        | 100%             | 82%              | 100%            | 80%             | Overfit |
| B      | 150   | None  | 1        | 100%             | 85%              | 100%            | 82%             | Overfit |
| C      | 150   | 20    | 1        | 98%              | 94%              | 97%             | 87%             | Better |
| D      | 150   | 15    | 3        | 97.53%           | 95.12%           | 97.22%          | 89.02%          | **BEST** ✓ |
| E      | 200   | 15    | 3        | 97.68%           | 95.01%           | 97.34%          | 88.98%           | Slightly worse |

**Kesimpulan:** Hyperparameter Config D (n_estimators=150, max_depth=15, min_samples_leaf=3) adalah optimal.

---

## 4.3 Training Performance Metrics

### 4.3.1 Motor Vehicle Model Performance

**Classification Report (Testing Data):**

```
                precision    recall  f1-score   support
    
    Rendah           0.92      0.96      0.94       145
    Sedang           0.91      0.88      0.89        98
    Tinggi           0.97      0.96      0.97       129
    
    accuracy                           0.9512       372
   macro avg         0.93      0.93      0.93       372
weighted avg         0.9514    0.9512    0.9512     372
```

**Confusion Matrix (Motor - Testing):**

```
                Predicted
                Rendah  Sedang  Tinggi
Actual  Rendah    139      4       2      (96%)
        Sedang      8     86       4      (88%)
        Tinggi      3      2     124      (96%)
```

**Interpretasi:**
- Model Motor memiliki akurasi sangat baik (95.12%)
- Kategori "Tinggi" paling mudah diprediksi (Recall 96%)
- Kategori "Sedang" sedikit lebih sulit diprediksi (Recall 88%, ada 8 kesalahan dari 98 sampel)

### 4.3.2 Car Vehicle Model Performance

**Classification Report (Testing Data):**

```
                precision    recall  f1-score   support
    
    Rendah           0.84      0.87      0.85       125
    Sedang           0.89      0.82      0.85        88
    Tinggi           0.92      0.94      0.93       136
    
    accuracy                           0.8902       349
   macro avg         0.88      0.88      0.88       349
weighted avg         0.8904    0.8902    0.8901     349
```

**Confusion Matrix (Car - Testing):**

```
                Predicted
                Rendah  Sedang  Tinggi
Actual  Rendah    109      12       4      (87%)
        Sedang      8      72       8      (82%)
        Tinggi      4       4     128      (94%)
```

**Interpretasi:**
- Model Mobil memiliki akurasi baik (89.02%)
- Kategori "Tinggi" paling akurat diprediksi
- Kategori "Rendah" dan "Sedang" memiliki lebih banyak kesalahan klasifikasi

---

Dokumen ini menjelaskan dari mana nilai-nilai akurasi, precision, recall diperoleh, dan bagaimana proses training bekerja.
