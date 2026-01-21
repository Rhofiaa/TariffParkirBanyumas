import pandas as pd

df = pd.read_excel('DataParkir_Fix.xlsx')
weekday_mobil = df['Pendapatan Tarif Parkir Weekday Mobil per tahun']
weekend_mobil = df['Pendapatan Tarif Parkir Weekend Mobil per tahun']

print("Tipe Weekday Mobil:", weekday_mobil.dtype)
print("Tipe Weekend Mobil:", weekend_mobil.dtype)

# Hitung total
total_mobil = weekday_mobil + weekend_mobil
print("\nTotal Mobil:")
print("Min:", total_mobil.min())
print("Max:", total_mobil.max())
print("Mean:", total_mobil.mean())

# Cek NaN
print("\nNaN count:")
print("Weekday NaN:", weekday_mobil.isna().sum())
print("Weekend NaN:", weekend_mobil.isna().sum())
