import random
import faker
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


fake = faker.Faker('ru.RU')

with open('dictionary_p_male.txt') as file: m_surname = file.read().split()
with open('dictionary_p_female.txt') as file: f_surname = file.read().split()
with open('dictionary_fn_male.txt') as file: m_first_name = file.read().split()
with open('dictionary_fn_female.txt') as file: f_first_name = file.read().split()
with open('dictionary_ln_male.txt') as file: m_last_name = file.read().split()
with open('dictionary_ln_female.txt') as file: f_last_name = file.read().split()

initial_time = datetime(2024, 9, 21, 0, 0)
end_time = initial_time + relativedelta(days=1)

train_dictionary_df = pd.read_excel('trainsbook.xlsx')

ticket_data=[]
cards_array=[]

def bank_card(bank, bank_system):
    digit_list = {
        'Мир': {'Sber': '2202', 'T-Bank': '2200', 'VTB': '2204', 'Alfa': '2233', },
        'MasterCard': {'Sber': '5469', 'T-Bank': '5489', 'VTB': '5443', 'Alfa': '5477', },
        'Other': {'Sber': '4276', 'T-Bank': '4277', 'VTB': '4272', 'Alfa': '4282', }}
    if bank_system in digit_list:
        digit = digit_list[bank_system].get(bank,
            '2206' if bank_system == 'Mir' else '5406' if bank_system == 'MasterCard' else '4279')
    else:
        digit = '4279'
    args = {
        'd1': digit,
        'd2': str(random.randint(1000, 9999)),
        'd3': str(random.randint(1000, 9999)),
        'd4': str(random.randint(1000, 9999))}
    card_number = ('{d1} {d2} {d3} {d4}').format(**args)
    return card_number
    '''if cards_array.count(card_number) >= 5:
        return bank_card(bank, bank_system)
    else:
        cards_array.append(card_number.format(**args))
        return card_number'''
class Person:  #Генерация ФИО
    def __init__(self):
        self.banks = ['Sber', 'T-Bank', 'VTB', 'Alfa', 'HK']
        self.bank_system = ['Visa', 'MasterCard', 'Mir']
        if (random.randint(1, 2) == 1):
            self.name = random.choice(m_last_name) + ' ' + random.choice(m_first_name) + ' ' + random.choice(m_surname)
        else:
            self.name = random.choice(f_last_name) + ' ' + random.choice(f_first_name) + ' ' + random.choice(f_surname)

        self.card = bank_card(random.choice(self.banks),random.choice(self.bank_system))
        self.passport = f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"
