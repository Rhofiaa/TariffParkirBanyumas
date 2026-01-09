# Bab 5: Pembangunan Tarif Ideal & Adaptif

## 5.1 Konsep Tarif Ideal dan Tarif Adaptif

### 5.1.1 Definisi

**Tarif Ideal:**
Tarif parkir yang optimal untuk memaksimalkan:
- Revenue (pendapatan) untuk penyelenggara
- Accessibility (aksesibilitas) untuk pengguna
- Sustainability (keberlanjutan) sistem parkir

**Tarif Adaptif:**
Sistem tarif yang menyesuaikan dengan kondisi real-time atau karakteristik spesifik area parkir, bukan tarif flat (seragam) untuk semua area.

### 5.1.2 Mengapa Diperlukan Tarif Adaptif?

**Masalah dengan Tarif Flat (Seragam):**
- Area dengan demand tinggi kekurangan spot parkir
- Area dengan demand rendah memiliki spot idle (kosong)
- Pendapatan tidak maksimal di area-area premium
- Inefficient resource allocation

**Solusi dengan Tarif Adaptif:**
- Tarif tinggi di area premium (high demand) → Reduce demand, increase revenue
- Tarif rendah di area kurang prime (low demand) → Attract demand
- Equilibrium supply-demand
- Maksimal utilization dan revenue

---

## 5.2 Metodologi Pembangunan Tarif Ideal

### 5.2.1 Data-Driven Approach

Tarif ideal dibangun berdasarkan **karakteristik area sebenarnya** menggunakan output dari model Random Forest:

```
Step 1: Identifikasi Karakteristik Area
        ↓
Step 2: Prediksi Kategori Potensi Tarif dengan Model
        ↓
Step 3: Tentukan Tarif Dasar untuk Setiap Kategori
        ↓
Step 4: Validasi dengan Data Historis
        ↓
Step 5: Fine-tune dengan Expert Opinion
        ↓
Step 6: Implement & Monitor
```

### 5.2.2 Mapping: Kategori Model → Tarif Ideal

Model Random Forest memprediksi 3 kategori: **Rendah, Sedang, Tinggi**

**Mapping ke Tarif Ideal (Contoh untuk Motor):**

| Kategori Prediksi | Karakteristik Area | Tarif Ideal/Jam | Tarif Ideal/Hari |
|---|---|---|---|
| **RENDAH** | Volume kendaraan rendah, lokasi tepi, akses sulit | Rp 1.000 - Rp 2.000 | Rp 5.000 - Rp 10.000 |
| **SEDANG** | Volume medium, lokasi semi-central, akses normal | Rp 2.500 - Rp 4.000 | Rp 12.500 - Rp 20.000 |
| **TINGGI** | Volume tinggi, lokasi premium/central, akses mudah | Rp 5.000 - Rp 8.000 | Rp 25.000 - Rp 40.000 |

**Mapping ke Tarif Ideal untuk Mobil:**

| Kategori Prediksi | Karakteristik Area | Tarif Ideal/Jam | Tarif Ideal/Hari |
|---|---|---|---|
| **RENDAH** | Volume rendah, lokasi tepi, sarana terbatas | Rp 2.000 - Rp 3.000 | Rp 10.000 - Rp 15.000 |
| **SEDANG** | Volume medium, lokasi semi-central, sarana standard | Rp 3.500 - Rp 5.500 | Rp 17.500 - Rp 27.500 |
| **TINGGI** | Volume tinggi, lokasi central/premium, sarana lengkap | Rp 7.000 - Rp 10.000 | Rp 35.000 - Rp 50.000 |

### 5.2.3 Rumus Perhitungan Tarif Ideal

#### **Metode 1: Price Elasticity Based**

$$\text{Tarif\_Ideal} = \text{Tarif\_Current} \times \left(1 + \alpha \times \frac{Demand - Supply}{Supply}\right)$$

Dimana:
- α = Price elasticity coefficient (0.2 - 0.5 typical)
- Demand = Volume kendaraan
- Supply = Kapasitas parkir

#### **Metode 2: Category-Based (Simplified)**

$$\text{Tarif\_Ideal} = \text{Tarif\_Base} + \text{Category\_Premium}$$

Dimana:
- **Tarif_Base** = Tarif minimum (Kategori Rendah)
- **Category_Premium** = Tambahan berdasarkan kategori
  - Rendah: +0% (Rp 0)
  - Sedang: +100% (Rp 1 × Tarif_Base)
  - Tinggi: +200% (Rp 2 × Tarif_Base)

