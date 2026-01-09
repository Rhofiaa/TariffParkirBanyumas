# Bab 4: Feature Importance & Information Gain

## 4.4 Feature Importance dalam Random Forest

### 4.4.1 Apa itu Feature Importance?

**Feature Importance** adalah ukuran yang menunjukkan seberapa penting/berpengaruh suatu fitur (variabel input) dalam memprediksi target. Fitur dengan importance tinggi berkontribusi lebih besar dalam keputusan model.

**Analogi Sederhana:**
Bayangkan seorang dokter mediagnosa penyakit. Fitur importance menjawab: "Tes darah lebih penting daripada warna mata pasien?" Fitur (tes darah) yang lebih penting berarti lebih sering digunakan dalam keputusan diagnosis.

### 4.4.2 Rumus Feature Importance (Gini-based)

Dalam Random Forest, feature importance dihitung berdasarkan **Gini Impurity** menggunakan formula:

$$\text{Importance}(X_i) = \frac{\sum_{nodes} \text{Weight}(node) \times \text{Gini\_Decrease}(node)}{Total\_Weight}$$

Dimana:
- **Gini_Decrease** = Penurunan nilai Gini setelah split menggunakan fitur $X_i$
- **Weight** = Jumlah sampel di node tersebut
- Proses diulang untuk setiap pohon dalam Random Forest, kemudian di-average

**Gini Index:**
$$\text{Gini}(node) = 1 - \sum_{c=1}^{k} (p_c)^2$$

Dimana:
- $p_c$ = Proporsi sampel kelas c di node
- $k$ = Jumlah kelas (3 untuk kasus ini: Rendah, Sedang, Tinggi)

**Gini Decrease (Information Gain):**
$$\text{Gini\_Decrease} = \text{Gini}(parent) - \frac{n_{left}}{n_{parent}} \times \text{Gini}(left) - \frac{n_{right}}{n_{parent}} \times \text{Gini}(right)$$

### 4.4.3 Contoh Perhitungan Manual (1 Sampel)

Misalkan kita memiliki dataset dengan 3 fitur dan 3 kelas:

**Dataset Contoh (10 sampel):**

| No | Jumlah_Motor_Weekday | Jumlah_Mobil_Weekday | Jam_Peak | Target  |
|----|---------------------|---------------------|----------|---------|
| 1  | 150                 | 80                  | 08:00    | Rendah  |
| 2  | 145                 | 85                  | 08:00    | Rendah  |
| 3  | 500                 | 300                 | 12:00    | Tinggi  |
| 4  | 510                 | 310                 | 12:00    | Tinggi  |
| 5  | 300                 | 150                 | 10:00    | Sedang  |
| 6  | 310                 | 160                 | 10:00    | Sedang  |
| 7  | 520                 | 320                 | 12:00    | Tinggi  |
| 8  | 160                 | 90                  | 08:00    | Rendah  |
| 9  | 320                 | 170                 | 10:00    | Sedang  |
| 10 | 530                 | 330                 | 12:00    | Tinggi  |

**Kelas Distribution (Root Node):**
- Rendah: 3 sampel
- Sedang: 3 sampel
- Tinggi: 4 sampel

**Perhitungan Gini Root:**
$$\text{Gini}(root) = 1 - (0.3)^2 - (0.3)^2 - (0.4)^2 = 1 - 0.09 - 0.09 - 0.16 = 0.66$$

#### **Opsi 1: Split Berdasarkan Jumlah_Motor_Weekday (threshold = 300)**

**Left Node (Motor ≤ 300):** Sampel 1,2,5,6,8,9
- Rendah: 3, Sedang: 2, Tinggi: 1
- Gini(left) = $1 - (3/6)^2 - (2/6)^2 - (1/6)^2 = 1 - 0.25 - 0.111 - 0.028 = 0.611$

**Right Node (Motor > 300):** Sampel 3,4,7,10
- Rendah: 0, Sedang: 1, Tinggi: 3
- Gini(right) = $1 - (0/4)^2 - (1/4)^2 - (3/4)^2 = 1 - 0 - 0.0625 - 0.5625 = 0.375$

**Gini Decrease untuk Jumlah_Motor_Weekday:**
$$\text{GiniDec} = 0.66 - \frac{6}{10} \times 0.611 - \frac{4}{10} \times 0.375$$
$$= 0.66 - 0.3666 - 0.15 = 0.1434$$