class Vagon:
    def __init__(self, type):
        self.vagon_data = {
            #a) Поезда «Сапсан»
            'a_1': {'size': 1, 'price': 100000, 'naming': '1P'}, # (1) 1Р — купе-переговорная, продаётся только целиком
            'a_2': {'size': 14, 'price': 30000, 'naming': '1B'}, # (2) 1В — просто места в вагоне 1 класса, без переговорной
            'a_3': {'size': 30, 'price': 20000, 'naming': '1C'}, # (3) 1С — вагон бизнес-класса
            'a_4': {'size': 40, 'price': 8000, 'naming': '2C'}, # (4) 2С — сидячий вагон эконом-класса
            'a_5': {'size': 50, 'price': 5000, 'naming': '2B'}, # 5) 2В — класс «Экономический+» (вагон № 10 и № 20)
            'a_6': {'size': 12, 'price': 6500, 'naming': '2E'}, # (6) 2E — места в вагоне-бистро
            # b) Поезда «Стриж»
            'b_1': {'size': 16, 'price': 30000, 'naming': '1E'}, # (1) 1Е — СВ (VIP). Продаётся купе целиком, в нём могут ехать 1 или 2 пассажира.
            'b_2': {'size': 40, 'price': 12000, 'naming': '1P'}, # (2) 1Р — сидячие вагоны 1 класса.
            'b_3': {'size': 50, 'price': 5000, 'naming': '2C'}, # (3) 2С — сидячие вагоны 2 класса.
            # c) Сидячий вагон
            'c_1': {'size': 81, 'price': 1000, 'naming': '1C'}, # (1) 1С - обычные сидячие места
            'c_2': {'size': 36, 'price': 2000, 'naming': '1P'}, # (2) 1Р — в двухэтажном сидячем вагоне так маркируются места в купе
            'c_3': {'size': 1, 'price': 100000, 'naming': '1B'}, # (3) 1В — вагон с индивидуальным размещением, то есть выкупаются все места.
            'c_4': {'size': 81, 'price': 2500, 'naming': '2P'}, # (4) 2Р — вагон повышенной комфортности
            'c_5': {'size': 81, 'price': 1000, 'naming': '2E'}, # (5) 2Е — сидячий вагон
            # d) Плацкартные вагоны
            'd_1': {'size': 54, 'price': 3500, 'naming': '3Э'}, # (1) 3Э — плацкартный вагон
            # e) Купе
            'e_1': {'size': 36, 'price': 4000, 'naming': '2Э'}, # (1) 2Э — кондиционируемый вагон повышенной комфортности с 4-местными купе.
            # f) Люкс (СВ)
            'f_1': {'size': 18, 'price': 18000, 'naming': '1Б'}, # (1) 1Б — бизнес-класс.
            'f_2': {'size': 18, 'price': 11000, 'naming': '1Л'}, # (2) 1Л — вагон СВ.
            # g) Мягкий вагон
            'g_1': {'size': 16, 'price': 8000, 'naming': '1A'}, # (1) 1А — вагон состоит из 4 купе и салона-бара.
            'g_2': {'size': 16, 'price': 8000, 'naming': '1И'} # (1) 1А — вагон состоит из 4 купе и салона-бара.
        }

        if type in self.vagon_data:
            data = self.vagon_data[type]
            self.size = data['size']
            self.price = data['price']
            self.naming = data['naming']
        else:
            raise ValueError("Неизвестный тип вагона")
