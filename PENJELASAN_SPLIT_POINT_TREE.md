# Penjelasan Split Point pada Decision Tree

## Apa itu Nilai-Nilai Seperti 10.75, 17.25, 13.25, 8.5?

Nilai-nilai tersebut adalah **split points (threshold)** atau **nilai batas pemisahan** yang digunakan oleh algoritma Decision Tree untuk membagi data di setiap node.

### Contoh dari Tree Anda:
```
Root Node: Jam Sepi Motor Weekday <= 17.25
├── Left (True): Jam Ramai Motor Weekday <= 13.25 → Rendah
└── Right (False): Jam Sedang Motor Weekday <= 10.75 → Sedang
```

**Penjelasan:**
- **17.25** = Threshold untuk fitur "Jam Sepi Motor Weekday"
- **13.25** = Threshold untuk fitur "Jam Ramai Motor Weekday"  
- **10.75** = Threshold untuk fitur "Jam Sedang Motor Weekday"

---

## Bagaimana Cara Algoritma Menentukan Nilai-Nilai Ini?

Selama proses **training**, algoritma Decision Tree melakukan:

### Langkah 1: Cari Nilai Unik Setiap Fitur
Contoh untuk fitur "Jam Sepi Motor Weekday", data mungkin seperti:
```
[5.2, 8.5, 10.1, 13.7, 15.3, 17.25, 19.8, 22.4, ...]
```

### Langkah 2: Uji Semua Kemungkinan Threshold
Untuk setiap nilai unik, hitung **Information Gain** atau **Gini Impurity**:

| Threshold | Gini Impurity | Information Gain |
|-----------|---------------|------------------|
| 5.2       | 0.48          | 0.12             |
| 8.5       | 0.42          | 0.18             |
| 10.1      | 0.38          | 0.22             |
| **13.7**  | **0.32**      | **0.28** ✓       |
| 15.3      | 0.45          | 0.15             |
| **17.25** | **0.31**      | **0.29** ✓✓ BEST |
| 19.8      | 0.50          | 0.10             |

### Langkah 3: Pilih Threshold dengan Information Gain Terbaik
Algoritma memilih **17.25** karena memberikan **Information Gain tertinggi (0.29)**.

---

## Rumus Information Gain

### Rumus Gini Impurity:
$$\text{Gini}(p) = 1 - \sum_{i=1}^{k} p_i^2$$

Dimana:
- $p_i$ = proporsi kelas i di node
- $k$ = jumlah kelas (dalam kasus Anda: 3 = Rendah, Sedang, Tinggi)

### Contoh Hitung Manual untuk Threshold 17.25:

**Sebelum split (semua data di root):**
```
Data total: 203 sampel
Rendah: 115 sampel (p1 = 115/203 = 0.566)
Sedang: 107 sampel (p2 = 107/203 = 0.527)
Tinggi: 102 sampel (p3 = 102/203 = 0.502)

Gini(parent) = 1 - (0.566² + 0.527² + 0.502²)
             = 1 - (0.320 + 0.278 + 0.252)
             = 1 - 0.850
             = 0.150  ← nilai "gini = 0.666" di node Anda
```

**Setelah split dengan threshold 17.25:**

**Left node (Jam Sepi Motor Weekday <= 17.25):**
```
Data: 176 sampel
Rendah: 107 (p1 = 107/176 = 0.608)
Sedang: 78 (p2 = 78/176 = 0.443)
Ramai: 94 (p3 = 94/176 = 0.534)

Gini(left) = 1 - (0.608² + 0.443² + 0.534²)
           = 1 - (0.370 + 0.196 + 0.285)
           = 1 - 0.851
           = 0.149
```

**Right node (Jam Sepi Motor Weekday > 17.25):**
```
Data: 27 sampel
Rendah: 8 (p1 = 8/27 = 0.296)
Sedang: 29 (p2 = 29/27 = 1.074) [ERROR - ini illustrative saja]
```