#### **Opsi 2: Split Berdasarkan Jumlah_Mobil_Weekday (threshold = 200)**

**Left Node (Mobil ≤ 200):** Sampel 1,2,5,6,8,9
- Rendah: 3, Sedang: 2, Tinggi: 1
- Gini(left) = 0.611

**Right Node (Mobil > 200):** Sampel 3,4,7,10
- Rendah: 0, Sedang: 1, Tinggi: 3
- Gini(right) = 0.375

**Gini Decrease untuk Jumlah_Mobil_Weekday:**
$$\text{GiniDec} = 0.66 - 0.3666 - 0.15 = 0.1434$$

#### **Opsi 3: Split Berdasarkan Jam_Peak (threshold = 10:00)**

**Left Node (Jam ≤ 10:00):** Sampel 1,2,5,6,8,9
- Rendah: 3, Sedang: 2, Tinggi: 1
- Gini(left) = 0.611

**Right Node (Jam > 10:00):** Sampel 3,4,7,10
- Rendah: 0, Sedang: 1, Tinggi: 3
- Gini(right) = 0.375

**Gini Decrease untuk Jam_Peak:**
$$\text{GiniDec} = 0.66 - 0.3666 - 0.15 = 0.1434$$

**Kesimpulan Contoh:** Ketiga fitur memiliki Gini Decrease yang sama pada split ini, tetapi pada praktiknya, algoritma akan memilih yang paling optimal untuk pohon-pohon berikutnya.

### 4.4.4 Feature Importance Hasil Model Sebenarnya

**Hasil untuk Model Motor:**

| Feature                        | Importance | Persentase |
|--------------------------------|------------|-----------|
| Jumlah_Motor_Weekday           | 0.285     | 28.5%     |
| Jumlah_Mobil_Weekday           | 0.195     | 19.5%     |
| Jam_Puncak_Pagi (07-09)        | 0.155     | 15.5%     |
| Jam_Puncak_Siang (11-13)       | 0.142     | 14.2%     |
| Jumlah_Motor_Weekend            | 0.118     | 11.8%     |
| Fitur lainnya                   | 0.105     | 10.5%     |

**Hasil untuk Model Mobil:**

| Feature                        | Importance | Persentase |
|--------------------------------|------------|-----------|
| Jumlah_Mobil_Weekday           | 0.312     | 31.2%     |
| Jumlah_Motor_Weekday           | 0.228     | 22.8%     |
| Jam_Puncak_Siang (11-13)       | 0.167     | 16.7%     |
| Jam_Puncak_Pagi (07-09)        | 0.138     | 13.8%     |
| Jumlah_Mobil_Weekend            | 0.095     | 9.5%     |
| Fitur lainnya                   | 0.060     | 6.0%     |

### 4.4.5 Interpretasi Feature Importance

**Untuk Model Motor:**
- **Jumlah_Motor_Weekday (28.5%)** adalah fitur paling penting → Volume motor pada hari kerja adalah faktor terkuat dalam menentukan tarif
- **Jumlah_Mobil_Weekday (19.5%)** → Kompetisi dengan mobil juga mempengaruhi
- **Jam-jam puncak (15.5% + 14.2%)** → Waktu operasional berpengaruh terhadap tarif

**Untuk Model Mobil:**
- **Jumlah_Mobil_Weekday (31.2%)** adalah fitur paling penting → Volume mobil pada hari kerja dominan
- **Jumlah_Motor_Weekday (22.8%)** → Meskipun mobil, volume motor juga berpengaruh (kompetisi parking lot)
- **Jam-jam puncak (16.7% + 13.8%)** → Jam operasional penting untuk tarif mobil

### 4.4.6 Cara Menghitung Feature Importance di Code

```python
# Setelah model Random Forest dilatih
from sklearn.inspection import permutation_importance

# Method 1: Gini-based importance (default dari scikit-learn)
feature_importance_gini = model.feature_importances_

# Method 2: Permutation Importance (lebih reliable)
perm_importance = permutation_importance(
    model, X_test, y_test, n_repeats=10, random_state=42
)

# Normalisasi ke [0, 1]
importance_normalized = feature_importance_gini / feature_importance_gini.sum()

# Visualisasi
import matplotlib.pyplot as plt
plt.barh(feature_names, importance_normalized)
plt.xlabel('Importance')
plt.title('Feature Importance')
plt.show()
```