class Route:#предположим, с одним номером существует один состав, курсирующий туда-обратно с дельтой в 2-8 часов. на каждое отправление продаются билеты #класс получает порядковый номер номер поезда в словаре
    def __init__(self, number):
        self.number = train_dictionary_df.iloc[number, 0]
        self.type = str(train_dictionary_df.iloc[number, 1])
        self.original = train_dictionary_df.iloc[number, 2]
        self.destination = train_dictionary_df.iloc[number, 3]
        self.roadtime = int(train_dictionary_df.iloc[number, 4])
        self.delta = relativedelta(minutes=random.randint(120,480))
        self.position = initial_time + relativedelta(minutes=random.randint(1,111))
        self.destination_time = self.position + relativedelta(hours=self.roadtime)
        self.train_data = {
            'a': {
                'a_1': 0, 'a_2': 0, 'a_3': 0, 'a_4': 0, 'a_5': 0, 'a_6': 0,
                'b_1': 0, 'b_2': 0, 'b_3': 0, 'c_1': 1, 'c_2': 0, 'c_3': 0,
                'c_4': 0, 'c_5': 0, 'd_1': 7, 'e_1': 5, 'f_1': 1, 'f_2': 1,
                'g_1': 0, 'g_2': 0
            },
            'b': {
                'a_1': 0, 'a_2': 0, 'a_3': 0, 'a_4': 0, 'a_5': 0, 'a_6': 0,
                'b_1': 0, 'b_2': 0, 'b_3': 0, 'c_1': 2, 'c_2': 0, 'c_3': 0,
                'c_4': 0, 'c_5': 0, 'd_1': 7, 'e_1': 5, 'f_1': 1, 'f_2': 1,
                'g_1': 0, 'g_2': 0
            },
            'c': {
                'a_1': 0, 'a_2': 0, 'a_3': 0, 'a_4': 0, 'a_5': 0, 'a_6': 0,
                'b_1': 0, 'b_2': 0, 'b_3': 0, 'c_1': 2, 'c_2': 0, 'c_3': 0,
                'c_4': 0, 'c_5': 0, 'd_1': 8, 'e_1': 6, 'f_1': 1, 'f_2': 0,
                'g_1': 0, 'g_2': 0
            },
            'd': {
                'a_1': 0, 'a_2': 0, 'a_3': 0, 'a_4': 0, 'a_5': 0, 'a_6': 0,
                'b_1': 0, 'b_2': 0, 'b_3': 0, 'c_1': 0, 'c_2': 0, 'c_3': 0,
                'c_4': 0, 'c_5': 2, 'd_1': 7, 'e_1': 7, 'f_1': 1, 'f_2': 1,
                'g_1': 0, 'g_2': 0
            },
            'e': {
                'a_1': 0, 'a_2': 0, 'a_3': 0, 'a_4': 0, 'a_5': 0, 'a_6': 0,
                'b_1': 0, 'b_2': 0, 'b_3': 0, 'c_1': 1, 'c_2': 0, 'c_3': 0,
                'c_4': 2, 'c_5': 10, 'd_1': 0, 'e_1': 1, 'f_1': 1, 'f_2': 0,
                'g_1': 0, 'g_2': 0
            },
            'sapsan': {
                'a_1': 1, 'a_2': 1, 'a_3': 3, 'a_4': 9, 'a_5': 0, 'a_6': 1,
                'b_1': 0, 'b_2': 0, 'b_3': 0, 'c_1': 0, 'c_2': 0, 'c_3': 0,
                'c_4': 0, 'c_5': 0, 'd_1': 0, 'e_1': 0, 'f_1': 0, 'f_2': 0,
                'g_1': 0, 'g_2': 0
            },
            'strige': {
                'a_1': 0, 'a_2': 0, 'a_3': 0, 'a_4': 0, 'a_5': 0, 'a_6': 0,
                'b_1': 3, 'b_2': 5, 'b_3': 7, 'c_1': 0, 'c_2': 0, 'c_3': 0,
                'c_4': 0, 'c_5': 0, 'd_1': 0, 'e_1': 0, 'f_1': 0, 'f_2': 0,
                'g_1': 0, 'g_2': 0
            },
            'neva': {
                'a_1': 0, 'a_2': 0, 'a_3': 0, 'a_4': 0, 'a_5': 0, 'a_6': 0,
                'b_1': 0, 'b_2': 0, 'b_3': 0, 'c_1': 2, 'c_2': 0, 'c_3': 0,
                'c_4': 4, 'c_5': 4, 'd_1': 0, 'e_1': 0, 'f_1': 1, 'f_2': 1,
                'g_1': 0, 'g_2': 0
            }}

        self.boarding()
    def swap(self):
        self.position += self.delta
        self.destination_time = self.position + relativedelta(hours=self.roadtime)
        temp = self.destination
        self.destination = self.original
        self.original = temp
        self.boarding()
    def boarding(self): #рассаживаем
        vag_number = 0
        if self.type in self.train_data:
            for key,value in self.train_data[self.type].items():
                for i in range(0, value):
                    v = Vagon(key)
                    vag_number += 1
                    for l in range(0, v.size):
                        man = Person()
                        ticket_data.append({
                            "ФИО": man.name,
                            "Паспорт": man.passport,
                            "Откуда": self.original,
                            "Куда": self.destination,
                            "Дата отъезда": self.position.strftime("%Y-%m-%dT%H:%M"),
                            "Дата приезда": self.destination_time.strftime("%Y-%m-%dT%H:%M"),
                            "Рейс": self.number,
                            "Выбор вагона и места": str(vag_number) + '-' + str(l+1),
                            "Стоимость": str(((v.price//10)*(self.roadtime)))+' руб',
                            "Карта оплаты": man.card
                        })
for n in range(1,len(train_dictionary_df)):
    train = Route(n)
    while (train.position < end_time):
        train.swap() #

# Создание DataFrame из списка данных
df = pd.DataFrame(ticket_data)
#Запись в Excel таблицу
df.to_excel('Tickets.xlsx', index=False)

















