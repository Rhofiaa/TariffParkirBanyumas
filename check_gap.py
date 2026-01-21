import pandas as pd

df = pd.read_excel('DataParkir_Fix.xlsx')
df_clean = df.dropna(subset=['Titik'])
print('Total data:', len(df_clean))

# Hitung distribusi motor dan mobil
total_motor = df_clean['Pendapatan Tarif Parkir Weekday Motor per tahun'] + df_clean['Pendapatan Tarif Parkir Weekend Motor per tahun']
total_mobil = df_clean['Pendapatan Tarif Parkir Weekday Mobil per tahun'] + df_clean['Pendapatan Tarif Parkir Weekend Mobil per tahun']

try:
    motor_class = pd.qcut(total_motor, q=3, labels=['Rendah','Sedang','Tinggi'], duplicates='drop')
    print('\nMotor distribution:')
    print(motor_class.value_counts().sort_index())
    print('Total motor classes:', motor_class.nunique())
except Exception as e:
    print('Motor class error:', e)

try:
    mobil_class = pd.qcut(total_mobil, q=3, labels=['Rendah','Sedang','Tinggi'], duplicates='drop')
    print('\nMobil distribution:')
    print(mobil_class.value_counts().sort_index())
    print('Total mobil classes:', mobil_class.nunique())
except Exception as e:
    print('Mobil class error:', e)

# Hitung train-test split
print('\nTrain-test split (80-20):')
train_size = int(len(df_clean) * 0.8)
test_size = len(df_clean) - train_size
print(f'Train: {train_size}, Test: {test_size}')