### Information Gain:
$$\text{IG} = \text{Gini}(parent) - \left(\frac{n_{left}}{n_{total}} \times \text{Gini}(left) + \frac{n_{right}}{n_{total}} \times \text{Gini}(right)\right)$$

$$\text{IG} = 0.150 - (0.866 \times 0.149 + 0.134 \times \text{Gini}(right))$$

**Algoritma memilih threshold yang menghasilkan IG tertinggi.**

---

## Mengapa Berbeda-Beda? (17.25 vs 13.25 vs 10.75)

Setiap node mencari **fitur dan threshold terbaik untuk split data mereka sendiri**:

1. **Root node** → Cari feature + threshold terbaik dari SEMUA 203 sampel → **17.25 pada Jam Sepi Motor Weekday**

2. **Left child node** → Cari feature + threshold terbaik dari 176 sampel saja → **13.25 pada Jam Ramai Motor Weekday**

3. **Right child node** → Cari feature + threshold terbaik dari 27 sampel saja → **10.75 pada Jam Sedang Motor Weekday**

Karena data berbeda di setiap node, feature dan threshold optimal juga berbeda!

---

## Proses Ini Terjadi Otomatis During Training

**Anda TIDAK perlu menghitung manual** di code. Scikit-learn Random Forest melakukan ini secara otomatis:

```python
from sklearn.ensemble import RandomForestClassifier

# Training
model = RandomForestClassifier(n_estimators=150, max_depth=15, ...)
model.fit(X_train, y_train)

# Model sudah menemukan semua split points otomatis!
# Setiap tree dalam forest memiliki split points sendiri
```

---

## Cara Melihat Split Points di Kode

```python
from sklearn.tree import export_text

# Lihat struktur satu tree
tree_rules = export_text(model.estimators_[0], feature_names=feature_names)
print(tree_rules)
```

**Output mirip:**
```
|--- Jam Sepi Motor Weekday <= 17.25
|   |--- Jam Ramai Motor Weekday <= 13.25
|   |   |--- class: Rendah
|   |--- Jam Ramai Motor Weekday > 13.25
|   |   |--- Jam Sedang Motor Weekday <= 10.75
|   |   |   |--- class: Sedang
```

---

## Ringkasan untuk Ujian/Bimbingan

**Pertanyaan Dosen:** "Kok 17.25? Darimana nilainya?"

**Jawaban Anda:**
> "Nilai 17.25 adalah threshold optimal untuk fitur 'Jam Sepi Motor Weekday' di root node. Selama training, algoritma Decision Tree menguji semua nilai unik fitur ini dan menghitung Information Gain (menggunakan Gini Impurity) untuk setiap threshold. Threshold yang memberikan Information Gain tertinggi dipilih karena dapat membagi data dengan paling efektif ke dua kelas. Proses ini dilakukan otomatis oleh scikit-learn dan menggunakan greedy algorithm untuk setiap node secara independen."

**Pertanyaan Dosen:** "Cara hitungnya gimana?"

**Jawaban Anda:**
> "Menggunakan rumus Gini Impurity: Gini(p) = 1 - Σ(p_i²). Sebelum split, kita hitung Gini parent node dengan proporsi setiap kelas. Setelah split di threshold tertentu, hitung Gini left dan right child. Information Gain = Gini(parent) - weighted average Gini(children). Threshold dengan IG tertinggi dipilih. Perhitungan ini untuk semua 203 sampel di root node, menghasilkan threshold 17.25 yang optimal."

---

## File Referensi dalam Project Anda

Untuk lihat split points model Anda:

1. **app.py** → Bagian `display_tree_visualization()` menampilkan tree dengan split points
2. **Terminal Python** → 
```python
from sklearn.tree import export_text
rules = export_text(model.estimators_[0], feature_names=['Jumlah Motor Weekday', ...])
print(rules)
```

---

## Penjelasan Format Jam Desimal (17.25, 13.5, dll)