**Contoh Motor:**
```
Tarif_Base = Rp 1.500/jam (kategori Rendah)

- Kategori RENDAH: 1.500 + 0 = Rp 1.500/jam
- Kategori SEDANG: 1.500 + 1.500 = Rp 3.000/jam
- Kategori TINGGI: 1.500 + 3.000 = Rp 4.500/jam
```

#### **Metode 3: Revenue-Optimized**

$$\text{Tarif\_Ideal} = \arg\max_{T} \left( T \times \text{Demand}(T) \times \text{Occupancy\_Rate} \right)$$

Dimana:
- Demand(T) = Fungsi demand yang menurun dengan tarif T
- Occupancy_Rate = Tingkat okupansi parking lot (target 80-90%)

---

## 5.3 Estimasi Revenue Improvement

### 5.3.1 Perhitungan Revenue

**Formula:**
$$\text{Revenue} = \text{Tarif} \times \text{Volume} \times \text{Days\_per\_Month}$$

### 5.3.2 Contoh Perhitungan Revenue

**Skenario Motor di Area "Tinggi":**

**Current State (Flat Tariff):**
- Tarif = Rp 2.000/jam (rata-rata)
- Volume = 500 motor/hari
- Rata-rata durasi = 3 jam
- Operating days = 26 hari

$$\text{Revenue\_Current} = 2.000 \times 500 \times 3 \times 26 = \text{Rp 78.000.000/bulan}$$

**Dengan Tarif Adaptif (Kategori Tinggi):**
- Tarif baru = Rp 4.500/jam
- Expected volume decrease = 20% (demand elasticity)
- New volume = 500 × 0.8 = 400 motor/hari
- Durasi tetap = 3 jam
- Operating days = 26 hari

$$\text{Revenue\_Adaptif} = 4.500 \times 400 \times 3 \times 26 = \text{Rp 140.400.000/bulan}$$

**Improvement:**
$$\frac{\text{Revenue\_Adaptif} - \text{Revenue\_Current}}{\text{Revenue\_Current}} \times 100\% = \frac{62.400.000}{78.000.000} \times 100\% = 80\% \text{ increase}$$

### 5.3.3 Balanced Revenue & Accessibility

Namun, tarif terlalu tinggi bisa mengurangi accessibility. **Optimal balance:**

$$\text{Target\_Occupancy} = 80-85\%$$

Jika occupancy > 85%: Naik tarif
Jika occupancy < 70%: Turun tarif

---

## 5.4 Proses Validasi Tarif Ideal

### 5.4.1 Validasi dengan Data Historis

**Step 1:** Ambil data historis seluruh area parkir

**Step 2:** Group by prediction category dari model

**Step 3:** Analisis rata-rata:
- Volume kendaraan
- Durasi parkir
- Occupancy rate
- Revenue per spot

**Step 4:** Bandingkan dengan tarif ideal yang proposed

```
Contoh Result:

Kategori RENDAH:
- Rata-rata volume: 150 motor/hari
- Rata-rata durasi: 2.5 jam
- Occupancy rate: 45%
- Current tarif: Rp 2.000/jam
- Proposed tarif: Rp 1.500/jam ✓ (cocok, occupancy tetap rendah)

Kategori TINGGI:
- Rata-rata volume: 600 motor/hari
- Rata-rata durasi: 3.5 jam
- Occupancy rate: 95%
- Current tarif: Rp 2.000/jam
- Proposed tarif: Rp 4.500/jam ✓ (cocok, occupancy tinggi)
```

### 5.4.2 Sensitivity Analysis

Test bagaimana tarif ideal response terhadap perubahan:

```
Jika volume meningkat 20%:
- Kategori Tinggi masih occupy 95%? Ya → Naikkan tarif 10% lagi
- Atau occupancy akan jadi 114% (oversupply)? Tidak mungkin
  → Target occupancy 85% → Tarif harus naik untuk control demand

Jika volume menurun 30% (economic downturn):
- Kategori Sedang akan occupy 40%? Ya → Turunkan tarif untuk attract demand
```

---

## 5.5 Implementasi & Monitoring

### 5.5.1 Implementasi Bertahap

**Phase 1: Pilot (1-3 bulan)**
- Implement di 2-3 area kategori Tinggi
- Monitor occupancy, revenue, customer feedback
- Adjust tarif jika needed

**Phase 2: Expansion (3-6 bulan)**
- Expand ke semua area kategori Tinggi
- Implement di area Sedang
- Continue monitoring

