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
        if float(x)*10 == value: return key
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
def get_quasi_identifiers(data, quasi_identifiers):
    return list(map(lambda row: {key: row[key] for key in quasi_identifiers}, data))
def compare_datasets(original, anonymized, quasi_identifiers):
    original_unique = set(tuple(row.items()) for row in get_quasi_identifiers(original, quasi_identifiers))
    anonymized_unique = set(tuple(row.items()) for row in get_quasi_identifiers(anonymized, quasi_identifiers))
    return len(original_unique), len(anonymized_unique), len(anonymized_unique) / len(original_unique) * 100
def calculate_k_anonymity(df, column_names):
    group_counts = df.groupby(column_names).size()
    k_anonymity = group_counts.min()
    top_5_bad_k = group_counts.nsmallest(5)
    return k_anonymity, top_5_bad_k.tolist()
def suppress(df, quasi_identifiers, n):
    df_suppressed = df.copy()
    group_counts = df_suppressed.groupby(quasi_identifiers).size()
    group_counts_sorted = group_counts.sort_values()

    suppressed_count = 0
    for group, count in group_counts_sorted.items():
        mask = np.ones(len(df_suppressed), dtype=bool)
        for col, val in zip(quasi_identifiers, group):
            mask &= df_suppressed[col] == val

        group_size = mask.sum()

        if suppressed_count + group_size > n:
            rows_to_suppress = n - suppressed_count
            indices_to_suppress = df_suppressed.loc[mask].index[:rows_to_suppress]
            df_suppressed.loc[indices_to_suppress, quasi_identifiers] = np.nan
            suppressed_count += rows_to_suppress
            break
        else:
            df_suppressed.loc[mask, quasi_identifiers] = np.nan
            suppressed_count += group_size

        if suppressed_count >= n:
            break

    return df_suppressed, suppressed_count
def open_tickets(path):
    if path == "": path = '../data/Tickets.xlsx'
    df = pd.read_excel(path, engine='openpyxl')
    return df
def anonymise_tickets(path, outpath):
    if path == "": path = '../data/Tickets.xlsx'
    if outpath == "": outpath = '../data/Tickets_anon.xlsx'
    df = pd.read_excel(path)
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
    df['Стоимость'] = df['Базовая стоимость']
    return df