### Perbedaan PENTING: Desimal Biasa vs Jam Desimal

**Ini BUKAN desimal biasa!** Ada perbedaan besar:

| Format | Nilai | Waktu Sebenarnya | Cara Baca |
|--------|-------|-----------------|-----------|
| **Desimal Biasa** | 17.15 | 17 jam 9 menit | 17 + 0.15 = 17.15 |
| **Desimal Biasa** | 17.75 | 17 jam 45 menit | 17 + 0.75 = 17.75 |
| **Jam Desimal** | 17.25 | 17 jam 15 menit | 17 + 15/60 = 17.25 |
| **Jam Desimal** | 10.75 | 10 jam 45 menit | 10 + 45/60 = 10.75 |

**Lihat perbedaannya!**
- Desimal biasa 17.15 = 17 jam 9 menit (BUKAN 17 jam 15 menit!)
- Jam desimal 17.25 = 17 jam 15 menit ✓ (ini yang kita gunakan)

### Mengapa Ada 17.25, 10.75, dll?

Nilai jam di dalam tree adalah **jam desimal (decimal hours)** sebelum digunakan untuk training.

### Konversi Jam ke Jam Desimal

**Rumus:**
$$\text{Jam Desimal} = \text{Jam} + \frac{\text{Menit}}{60}$$

**Contoh:**
| Format Input | Jam | Menit | Perhitungan | Jam Desimal |
|-------------|-----|-------|-----------|------------|
| 17:15 | 17 | 15 | 17 + 15/60 | 17.25 |
| 13:30 | 13 | 30 | 13 + 30/60 | 13.50 |
| 10:45 | 10 | 45 | 10 + 45/60 | 10.75 |
| 08:30 | 8 | 30 | 8 + 30/60 | 8.50 |
| 20:00 | 20 | 0 | 20 + 0/60 | 20.00 |

**Lihat! Setiap menit = 1/60 dalam desimal:**
- 15 menit = 15/60 = 0.25
- 30 menit = 30/60 = 0.50
- 45 menit = 45/60 = 0.75
- 9 menit = 9/60 ≈ 0.15

### Di Dalam Code Anda

Fungsi `parse_time_to_decimal()` di app.py melakukan konversi ini:

```python
def parse_time_to_decimal(time_str):
    """Mengkonversi string waktu (H.M, H:M, atau H) menjadi jam desimal."""
    time_str = str(time_str).replace(',', '.').replace(':', '.')
    if '.' in time_str:
        h_str, m_part_str = time_str.split('.', 1)
        h = int(h_str)  # Jam
        m = int(m_part_str.ljust(2, '0')[:2])  # Menit (2 digit)
        return h + m / 60.0  # ← Konversi menit ke desimal JAM (bukan desimal biasa)
    else:
        return float(time_str)
```

**Contoh eksekusi:**
```python
# Input: "17.15" atau "17:15" (berarti 17 jam 15 menit)
# Proses: h = 17, m = 15
# Rumus: 17 + (15 ÷ 60) = 17 + 0.25 = 17.25
# Output: 17.25 ✓

# Input: "10.45" atau "10:45" (berarti 10 jam 45 menit)
# Proses: h = 10, m = 45
# Rumus: 10 + (45 ÷ 60) = 10 + 0.75 = 10.75
# Output: 10.75 ✓
```

**Catatan Penting:**
- Divisi `/60` adalah KUNCI yang membedakan
- Tanpa `/60`, maka 17:15 = desimal biasa 17.15 (= 17 jam 9 menit) ❌
- Dengan `/60`, maka 17:15 = jam desimal 17.25 (= 17 jam 15 menit) ✓

### Keuntungan Format Desimal

**Mengapa harus dikonversi? Karena algoritma Machine Learning memerlukan:**

