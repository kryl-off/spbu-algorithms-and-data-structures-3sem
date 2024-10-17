import pandas as pd
import re
import numpy as np
def day(dt):
    day = dt.day
    return day
def get_class_of_route(x):
    pricing = {
        '1P': 100000,
        '1B': 31000,
        '1C': 21000,
        '2C': 8200,
        '2B': 5200,
        '2E': 6700,
        '1E': 32000,
        '2C': 5300,
        '1C': 1050,
        '1P': 2100,
        '1B': 101000,
        '2P': 2600,
        '2E': 1100,
        '3Э': 3600,
        '2Э': 4200,
        '1Б': 18500,
        '1Л': 11500,
        '1A': 8500,
        '1И': 8700
    }
    for key, value in pricing.items():
        if int(x)*10 == value: return key
def get_train_type(train_number):
    train_number = re.findall(r'\d+', train_number)
    train_number = int(' '.join(train_number))
    if 1 <= train_number <= 150:
        return "скорые поезда"
    elif 151 <= train_number <= 298:
        return "скорые поезда сезонного или разового назначения"
    elif 301 <= train_number <= 450:
        return "c"
    elif 451 <= train_number <= 598:
        return "пассажирские круглогодичные поезда"
    elif 701 <= train_number <= 750:
        return "пассажирские поезда сезонного или разового назначения"
    elif 751 <= train_number <= 788:
        return "скоростные поезда"
def get_bank_system(digit):
    digit_list = {
        'Mir': ['2202 48', '2200 47','2200 70','4154 94'],
        'MasterCard': ['5469 02','5536 91','4893 83','5211 78'],
        'Visa': ['4276 60','4377 77','4272 29','4154 94',]}
    for card_type, prefixes in digit_list.items():
        if digit in prefixes: return card_type
def calculate_k_anonymity(df, column_names):
    group_counts = df.groupby(column_names).size()
    k_anonymity = group_counts.min()
    top_5_bad_k = group_counts.nsmallest(5)
    print(f"Минимальное значение k-анонимности: {k_anonymity}")
    print("Топ-5 записей с минимальной k-анонимностью:")
    print(top_5_bad_k)
    return k_anonymity

df = pd.read_excel('../data/Tickets.xlsx')
orig_df = df.copy()
df['ФИО'] = df['ФИО'].apply(lambda x: f"{x[:1]}")
df['Паспорт'] = df['Паспорт'].apply(lambda x: f"XXXX XXXXXX")
df['Дата отъезда'] = pd.to_datetime(df['Дата отъезда'])
df['Дата приезда'] = pd.to_datetime(df['Дата приезда'])

df['Time'] = (df['Дата приезда'] - df['Дата отъезда']).dt.total_seconds() / 3600
df['Базовая стоимость'] = df['Стоимость'] / df['Time']

df['Класс'] = df['Базовая стоимость'].apply(lambda x : get_class_of_route(x))
df['Тип'] = df['Рейс'].apply(lambda x :get_train_type(x))

df['Дата отъезда'] = df['Дата отъезда'].apply(lambda x: day(x))
df['Дата приезда'] = df['Дата приезда'].apply(lambda x: day(x))
df['Карта оплаты'] = df['Карта оплаты'].apply(lambda x: get_bank_system(x[:7]))
df['Выбор вагона и места'] = df['Класс']
df['Рейс'] = df['Тип']

all = list(df.columns)

part = ['ФИО','Паспорт','Откуда','Куда','Дата отъезда','Рейс','Выбор вагона и места','Базовая стоимость','Карта оплаты']
calculate_k_anonymity(df, column_names=part)

def suppress_for_k_anonymity(df, quasi_identifiers, k):
    df_suppressed = df.copy()
    group_counts = df_suppressed.groupby(quasi_identifiers).size()
    underrepresented_groups = group_counts[group_counts < k].index
    suppressed_count = 0
    for group in underrepresented_groups:
        mask = np.ones(len(df_suppressed), dtype=bool)
        for col, val in zip(quasi_identifiers, group):
            mask &= df_suppressed[col] == val

        suppressed_count += mask.sum()
        df_suppressed.loc[mask, quasi_identifiers] = np.nan

    return df_suppressed, suppressed_count


df_suppressed, suppressed_count = suppress_for_k_anonymity(df, part, k=10)

print(suppressed_count)

calculate_k_anonymity(df_suppressed, column_names=part)

df.to_excel('../data/Tickets_anon.xlsx', index=False)


'''локальное обобщение - рейсы на короткие, средние и длинные, время по числу;

фио - исключаем. достаточно паспортных данных + пол

возмущение - цена, 

микро - агрегация - поезда по типу из тз; номера карт - по платежной системе;

выделить по времени следования время и по оффсетам посчитать класс -> сокращаем место до вагона и класса'''

