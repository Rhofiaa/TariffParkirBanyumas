#!/usr/bin/env python3
import json
import os

# Notebook content
notebook_data = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🚗 SISTEM PREDIKSI TARIF PARKIR PROGRESIF DENGAN RANDOM FOREST\n",
                "\n",
                "**Tujuan**: Mengembangkan model machine learning untuk memprediksi klasifikasi potensi tarif parkir.\n",
                "\n",
                "**Data**: DataParkir_Fix.xlsx (407 lokasi parkir)\n",
                "\n",
                "**Section Order**: Data Processing → Feature Engineering → Model Training → Evaluation → Spatial Analysis → Interactive Simulation → Export\n",
                "\n",
                "---"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 1: SETUP & IMPORT LIBRARIES"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "from sklearn.model_selection import train_test_split\n",
                "from sklearn.preprocessing import LabelEncoder\n",
                "from sklearn.ensemble import RandomForestClassifier\n",
                "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix\n",
                "from sklearn.tree import plot_tree\n",
                "import seaborn as sns\n",
                "import matplotlib.pyplot as plt\n",
                "import re, datetime, folium\n",
                "\n",
                "print('✓ Semua libraries berhasil diimport')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 2: LOAD DATA"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('='*100)\n",
                "print('[STEP 1] LOAD DATA')\n",
                "print('='*100)\n",
                "\n",
                "file_path = 'DataParkir_Fix.xlsx'\n",
                "df = pd.read_excel(file_path)\n",
                "\n",
                "print(f'\\n✓ Data berhasil dimuat dari: {file_path}')\n",
                "print(f'  Shape: {df.shape} (baris, kolom)')\n",
                "print(f'\\nPreview Data (5 baris pertama):')\n",
                "print(df.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 3-4: FUNGSI HELPER & DATA SETUP"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Mapping Tarif Dasar\n",
                "tarif_mapping = {\n",
                "    'Motor': {'Rendah': 1000, 'Sedang': 2000, 'Tinggi': 3000},\n",
                "    'Mobil': {'Rendah': 3000, 'Sedang': 4000, 'Tinggi': 5000}\n",
                "}\n",
                "\n",
                "def konversi_jam(x):\n",
                "    '''Mengubah format jam ke desimal'''\n",
                "    if pd.isna(x) or str(x).strip() == '-':\n",
                "        return np.nan\n",
                "    s = str(x).strip()\n",
                "    parts = s.split('-')\n",
                "    start_str = parts[0]\n",
                "    end_str = parts[1] if len(parts) > 1 else parts[0]\n",
                "    \n",
                "    def to_minutes(time_str):\n",
                "        time_str = time_str.replace('.', ':')\n",
                "        h, m = 0, 0\n",
                "        try:\n",
                "            if ':' in time_str:\n",
                "                h, m = map(int, time_str.split(':'))\n",
                "            else:\n",
                "                h = int(time_str)\n",
                "        except ValueError:\n",
                "            return 0\n",
                "        return h * 60 + m\n",
                "    \n",
                "    start_min = to_minutes(start_str)\n",
                "    end_min = to_minutes(end_str)\n",
                "    avg_min = (start_min + end_min) / 2\n",
                "    return (avg_min / 60)\n",
                "\n",
                "def kategori_jam_otomatis(jam):\n",
                "    if (jam <= 6) or (jam >= 22):\n",
                "        return 'Sepi'\n",
                "    elif (jam > 8 and jam <= 19):\n",
                "        return 'Ramai'\n",
                "    else:\n",
                "        return 'Sedang'\n",
                "\n",
                "def calculate_progresif_tarif(jenis, potensi_class, jam_desimal):\n",
                "    tarif_dasar = tarif_mapping[jenis].get(potensi_class, 0)\n",
                "    if jam_desimal > 9.0:\n",
                "        if potensi_class == 'Tinggi':\n",
                "            return tarif_dasar + 1000\n",
                "        elif potensi_class == 'Sedang':\n",
                "            return tarif_dasar + 500\n",
                "    return tarif_dasar\n",
                "\n",
                "print('✓ Fungsi helper berhasil dibuat')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 5: DATA CLEANING"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df_clean = df.copy()\n",
                "\n",
                "pend_cols = [\n",
                "    'Pendapatan Tarif Parkir Weekday Motor per tahun',\n",
                "    'Pendapatan Tarif Parkir Weekday Mobil per tahun',\n",
                "    'Pendapatan Tarif Parkir Weekend Motor per tahun',\n",
                "    'Pendapatan Tarif Parkir Weekend Mobil per tahun'\n",
                "]\n",
                "\n",
                "print('[5.1] Membersihkan kolom Pendapatan...')\n",
                "for c in pend_cols:\n",
                "    if c in df_clean.columns:\n",
                "        df_clean[c] = df_clean[c].astype(str).str.replace(r'[^\\\\d,\\\\.]', '', regex=True)\n",
                "        df_clean[c] = df_clean[c].str.replace('.', '', regex=False)\n",
                "        df_clean[c] = df_clean[c].str.replace(',', '.', regex=False)\n",
                "        df_clean[c] = pd.to_numeric(df_clean[c], errors='coerce').fillna(0)\n",
                "\n",
                "print('✓ Kolom Pendapatan dibersihkan')\n",
                "\n",
                "print('[5.2] Mengkonversi kolom Jam...')\n",
                "jam_cols = [c for c in df_clean.columns if 'Jam' in c and 'per tahun' not in c]\n",
                "for col in jam_cols:\n",
                "    df_clean[col] = df_clean[col].apply(konversi_jam)\n",
                "    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())\n",
                "\n",
                "print(f'✓ {len(jam_cols)} kolom Jam berhasil dikonversi')\n",
                "\n",
                "print('[5.3] Handle Missing Values...')\n",
                "for col in df_clean.columns:\n",
                "    if df_clean[col].dtype != 'object':\n",
                "        df_clean[col] = df_clean[col].fillna(df_clean[col].median())\n",
                "    else:\n",
                "        if df_clean[col].isnull().any():\n",
                "            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else 'Unknown')\n",
                "\n",
                "print(f'✓ Data setelah pembersihan: {df_clean.shape[0]} baris')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 6: FEATURE ENGINEERING"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('[6.1] Menghitung Total Pendapatan...')\n",
                "motor_pend_cols = [c for c in pend_cols if 'Motor' in c]\n",
                "mobil_pend_cols = [c for c in pend_cols if 'Mobil' in c]\n",
                "\n",
                "df_clean['Total_Pendapatan_Tahun'] = df_clean[pend_cols].sum(axis=1)\n",
                "df_clean['Total_Pend_Motor'] = df_clean[motor_pend_cols].sum(axis=1)\n",
                "df_clean['Total_Pend_Mobil'] = df_clean[mobil_pend_cols].sum(axis=1)\n",
                "\n",
                "print('[6.2] Klasifikasi Potensi Tarif...')\n",
                "try:\n",
                "    df_clean['Class_Motor'] = pd.qcut(df_clean['Total_Pend_Motor'], q=3, labels=['Rendah','Sedang','Tinggi'])\n",
                "    df_clean['Class_Mobil'] = pd.qcut(df_clean['Total_Pend_Mobil'], q=3, labels=['Rendah','Sedang','Tinggi'])\n",
                "except ValueError:\n",
                "    df_clean['Class_Motor'] = pd.cut(df_clean['Total_Pend_Motor'], \n",
                "                                      bins=[-np.inf, df_clean['Total_Pend_Motor'].quantile(0.5), np.inf], \n",
                "                                      labels=['Rendah', 'Tinggi']).fillna('Rendah')\n",
                "    df_clean['Class_Mobil'] = pd.cut(df_clean['Total_Pend_Mobil'], \n",
                "                                      bins=[-np.inf, df_clean['Total_Pend_Mobil'].quantile(0.5), np.inf], \n",
                "                                      labels=['Rendah', 'Tinggi']).fillna('Rendah')\n",
                "\n",
                "print('✓ Klasifikasi berhasil dibuat')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 7: MODEL TRAINING"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fitur_motor = ['Jumlah Motor Weekday', 'Jumlah Motor Weekend'] + [c for c in jam_cols if 'Motor' in c]\n",
                "fitur_mobil = ['Jumlah Mobil Weekday', 'Jumlah Mobil Weekend'] + [c for c in jam_cols if 'Mobil' in c]\n",
                "\n",
                "def build_model(X, y):\n",
                "    le = LabelEncoder()\n",
                "    if len(y.unique()) > 1:\n",
                "        y_enc = le.fit_transform(y)\n",
                "    else:\n",
                "        y_enc = y\n",
                "    \n",
                "    if len(y.unique()) > 1 and all(y.value_counts() > 1):\n",
                "        X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)\n",
                "    else:\n",
                "        X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)\n",
                "    \n",
                "    if X_train.empty:\n",
                "        return None, le, pd.DataFrame(), pd.DataFrame(), np.array([]), np.array([]), np.array([]), pd.DataFrame(), {}, {}\n",
                "    \n",
                "    model = RandomForestClassifier(n_estimators=150, max_depth=15, min_samples_leaf=3, random_state=42)\n",
                "    model.fit(X_train, y_train)\n",
                "    y_pred = model.predict(X_test)\n",
                "    \n",
                "    return model, le, X_train, X_test, y_train, y_test, y_pred, X_train, {}, {}\n",
                "\n",
                "print('=== TRAINING MODEL (RANDOM FOREST) ===')\n",
                "model_motor, le_motor, X_train_m, X_test_m, y_train_m, y_test_m, y_pred_m, _, _, _ = build_model(\n",
                "    df_clean[fitur_motor], df_clean['Class_Motor']\n",
                ")\n",
                "model_mobil, le_mobil, X_train_c, X_test_c, y_train_c, y_test_c, y_pred_c, _, _, _ = build_model(\n",
                "    df_clean[fitur_mobil], df_clean['Class_Mobil']\n",
                ")\n",
                "\n",
                "print(f'[Motor] Total: {len(df_clean)} | Training: {len(X_train_m)} | Testing: {len(X_test_m)}')\n",
                "print(f'✓ Model Motor training selesai!')\n",
                "print(f'[Mobil] Total: {len(df_clean)} | Training: {len(X_train_c)} | Testing: {len(X_test_c)}')\n",
                "print(f'✓ Model Mobil training selesai!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 8: MODEL EVALUATION"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('=== EVALUASI MODEL ===')\n",
                "\n",
                "y_pred_train_m = model_motor.predict(X_train_m)\n",
                "y_pred_test_m = model_motor.predict(X_test_m)\n",
                "train_acc_m = accuracy_score(y_train_m, y_pred_train_m)\n",
                "test_acc_m = accuracy_score(y_test_m, y_pred_test_m)\n",
                "\n",
                "print(f'\\\\nMOTOR:')\n",
                "print(f'  Akurasi Training: {train_acc_m:.4f} ({train_acc_m*100:.2f}%)')\n",
                "print(f'  Akurasi Testing : {test_acc_m:.4f} ({test_acc_m*100:.2f}%)')\n",
                "print(f'  Overfitting Gap : {(train_acc_m - test_acc_m)*100:.2f}%')\n",
                "\n",
                "y_pred_train_c = model_mobil.predict(X_train_c)\n",
                "y_pred_test_c = model_mobil.predict(X_test_c)\n",
                "train_acc_c = accuracy_score(y_train_c, y_pred_train_c)\n",
                "test_acc_c = accuracy_score(y_test_c, y_pred_test_c)\n",
                "\n",
                "print(f'\\\\nMOBIL:')\n",
                "print(f'  Akurasi Training: {train_acc_c:.4f} ({train_acc_c*100:.2f}%)')\n",
                "print(f'  Akurasi Testing : {test_acc_c:.4f} ({test_acc_c*100:.2f}%)')\n",
                "print(f'  Overfitting Gap : {(train_acc_c - test_acc_c)*100:.2f}%')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 9: FEATURE IMPORTANCE"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('=== FEATURE IMPORTANCE ===')\n",
                "\n",
                "importance_motor = pd.DataFrame({\n",
                "    'Fitur': fitur_motor,\n",
                "    'Importance': model_motor.feature_importances_\n",
                "}).sort_values(by='Importance', ascending=False)\n",
                "\n",
                "importance_mobil = pd.DataFrame({\n",
                "    'Fitur': fitur_mobil,\n",
                "    'Importance': model_mobil.feature_importances_\n",
                "}).sort_values(by='Importance', ascending=False)\n",
                "\n",
                "print('\\\\nMOTOR Top 5:')\n",
                "print(importance_motor.head())\n",
                "print('\\\\nMOBIL Top 5:')\n",
                "print(importance_mobil.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 10: SPATIAL ANALYSIS WITH FOLIUM MAP"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('\\\\n[STEP 11A] ANALISIS SPASIAL DENGAN PETA INTERAKTIF')\n",
                "\n",
                "# Prediksi untuk semua data\n",
                "y_pred_m_enc = model_motor.predict(df_clean[fitur_motor])\n",
                "df_clean['Klasifikasi Potensi (Motor)'] = le_motor.inverse_transform(y_pred_m_enc)\n",
                "\n",
                "y_pred_c_enc = model_mobil.predict(df_clean[fitur_mobil])\n",
                "df_clean['Klasifikasi Potensi (Mobil)'] = le_mobil.inverse_transform(y_pred_c_enc)\n",
                "\n",
                "# Buat peta\n",
                "map_center = [df_clean['Latitude'].mean(), df_clean['Longitude'].mean()]\n",
                "m = folium.Map(location=map_center, zoom_start=13, tiles='OpenStreetMap')\n",
                "\n",
                "color_mapping = {\n",
                "    'Rendah': '#FFA500',   # Orange\n",
                "    'Sedang': '#FFD700',   # Gold\n",
                "    'Tinggi': '#FF6347'    # Red\n",
                "}\n",
                "\n",
                "fg_motor = folium.FeatureGroup(name='Motor (Potensi Tarif)', show=True)\n",
                "fg_mobil = folium.FeatureGroup(name='Mobil (Potensi Tarif)', show=True)\n",
                "\n",
                "for index, row in df_clean.iterrows():\n",
                "    titik = row['Titik']\n",
                "    lat, lon = row['Latitude'], row['Longitude']\n",
                "    motor_class = row['Klasifikasi Potensi (Motor)']\n",
                "    mobil_class = row['Klasifikasi Potensi (Mobil)']\n",
                "    motor_tarif = tarif_mapping['Motor'].get(motor_class, 0)\n",
                "    mobil_tarif = tarif_mapping['Mobil'].get(mobil_class, 0)\n",
                "    \n",
                "    folium.CircleMarker(\n",
                "        location=[lat, lon],\n",
                "        radius=6,\n",
                "        color=color_mapping.get(motor_class, '#808080'),\n",
                "        fill=True,\n",
                "        fill_color=color_mapping.get(motor_class, '#808080'),\n",
                "        fill_opacity=0.8,\n",
                "        popup=f'{titik} (Motor: {motor_class}, Rp{motor_tarif}/jam)',\n",
                "        tooltip=f'{titik}'\n",
                "    ).add_to(fg_motor)\n",
                "    \n",
                "    folium.CircleMarker(\n",
                "        location=[lat, lon],\n",
                "        radius=6,\n",
                "        color=color_mapping.get(mobil_class, '#808080'),\n",
                "        fill=True,\n",
                "        fill_color=color_mapping.get(mobil_class, '#808080'),\n",
                "        fill_opacity=0.8,\n",
                "        popup=f'{titik} (Mobil: {mobil_class}, Rp{mobil_tarif}/jam)',\n",
                "        tooltip=f'{titik}'\n",
                "    ).add_to(fg_mobil)\n",
                "\n",
                "fg_motor.add_to(m)\n",
                "fg_mobil.add_to(m)\n",
                "folium.LayerControl(collapsed=False).add_to(m)\n",
                "\n",
                "m.save('peta_potensi_tarif_parkir.html')\n",
                "print(f'✓ Peta interaktif disimpan: peta_potensi_tarif_parkir.html')\n",
                "print(f'✓ Total lokasi parkir: {len(df_clean)}')\n",
                "m"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 11: INTERACTIVE PREDICTION SIMULATION"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('[STEP 12] SIMULASI PREDIKSI INTERAKTIF')\n",
                "print('Masukkan pilihan: 1 untuk Motor, 2 untuk Mobil')\n",
                "print('Atau tekan Ctrl+C untuk selesai')\n",
                "\n",
                "# Contoh simulasi sederhana\n",
                "print('\\\\n=== CONTOH SIMULASI ===')\n",
                "jenis = 'Motor'\n",
                "model = model_motor\n",
                "le = le_motor\n",
                "fitur = fitur_motor\n",
                "X_train = X_train_m\n",
                "\n",
                "jumlah_weekday = 100\n",
                "jumlah_weekend = 80\n",
                "jam_input = 17.5\n",
                "kategori_jam = kategori_jam_otomatis(jam_input)\n",
                "\n",
                "data_baru = pd.DataFrame([X_train.mean()], columns=X_train.columns)\n",
                "data_baru[f'Jumlah {jenis} Weekday'] = jumlah_weekday\n",
                "data_baru[f'Jumlah {jenis} Weekend'] = jumlah_weekend\n",
                "\n",
                "pred_encoded = model.predict(data_baru)[0]\n",
                "pred_class = le.inverse_transform([pred_encoded])[0]\n",
                "proba = model.predict_proba(data_baru)[0]\n",
                "confidence = proba[pred_encoded]\n",
                "\n",
                "tarif_base = tarif_mapping[jenis][pred_class]\n",
                "tarif_progresif = calculate_progresif_tarif(jenis, pred_class, jam_input)\n",
                "\n",
                "print(f'\\\\n📊 INPUT:')\n",
                "print(f'  Jenis: {jenis}')\n",
                "print(f'  Jumlah Weekday: {jumlah_weekday} unit')\n",
                "print(f'  Jumlah Weekend: {jumlah_weekend} unit')\n",
                "print(f'  Jam Puncak: {jam_input:.2f} (Kategori: {kategori_jam})')\n",
                "print(f'\\\\n🎯 PREDIKSI:')\n",
                "print(f'  Klasifikasi: {pred_class.upper()}')\n",
                "print(f'  Confidence: {confidence*100:.2f}%')\n",
                "print(f'\\\\n💰 REKOMENDASI TARIF:')\n",
                "print(f'  Tarif Dasar: Rp{tarif_base:,.0f} / jam')\n",
                "print(f'  Tarif Progresif: Rp{tarif_progresif:,.0f} / jam')\n",
                "print(f'  Selisih: Rp{tarif_progresif - tarif_base:,.0f} / jam')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## SECTION 12: EXPORT & SUMMARY"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('[STEP 13] RINGKASAN FINAL & EXPORT DATA')\n",
                "\n",
                "kolom_output = [\n",
                "    'Titik',\n",
                "    'Latitude',\n",
                "    'Longitude',\n",
                "    'Klasifikasi Potensi (Motor)',\n",
                "    'Klasifikasi Potensi (Mobil)'\n",
                "]\n",
                "\n",
                "df_rekomendasi = df_clean[kolom_output].copy()\n",
                "df_rekomendasi.to_excel('Tabel_Rekomendasi_Tarif_Parkir.xlsx', index=False)\n",
                "\n",
                "print('\\\\n=== RINGKASAN 10 BARIS PERTAMA ===')\n",
                "print(df_rekomendasi.head(10).to_string())\n",
                "print('\\\\n✓ Hasil disimpan ke: Tabel_Rekomendasi_Tarif_Parkir.xlsx')\n",
                "\n",
                "summary = pd.DataFrame({\n",
                "    'Metrik': ['Total Data', 'Training', 'Testing', 'Fitur Motor', 'Fitur Mobil', 'Model', 'N Trees', 'Max Depth', 'Min Samples'],\n",
                "    'Nilai': [len(df_clean), len(X_train_m), len(X_test_m), len(fitur_motor), len(fitur_mobil), 'RandomForest', 150, 15, 3]\n",
                "})\n",
                "\n",
                "print('\\\\n=== SUMMARY ===')\n",
                "print(summary.to_string(index=False))\n",
                "\n",
                "print('\\\\n' + '='*100)\n",
                "print('✓✓✓ SIMULASI LENGKAP SELESAI ✓✓✓')\n",
                "print('='*100)\n",
                "print(f'''\n",
                "FILE YANG DIHASILKAN:\n",
                "1. Tabel_Rekomendasi_Tarif_Parkir.xlsx\n",
                "2. peta_potensi_tarif_parkir.html\n",
                "\n",
                "SECTION ORDER (BENAR):\n",
                "1-9. Data Processing, Cleaning, Feature Engineering, Training\n",
                "10. SPATIAL ANALYSIS (Folium Map)\n",
                "11. INTERACTIVE SIMULATION (Prediksi Interaktif)\n",
                "12. EXPORT & SUMMARY\n",
                "\n",
                "Ready untuk Google Colab!\n",
                "''')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.9.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write notebook
output_path = 'simulasi_colab.ipynb'
with open(output_path, 'w') as f:
    json.dump(notebook_data, f, indent=1)

print(f"✓ Notebook created: {output_path}")
print(f"✓ File size: {os.path.getsize(output_path)} bytes")