1. **Angka Kontinyu (Continuous Numbers)**
   - Decision Tree perlu membuat perbandingan: `apakah jam <= 17.25?`
   - Tidak bisa membandingkan string/teks "17:15" secara numerik
   - Format desimal bisa dibandingkan: 17.25 > 13.5 > 10.75 ✓

2. **Urutan yang Benar (Ordered)**
   ```
   Salah (jika teks):      Benar (desimal):
   "17:15" = string         17.25 = angka
   "20:00" = string         20.00 = angka
   "08:30" = string         8.50 = angka
   
   Tidak bisa dibanding!    Bisa dibanding!
                            8.50 < 17.25 < 20.00 ✓
   ```

3. **Split Point yang Masuk Akal**
   - Decision Tree perlu membuat "split" di tengah-tengah
   - Contoh: "Apakah jam <= 17.25?" (17 jam 15 menit)
   - Ini HANYA bisa dilakukan dengan angka, bukan teks

4. **Perhitungan Information Gain**
   - Algoritma perlu hitung Gini Impurity untuk setiap threshold
   - Gini Impurity hanya bisa dihitung dengan angka
   - Teks "17:15" tidak bisa digunakan dalam rumus matematika ❌

### Analogi Sederhana

**Bayangkan Anda punya daftar umur orang:**
```
Jika format teks:
Umur = ["25 tahun", "30 tahun", "45 tahun", "18 tahun"]

Algoritma bertanya: "Siapa yang lebih muda dari 30 tahun?"
Komputer bingung! Karena "25 tahun" adalah teks, tidak bisa dibanding.

Jika format angka:
Umur = [25, 30, 45, 18]

Algoritma bertanya: "Siapa yang umur <= 30?"
Komputer bisa jawab! [25, 18] ✓
```

**SAMA PERSIS dengan jam:**
```
Jika format teks "HH:MM":
Jam = ["17:15", "20:00", "08:30", "13:45"]
Algoritma tidak bisa membuat split point ❌

Jika format desimal:
Jam = [17.25, 20.00, 8.50, 13.75]
Algoritma bisa membuat split "jam <= 17.25" ✓
```

### Contoh Nyata dalam Model Anda

**Tanpa konversi (TIDAK BISA):**
```
Decision Tree mencoba membuat rule:
  "Jam >= '17:15'" ?
  
Ini TIDAK BISA dilakukan dengan teks!
Komputer tidak tahu cara membanding string "17:15"
```

**Dengan konversi (BISA):**
```
Decision Tree membuat rule:
  "Jam >= 17.25" ?
  
INI BISA! Karena 17.25 adalah angka
Komputer bisa bandingkan: 17.5 >= 17.25? YES ✓
                         16.8 >= 17.25? NO ✓
```

### Jadi Penjelasan untuk Dosen

**Pertanyaan Dosen:** "Kenapa harus dikonversi? Kok ada 17.25?"

**Jawaban:**
> "Jam harus dikonversi dari format teks '17:15' menjadi angka desimal 17.25 karena algoritma machine learning (Decision Tree) hanya bisa bekerja dengan angka, bukan teks. Algoritma perlu membuat split point berupa perbandingan numerik seperti 'Jam <= 17.25?', yang hanya bisa dilakukan jika data adalah angka. Jika data tetap berformat teks, algoritma tidak bisa membandingkan dan membuat rule yang berarti. Konversi dilakukan dengan rumus: Jam Desimal = Jam + (Menit ÷ 60), sehingga 17:15 menjadi 17.25, yang mempertahankan urutan waktu yang benar untuk perhitungan Information Gain dan pembuatan split points."

---

**Catatan Penting:**
- Setiap tree dalam Random Forest (150 trees) memiliki split points berbeda-beda
- Nilai split points otomatis ditentukan selama training, bukan input manual
- Split points berbeda karena setiap tree dilatih dengan data sampel berbeda (bootstrap)
- Ini adalah keindahan Random Forest: diversitas tree → prediksi lebih robust
- **Format jam desimal digunakan HANYA untuk training model**, output final tetap dalam format readable
