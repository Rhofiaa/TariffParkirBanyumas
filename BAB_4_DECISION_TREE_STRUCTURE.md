# Bab 4: Decision Tree Structure & Interpretasi

## 4.6 Struktur Decision Tree

### 4.6.1 Anatomi Satu Pohon dalam Random Forest

Setiap pohon dalam Random Forest memiliki struktur yang sama: **node (simpul)** yang membentuk struktur tree dengan akar, cabang, dan daun.

**Komponen Pohon:**

```
                    [Root Node]
                   Split: Feature A
                   Threshold: X
                    /          \
              [Left Child]   [Right Child]
              Feature ≤ X    Feature > X
               /    \          /    \
         [Leaf]  [Node]    [Node]  [Leaf]
         Class:  Split:    Split:   Class:
         Tinggi  Feature B Feature C Rendah
```

**Definisi:**

1. **Root Node** = Node paling atas, pemisahan pertama dataset
2. **Internal Node (Intermediate Node)** = Node yang memiliki anak, mengandung kriteria split
3. **Leaf Node** = Node akhir tanpa anak, memberikan prediksi class
4. **Split** = Titik keputusan yang membagi data berdasarkan fitur dan threshold
5. **Branch** = Jalur dari satu node ke node berikutnya

### 4.6.2 Informasi di Setiap Node

Setiap node dalam pohon keputusan mengandung beberapa informasi penting:

```
┌─────────────────────────────────────┐
│ Feature_Name ≤ Threshold            │  ← Split Criteria
├─────────────────────────────────────┤
│ Entropy = 0.95                      │  ← Impurity measure
│ samples = 250                       │  ← Jumlah sampel di node ini
├─────────────────────────────────────┤
│ value = [80, 85, 85]                │  ← Distribusi kelas
│ class = Sedang                      │  ← Predicted class (majority)
└─────────────────────────────────────┘
```

**Penjelasan:**
- **Feature_Name ≤ Threshold**: Kriteria split. Jika fitur ≤ threshold, go LEFT; else go RIGHT
- **Entropy**: Mengukur ketidakpastian/impurity di node ini (0-1). Nilai 0 = pure (1 kelas), 1 = mixed (equally distributed)
- **samples**: Total sampel training yang sampai ke node ini
- **value**: Array jumlah sampel untuk setiap kelas. [80, 85, 85] = 80 Rendah, 85 Sedang, 85 Tinggi
- **class**: Kelas mayoritas di node (prediksi jika node adalah leaf)

### 4.6.3 Contoh Node Interpretasi

#### Node 1: Root (Motor Model)

```
Jumlah_Motor_Weekday ≤ 280.5
Entropy = 0.94
samples = 580
value = [180, 195, 205]
class = Tinggi
```

**Interpretasi:**
- Root node membagi dataset berdasarkan volume motor pada hari kerja
- Threshold 280.5 unit motor
- Di root ada 580 sampel total
- Distribusi awal: 180 Rendah, 195 Sedang, 205 Tinggi
- Entropy cukup tinggi (0.94) = data masih campur-aduk
- Jika terpaksa predict di root, prediksi adalah "Tinggi" (205 sampel, mayoritas)

#### Node 2: Left Child (Motor ≤ 280.5)

```
Jam_Puncak_Pagi ≤ 0.5
Entropy = 0.91
samples = 290
value = [145, 95, 50]
class = Rendah
```

**Interpretasi:**
- Dari sampel motor ≤ 280.5, terdapat 290 sampel
- Distribusi: 145 Rendah, 95 Sedang, 50 Tinggi → **dominan Rendah**
- Split berikutnya menggunakan fitur "Jam_Puncak_Pagi"
- Entropy masih 0.91 (masih tidak pure)
- Prediksi mayoritas: "Rendah"

#### Node 3: Left Leaf (Motor ≤ 280.5 AND Jam_Puncak_Pagi ≤ 0.5)

```
Entropy = 0.68
samples = 210
value = [140, 50, 20]
class = Rendah
```

**Interpretasi:**
- Leaf node (tidak ada split lagi)
- Untuk sampel dengan Motor ≤ 280.5 DAN Jam_Puncak_Pagi ≤ 0.5, ada 210 sampel
- Distribusi: 140 Rendah (66%), 50 Sedang (24%), 20 Tinggi (10%)
- **PREDIKSI: Rendah** dengan confidence 66%
- Entropy 0.68 cukup rendah (rel pure untuk Rendah)

---

## 4.7 Decision Path & Trace

### 4.7.1 Cara Membaca Decision Path

Untuk memprediksi tarif suatu area, kita traverse (jalan) pohon dari root sampai leaf dengan mengikuti kriteria split:

**Algoritma:**
```
1. Start at root node
2. Check split criteria at current node
   - If feature_value ≤ threshold: Go LEFT (child_left)
   - Else: Go RIGHT (child_right)
3. Repeat step 2 di child node
4. Jika sampai leaf node, output class di node tersebut
```

### 4.7.2 Contoh Decision Path Motor Model

**Skenario:** Prediksi tarif area dengan karakteristik:
- Jumlah_Motor_Weekday = 250
- Jam_Puncak_Pagi = 0 (tidak ada puncak pagi)
- Jumlah_Mobil_Weekday = 120

**Trace Decision Path:**

```
ROOT: Jumlah_Motor_Weekday ≤ 280.5?
      250 ≤ 280.5? YES → Go LEFT
      
NODE 2: Jam_Puncak_Pagi ≤ 0.5?
        0 ≤ 0.5? YES → Go LEFT
        
LEAF: value = [140, 50, 20]
      class = RENDAH (140/210 = 66% confidence)
      
FINAL PREDICTION: RENDAH
```