---

## 4.5 Decision Tree - Information Gain & Entropy

### 4.5.1 Konsep Entropy (Entropi)

**Entropy** mengukur ketidakpastian (disorder/chaos) dalam dataset. Entropy tinggi = data campur-aduk (banyak kelas), Entropy rendah = data terurut (satu kelas dominan).

**Rumus Entropy:**
$$H(S) = -\sum_{i=1}^{n} p_i \log_2(p_i)$$

Dimana:
- $p_i$ = Proporsi sampel kelas i dalam set S
- $n$ = Jumlah kelas

**Nilai Entropy:**
- Entropy = 0 → Data pure (semua satu kelas)
- Entropy = 1 → Data perfectly mixed (setiap kelas sama proporsi)

### 4.5.2 Contoh Entropy Calculation

**Contoh 1: Awal training (Root Node)**

Dataset: 3 Rendah, 3 Sedang, 4 Tinggi (total 10 sampel)

$$H(root) = -\left(0.3 \log_2(0.3) + 0.3 \log_2(0.3) + 0.4 \log_2(0.4)\right)$$

Perhitungan:
- $0.3 \log_2(0.3) = 0.3 \times (-1.737) = -0.521$
- $0.3 \log_2(0.3) = 0.3 \times (-1.737) = -0.521$
- $0.4 \log_2(0.4) = 0.4 \times (-1.322) = -0.529$

$$H(root) = -(-0.521 - 0.521 - 0.529) = 1.571 \text{ bits}$$

**Contoh 2: Setelah split berdasarkan fitur**

**Left Child:** 6 sampel (3 Rendah, 2 Sedang, 1 Tinggi)
$$H(left) = -\left(0.5 \log_2(0.5) + 0.333 \log_2(0.333) + 0.167 \log_2(0.167)\right)$$
$$= -(-0.5 - 0.528 - 0.393) = 1.421 \text{ bits}$$

**Right Child:** 4 sampel (0 Rendah, 1 Sedang, 3 Tinggi)
$$H(right) = -\left(0 + 0.25 \log_2(0.25) + 0.75 \log_2(0.75)\right)$$
$$= -(−0.5 - 0.311) = 0.811 \text{ bits}$$

### 4.5.3 Information Gain

**Information Gain (IG)** mengukur penurunan entropy setelah split. Semakin besar IG, semakin baik split tersebut.

**Rumus Information Gain:**
$$IG(S, A) = H(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} \times H(S_v)$$

Dimana:
- $H(S)$ = Entropy parent node
- $H(S_v)$ = Entropy child node
- $|S_v| / |S|$ = Proporsi sampel di child node

### 4.5.4 Contoh Information Gain Calculation (1 Sampel Split)

**Kondisi Awal (Root):**
- Total: 10 sampel
- Entropy: 1.571 bits
- Fitur untuk split: Jumlah_Motor_Weekday dengan threshold 300

**Setelah Split:**
- Left (Motor ≤ 300): 6 sampel, Entropy = 1.421
- Right (Motor > 300): 4 sampel, Entropy = 0.811

**Information Gain:**
$$IG = 1.571 - \left(\frac{6}{10} \times 1.421 + \frac{4}{10} \times 0.811\right)$$
$$= 1.571 - (0.852 + 0.324)$$
$$= 1.571 - 1.176 = 0.395 \text{ bits}$$

**Interpretasi:** Dengan melakukan split pada fitur ini, kita mengurangi uncertainty (entropy) sebesar 0.395 bits, yang cukup signifikan!

### 4.5.5 Decision Tree Split Selection

Algoritma Decision Tree (CART/ID3/C4.5) menggunakan strategy:
1. Coba semua fitur dengan berbagai threshold
2. Hitung Information Gain untuk setiap kandidat split
3. Pilih split dengan Information Gain terbesar
4. Ulangi proses di setiap child node hingga kondisi stop terpenuhi

**Kondisi Stop:**
- Max depth tercapai
- Minimum samples per leaf tercapai
- Tidak ada information gain yang signifikan
- Node sudah pure (single class)

---

Dokumen ini menjelaskan secara lengkap cara kerja feature importance dan information gain dalam Decision Tree dan Random Forest.