**Phase 3: Full Implementation (6+ bulan)**
- Implement di semua area (Rendah, Sedang, Tinggi)
- Establish dynamic pricing if needed
- Regular review dan adjustment

### 5.5.2 KPI Monitoring

**Key Indicators to Track:**

| KPI | Target | How to Measure |
|---|---|---|
| **Revenue Growth** | +50-100% increase | Revenue Month-to-Month comparison |
| **Occupancy Rate** | 80-85% | Available spots / Total spots |
| **Customer Satisfaction** | ≥ 3.5/5 rating | Survey atau customer feedback |
| **Compliance** | ≥ 95% | Amount collected / Amount charged |
| **Turnaround Time** | < 30 min avg | Duration = Out time - In time |

### 5.5.3 Regular Review Cycle

```
Every 3 Months:
├─ Analyze occupancy trends
├─ Check revenue vs target
├─ Gather customer feedback
├─ Assess demand elasticity
├─ Re-run model dengan data terbaru
└─ Adjust tarif jika significant change detected
```

---

## 5.6 Challenges & Considerations

### 5.6.1 Potential Challenges

**1. Customer Resistance**
- Solusi: Gradual implementation, transparent communication

**2. Fairness Concerns**
- "Kenapa area A lebih mahal dari area B?"
- Solusi: Explain dengan data, buat educational materials

**3. Data Quality**
- Jika data tidak akurat, prediksi salah
- Solusi: Regular data audit, validation

**4. Unexpected Events**
- Holiday, weather, special events change demand
- Solusi: Incorporate seasonal factors, external data

### 5.6.2 External Factors Not in Model

**Factors yang dapat mempengaruhi tapi belum di-model:**
- Cuaca ekstrem
- Event khusus (konser, festival)
- Economic crisis
- Policy changes (PSBB, dll)

**Mitigation:**
- Keep model simple untuk robustness
- Manual override capability untuk exceptional cases
- Regular retraining dengan data baru

---

## 5.7 Case Study: Contoh Area Spesifik

### 5.7.1 Area Kategori RENDAH (Motor)

**Karakteristik Area:**
- Lokasi: Jalan tepi, area suburban
- Volume motor: 80-150/hari
- Durasi avg: 2-3 jam
- Akses: Kurang mudah

**Model Prediction:** RENDAH

**Analisis Historis:**
- Current tarif: Rp 2.000/jam
- Current occupancy: 35%
- Current revenue: Rp 12 juta/bulan
- Problem: Area under-utilized

**Tarif Ideal Proposed:**
- New tarif: Rp 1.000/jam
- Expected volume: +40% (demand elastic di low tariff)
- Expected occupancy: 50%
- Expected revenue: Rp 14.4 juta/bulan (+20%)

**Benefit:**
- Better utilization
- Slight revenue increase
- Customer satisfaction (cheaper parkir)

---

### 5.7.2 Area Kategori TINGGI (Mobil)

**Karakteristik Area:**
- Lokasi: Central business district
- Volume mobil: 400-700/hari
- Durasi avg: 4-8 jam
- Akses: Sangat mudah

**Model Prediction:** TINGGI

**Analisis Historis:**
- Current tarif: Rp 3.000/jam
- Current occupancy: 98%
- Current revenue: Rp 87 juta/bulan
- Problem: Oversupply, always full, customer complain

**Tarif Ideal Proposed:**
- New tarif: Rp 8.000/jam
- Expected volume: -25% (demand elastic di high tariff)
- Expected occupancy: 82%
- Expected revenue: Rp 154.8 juta/bulan (+78%)

**Benefit:**
- Control demand
- Increase accessibility (easier to find spot)
- Significant revenue increase
- Better spot turnover

---

## 5.8 Kesimpulan Pembangunan Tarif Ideal

**Ringkasan Proses:**

1. **Analisis** berbasis data historis (80:20 split training)
2. **Prediksi** menggunakan Random Forest dengan 150 trees
3. **Kategorisasi** area ke Rendah/Sedang/Tinggi
4. **Mapping** ke tarif ideal berbasis kategori
5. **Validasi** dengan data historis dan sensitivity analysis
6. **Implementasi** bertahap dengan monitoring KPI
7. **Iterasi** continuous berdasarkan hasil real-world

**Expected Outcomes:**
- Overall revenue increase: 50-100%
- Better parking accessibility
- Efficient utilization
- Sustainable growth

Dokumen ini menjelaskan secara lengkap bagaimana tarif ideal dibangun dari model prediksi dan bagaimana result diperoleh untuk pembahasan di laporan.