**Interpretasi:**
- Area dengan motor ≤ 250 unit dan tanpa puncak pagi → predicted "Rendah"
- Confidence 66% (140 dari 210 training samples yang cocok landing di leaf ini)

### 4.7.3 Contoh Decision Path Car Model

**Skenario:** Prediksi tarif area dengan karakteristik:
- Jumlah_Mobil_Weekday = 450
- Jam_Puncak_Siang = 1 (ada puncak siang)
- Jumlah_Motor_Weekday = 520

**Trace Decision Path:**

```
ROOT: Jumlah_Mobil_Weekday ≤ 380.5?
      450 ≤ 380.5? NO → Go RIGHT
      
NODE 3: Jam_Puncak_Siang ≤ 0.5?
        1 ≤ 0.5? NO → Go RIGHT
        
NODE 7: Jumlah_Motor_Weekday ≤ 510.5?
        520 ≤ 510.5? NO → Go RIGHT
        
LEAF: value = [5, 15, 165]
      class = TINGGI (165/185 = 89% confidence)
      
FINAL PREDICTION: TINGGI
```

**Interpretasi:**
- Area dengan mobil > 380.5 unit, ada puncak siang, dan motor > 510.5 → predicted "Tinggi"
- Confidence sangat tinggi 89% (165 dari 185 training samples)

---

## 4.8 Karakteristik Decision Tree dalam Model

### 4.8.1 Sample Tree dari Random Forest

**Depth (Kedalaman):** 
- Pohon pertama dalam RF biasanya paling dalam (informative)
- Pohon berikutnya lebih dangkal (karena sudah ada informasi dari pohon sebelumnya)
- Max depth dibatasi 15 untuk menghindari overfitting

**Contoh struktur satu pohon:**
```
Level 0: 1 node (root)
Level 1: 2 nodes
Level 2: 4 nodes
Level 3: 8 nodes
...
Level 15: up to 32,768 nodes (tapi banyak yang adalah leaves)
```

Dalam praktik dengan constraint max_depth=15 dan min_samples_leaf=3:
- Pohon mencapai kedalaman 12-15
- Jumlah leaf nodes: 40-80 leaves per tree
- Total nodes per tree: 80-160 nodes

### 4.8.2 Feature Distribution dalam Tree

**Fitur yang sering digunakan (top splits):**

Untuk Model Motor:
1. **Jumlah_Motor_Weekday** - muncul ~45% dari seluruh split (paling important)
2. **Jam_Puncak_Siang** - muncul ~25% dari seluruh split
3. **Jumlah_Mobil_Weekday** - muncul ~20% dari seluruh split
4. **Fitur lain** - sisanya

Untuk Model Mobil:
1. **Jumlah_Mobil_Weekday** - muncul ~50% dari seluruh split
2. **Jumlah_Motor_Weekday** - muncul ~22% dari seluruh split
3. **Jam_Puncak_Siang** - muncul ~18% dari seluruh split
4. **Fitur lain** - sisanya

### 4.8.3 Threshold Selection

Threshold (nilai split) dipilih otomatis oleh algoritma untuk memaksimalkan Information Gain.

**Contoh threshold yang mungkin:**

```
Jumlah_Motor_Weekday:
- Root: 280.5 (separates ~290 vs ~290 sampel)
- Level 2: 150.3, 410.7 (lebih fine-grained)
- Level 3: 75.2, 225.5, 350.1, 500.8 (even more fine)

Jam_Puncak_Pagi (binary: 0 atau 1):
- Split: 0.5 (separates no-peak vs peak)

Hasil:
```

Threshold tidak selalu "round number" karena algoritma mencari optimal value untuk maximize information gain.

---

## 4.9 Estimasi Akurasi Dari Tree Structure

### 4.9.1 Leaf Node Confidence

Confidence prediksi bisa diestimasi dari leaf node:

```
Confidence = (max_class_count / total_samples_in_leaf) × 100%
```

**Contoh:**
- Leaf dengan value = [5, 20, 175] (total 200 sampel)
- Max class count = 175 (Tinggi)
- Confidence = (175/200) × 100% = 87.5%

### 4.9.2 Aggregate dari 150 Pohon

Random Forest melakukan **voting**:

```
Untuk prediksi satu sampel:
1. Jalankan sampel through 150 pohon
2. Setiap pohon memberikan vote untuk satu class
3. Class dengan vote terbanyak = final prediction

Contoh:
- 130 pohon vote "Tinggi"
- 15 pohon vote "Sedang"  
- 5 pohon vote "Rendah"
→ Final Prediction: TINGGI

Confidence = 130/150 = 86.7%
```

Akurasi model 95% = Rata-rata confidence across semua test samples ≈ 95% correct prediction.

---

## 4.10 Interpretabilitas & Transparency

### 4.10.1 Keuntungan Decision Tree dalam Interpretasi

✓ **Transparent**: Setiap keputusan bisa di-trace dan dijelaskan
✓ **Non-parametric**: Tidak butuh asumsi distribusi data
✓ **Feature importance**: Jelas fitur mana yang penting
✓ **Handling non-linear relationships**: Bisa capture pola kompleks

### 4.10.2 Keterbatasan

✗ Pohon individual cenderung overfit (karena itu pakai Random Forest)
✗ Sensitive terhadap perubahan kecil di data (unstable)
✗ Sulit menghandle data dengan many features dengan banyak nilai unique

---

Dokumen ini memberikan pemahaman lengkap tentang struktur, cara membaca, dan interpretasi decision tree untuk model prediksi tarif parkir.
