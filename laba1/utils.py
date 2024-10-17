import random
import tkinter as tk
from dateutil.relativedelta import relativedelta



with open('../data/dictionary_p_male.txt') as file: m_surname = file.read().split()
with open('../data/dictionary_p_female.txt') as file: f_surname = file.read().split()
with open('../data/dictionary_fn_male.txt') as file: m_first_name = file.read().split()
with open('../data/dictionary_fn_female.txt') as file: f_first_name = file.read().split()
with open('../data/dictionary_ln_male.txt') as file: m_last_name = file.read().split()
with open('../data/dictionary_ln_female.txt') as file: f_last_name = file.read().split()

def bank_card(bank_system_probability, bank_probability):
    digit_list = {
        'Mir': {'Sber': '2202 48', 'T-Bank': '2200 47', 'VTB': '2200 70', 'Alfa': '4154 94', },
        'MasterCard': {'Sber': '5469 02', 'T-Bank': '5536 91', 'VTB': '4893 83', 'Alfa': '5211 78', },
        'Visa': {'Sber': '4276 60', 'T-Bank': '4377 77', 'VTB': '4272 29', 'Alfa': '4154 94', }
    }
    banks = ['Sber', 'T-Bank', 'VTB', 'Alfa']
    bank_systems = ['Mir', 'MasterCard', 'Visa']
    if bank_system_probability == []:
        bank_system_probability = [1, 1, 1] # По умолчанию равные
    if bank_probability == []:
        bank_probability = [1, 1, 1, 1]  # По умолчанию равные

    bank = random.choices(banks, weights=bank_probability, k=1)[0] #Выбор банка с учетом вероятности
    bank_system = random.choices(bank_systems, weights=bank_system_probability, k=1)[0]  # Выбор system с учетов вероятности

    if bank_system in digit_list:
        digit = digit_list[bank_system][bank]

    args = {
        'd1': digit,
        'd2': str(random.randint(1000, 9999)),
        'd3': str(random.randint(1000, 9999)),
        'd4': str(random.randint(1000, 9999))
    }

    card_number = ('{d1} {d2} {d3} {d4}').format(**args)
    return card_number
    '''if cards_array.count(card_number) >= 5:
        return bank_card(bank, bank_system)
    else:
        cards_array.append(card_number.format(**args))
        return card_number'''

