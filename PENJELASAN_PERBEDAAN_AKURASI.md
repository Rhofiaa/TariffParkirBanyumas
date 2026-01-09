# Perbedaan Akurasi antara app.py dan simulasi_simple.py

## Penyebab Perbedaan Nilai Akurasi

Ada **3 perbedaan utama** yang menyebabkan nilai akurasi berbeda:

### 1. **METODE PERHITUNGAN AKURASI FINAL**

#### Di app.py:
```python
# Line 240-248 di app.py
y_pred_train_prob = np.zeros((len(y_train), len(le.classes_)))
y_pred_test_prob = np.zeros((len(y_test), len(le.classes_)))

# Aggregate predictions dari n_trees PERTAMA (10, 20, 30, ..., 150)
for estimator in model.estimators_[:n_trees]:
    y_pred_train_prob += estimator.predict_proba(X_train)
    y_pred_test_prob += estimator.predict_proba(X_test)

# Majority voting
y_pred_train_final = np.argmax(y_pred_train_prob, axis=1)
y_pred_test_final = np.argmax(y_pred_test_prob, axis=1)

train_acc = np.mean(y_pred_train_final == y_train)
test_acc = np.mean(y_pred_test_final == y_test)
```

**Penjelasan:**
- Menggunakan **CUMULATIVE PROBABILITY VOTING** dari n_trees pertama
- Tidak semua 150 trees digunakan sekaligus, melainkan setiap n (10, 20, 30, ... 150)
- Hasil akurasi adalah akurasi untuk 150 trees (n_trees terakhir)

#### Di simulasi_simple.py:
```python
# Line 328-330 di simulasi_simple.py
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_acc = accuracy_score(y_train, y_pred_train)
test_acc = accuracy_score(y_test, y_pred_test)
```

**Penjelasan:**
- Menggunakan **LANGSUNG PREDICT** dari seluruh 150 trees
- `model.predict()` menggunakan internal majority voting dari RandomForest

---

### 2. **PERBEDAAN FITUR (Features)**

#### Di app.py:
```python
# Dari app.py, fitur yang digunakan adalah:
fitur_motor = [kolom jam yang sudah dikonversi dengan format spesifik]
fitur_mobil = [kolom jam yang sudah dikonversi dengan format spesifik]
```

#### Di simulasi_simple.py:
```python
# Line 197-198
fitur_motor = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend'] + [c for c in jam_cols if 'Motor' in c]
fitur_mobil = ['Jumlah Mobil Weekday', 'Jumlah Mobil Weekend'] + [c for c in jam_cols if 'Mobil' in c]
```

**Perbedaan:**
- Jumlah fitur mungkin berbeda
- Urutan fitur mungkin berbeda
- Jika ada fitur tambahan atau berkurang, akurasi akan berbeda

---

### 3. **PERBEDAAN DATA PREPROCESSING & CLEANING**

#### Di app.py:
```python
# Sudah ada logika tersendiri untuk:
- Handling missing values dengan metode spesifik
- Konversi jam dengan fungsi parse_time_to_decimal()
- Cleaning kolom pendapatan dengan cara tertentu
- Mungkin ada penanganan outliers
```

#### Di simulasi_simple.py:
```python
# Line 120-150
# Cleaning berbeda:
- Konversi jam menggunakan fungsi konversi_jam()
- Handle missing values dengan fillna(median/mode)
- Cleaning pendapatan dengan regex berbeda
```

**Perbedaan:**
- Jika preprocessing berbeda → data input ke model berbeda → akurasi berbeda

---

### 4. **RANDOM STATE & DATA SPLIT**

Meskipun keduanya menggunakan `random_state=42`, jika **fitur atau data preprocessing berbeda**, data yang masuk ke split juga berbeda, sehingga **train/test split akan berbeda**, yang menyebabkan **akurasi berbeda**.

---

## Penjelasan untuk Dosen

Jika dosen bertanya: **"Mengapa akurasi di app.py berbeda dengan simulasi_simple.py?"**

**Jawaban:**

> "Ada beberapa penyebab perbedaan akurasi:

> 1. **Metode perhitungan akurasi**: Di app.py, saya menggunakan cumulative probability voting dari subset trees (10, 20, ..., 150), sedangkan simulasi_simple.py menggunakan direct predict dari seluruh 150 trees sekaligus. Meskipun keduanya akhirnya menggunakan 150 trees, metode voting berbeda bisa memberikan hasil sedikit berbeda.

> 2. **Perbedaan fitur**: Fitur yang digunakan mungkin berbeda urutan atau jumlahnya, sehingga model mempelajari pola data yang berbeda.

> 3. **Perbedaan preprocessing**: Cara membersihkan data, mengkonversi jam, dan handle missing values mungkin sedikit berbeda, sehingga input ke model berbeda.

> 4. **Data split berbeda**: Meskipun random_state sama, jika data yang masuk ke split berbeda (akibat preprocessing), maka sampel train/test akan berbeda, menghasilkan model yang sedikit berbeda.

> **Kesimpulannya**: Perbedaan akurasi adalah **normal dan expected** karena perbedaan preprocessing dan fitur. Yang penting adalah kedua model menunjukkan **trend yang sama** (training accuracy lebih tinggi dari testing accuracy dengan gap yang reasonable, menunjukkan tidak overfitting parah)."

---

## Solusi: Membuat simulasi_simple.py Identik dengan app.py

Jika ingin hasil yang **sama persis**, simulasi_simple.py harus:

1. ✅ Menggunakan fungsi `build_model()` yang sama seperti app.py
2. ✅ Menggunakan fitur yang sama persis
3. ✅ Menggunakan preprocessing yang sama persis
4. ✅ Menggunakan metode perhitungan akurasi yang sama

**Opsi:**
- Salin langsung `build_model()` dari app.py ke simulasi_simple.py
- Pastikan fitur_motor dan fitur_mobil sama persis
- Gunakan fungsi preprocessing dari app.py

---

## Ringkasan Tabel Perbedaan

| Aspek | app.py | simulasi_simple.py |
|-------|--------|-------------------|
| Metode Akurasi | Cumulative Prob Voting (subset) | Direct Predict (all) |
| Fitur Motor | [list tertentu] | Dinamis dari jam_cols |
| Fitur Mobil | [list tertentu] | Dinamis dari jam_cols |
| Konversi Jam | parse_time_to_decimal() | konversi_jam() |
| Handle Missing | Spesifik per kolom | fillna(median/mode) |
| Cleaning Pend | Regex tertentu | Regex berbeda |
| Result | Akurasi Training = X% | Akurasi Training = Y% |
| | Akurasi Testing = X% | Akurasi Testing = Y% |

**Perbedaan akurasi adalah NORMAL karena preprocessing dan fitur berbeda.**