class Route:#предположим, с одним номером существует один состав, курсирующий туда-обратно с дельтой в 2-8 часов. на каждое отправление продаются билеты #класс получает порядковый номер номер поезда в словаре
    def __init__(self, number,train_dictionary_df,initial_time, ticket_data,sys_prob, bank_prob):
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

        self.boarding(ticket_data,sys_prob, bank_prob)
    def swap(self, ticket_data,sys_prob, bank_prob):
        self.position += self.delta
        self.destination_time = self.position + relativedelta(hours=self.roadtime)
        temp = self.destination
        self.destination = self.original
        self.original = temp
        self.boarding(ticket_data,sys_prob, bank_prob)
    def boarding(self, ticket_data,sys_prob, bank_prob): #рассаживаем
        vag_number = 0
        if self.type in self.train_data:
            for key,value in self.train_data[self.type].items():
                for i in range(0, value):
                    v = Vagon(key)
                    vag_number += 1
                    for l in range(0, v.size):
                        man = Person(sys_prob, bank_prob)
                        ticket_data.append({
                            "ФИО": man.name,
                            "Паспорт": man.passport,
                            "Откуда": self.original,
                            "Куда": self.destination,
                            "Дата отъезда": self.position,
                            "Дата приезда": self.destination_time, #"%Y-%m-%dT%H:%M"
                            "Рейс": self.number,
                            "Выбор вагона и места": str(vag_number) + '-' + str(l+1),
                            "Стоимость": str(((v.price//10)*(self.roadtime))),
                            "Карта оплаты": man.card
                        })
class Person:
    def __init__(self,sys_prob, bank_prob):
        if (random.randint(1, 2) == 1):
            self.name = 'М, ' + random.choice(m_last_name) + ' ' + random.choice(m_first_name) + ' ' + random.choice(m_surname)
        else:
            self.name = 'Ж, ' + random.choice(f_last_name) + ' ' + random.choice(f_first_name) + ' ' + random.choice(f_surname)

        self.card = bank_card(sys_prob, bank_prob)
        self.passport = f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"
class Vagon:
    def __init__(self, type):
        self.vagon_data = {
            #a) Поезда «Сапсан»
            'a_1': {'size': 1, 'price': 100000, 'naming': '1P'},  # (1) 1Р — купе-переговорная, продаётся только целиком
            'a_2': {'size': 14, 'price': 31000, 'naming': '1B'},  # (2) 1В — просто места в вагоне 1 класса, без переговорной
            'a_3': {'size': 30, 'price': 21000, 'naming': '1C'},  # (3) 1С — вагон бизнес-класса
            'a_4': {'size': 40, 'price': 8200, 'naming': '2C'},  # (4) 2С — сидячий вагон эконом-класса
            'a_5': {'size': 50, 'price': 5200, 'naming': '2B'},  # (5) 2В — класс «Экономический+»
            'a_6': {'size': 12, 'price': 6700, 'naming': '2E'},  # (6) 2E — места в вагоне-бистро

            # b) Поезда «Стриж»
            'b_1': {'size': 16, 'price': 32000, 'naming': '1E'},  # (1) 1Е — СВ (VIP). Продаётся купе целиком.
            'b_2': {'size': 40, 'price': 12500, 'naming': '1P'},  # (2) 1Р — сидячие вагоны 1 класса.
            'b_3': {'size': 50, 'price': 5300, 'naming': '2C'},  # (3) 2С — сидячие вагоны 2 класса.

            # c) Сидячий вагон
            'c_1': {'size': 81, 'price': 1050, 'naming': '1C'},  # (1) 1С - обычные сидячие места
            'c_2': {'size': 36, 'price': 2100, 'naming': '1P'},  # (2) 1Р — в двухэтажном сидячем вагоне места в купе
            'c_3': {'size': 1, 'price': 101000, 'naming': '1B'},  # (3) 1В — вагон с индивидуальным размещением
            'c_4': {'size': 81, 'price': 2600, 'naming': '2P'},  # (4) 2Р — вагон повышенной комфортности
            'c_5': {'size': 81, 'price': 1100, 'naming': '2E'},  # (5) 2Е — сидячий вагон

            # d) Плацкартные вагоны
            'd_1': {'size': 54, 'price': 3600, 'naming': '3Э'},  # (1) 3Э — плацкартный вагон

            # e) Купе
            'e_1': {'size': 36, 'price': 4200, 'naming': '2Э'},  # (1) 2Э — кондиционируемый вагон с 4-местными купе.

            # f) Люкс (СВ)
            'f_1': {'size': 18, 'price': 18500, 'naming': '1Б'},  # (1) 1Б — бизнес-класс.
            'f_2': {'size': 18, 'price': 11500, 'naming': '1Л'},  # (2) 1Л — вагон СВ.

            # g) Мягкий вагон
            'g_1': {'size': 16, 'price': 8500, 'naming': '1A'},  # (1) 1А — вагон состоит из 4 купе и салона-бара.
            'g_2': {'size': 16, 'price': 8700, 'naming': '1И'}  # (1) 1И — вагон состоит из 4 купе и салона-бара.
            }

        if type in self.vagon_data:
            data = self.vagon_data[type]
            self.size = data['size']
            self.price = data['price']
            self.naming = data['naming']
        else:
            raise ValueError("Неизвестный тип вагона")
class BankInputUI:
    def __init__(self, master):
        self.master = master
        master.title("Ввод значений банков")

        self.title_label = tk.Label(master, text="Введите целые значения вероятности для банков:")
        self.title_label.pack(pady=10)

        # Создаем метки и поля для ввода с фиксированными названиями
        self.labels = ['Sber', 'T-Bank', 'VTB', 'Alfa']
        self.entries = []

        for label in self.labels:
            lbl = tk.Label(master, text=label + ":")
            lbl.pack()
            entry = tk.Entry(master)
            entry.pack()
            self.entries.append(entry)

        self.prob_title_label = tk.Label(master, text="Введите целые вероятности банковских систем:")
        self.prob_title_label.pack(pady=10)

        # Создаем метки и поля для ввода вероятностей
        self.prob_labels = ['Mir', 'MasterCard', 'Visa']
        self.prob_entries = []

        for prob_label in self.prob_labels:
            prob_lbl = tk.Label(master, text=prob_label + ":")
            prob_lbl.pack()
            prob_entry = tk.Entry(master)
            prob_entry.pack()
            self.prob_entries.append(prob_entry)

        # Создаем кнопку для отправки данных
        self.submit_button = tk.Button(master, text="Отправить", command=self.submit)
        self.submit_button.pack()
        self.data = []
        self.probabilities = []

        # Кнопка для установки значения по умолчанию
        self.default_button = tk.Button(master, text="Установить значение по умолчанию (равные значения всех вероятностей)", command=self.submit_with_default)
        self.default_button.pack(pady=10)


    def set_default(self):
        # Устанавливаем значение 1 во все поля ввода
        for entry in self.entries + self.prob_entries:
            entry.delete(0, tk.END)  # Очищаем поле
            entry.insert(0, '1')  # Вставляем значение по умолчанию

    def submit(self):
        try:
            # Получаем значения из полей ввода

            self.data = [int(entry.get()) for entry in self.entries]
            self.probabilities = [int(entry.get()) for entry in self.prob_entries]
            self.show_info("Данные приняты.", "Приступить к генерации данных")
            self.master.quit()  # Закрываем окно
        except ValueError:
            #messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа.")
            self.show_info("Ошибка: Пожалуйста, введите корректные числа.", "ok")
    def submit_with_default(self):
        self.set_default()
        self.submit()

    def show_info(self, message, button_text=None): #аналог встроенного messagebox, но с более подходящим функционалом
        info_window = tk.Toplevel(self.master)
        info_window.title("Информация")
        info_label = tk.Label(info_window, text=message, padx=20, pady=20)
        info_label.pack()

        # Кнопка для закрытия окна
        if button_text != None:
            ok_button = tk.Button(info_window, text=button_text, command=info_window.destroy)
            ok_button.pack(pady=10)
        if button_text==None:
            info_window.after(5000, info_window.destroy)

        self.master.wait_window(info_window)


    def get_bank_prob(self):
        return self.data
    def get_sys_prob(self):
        return self.probabilities


