import tkinter as tk
import utils2
from tkinter import messagebox


# Функция для вывода состояния чекбоксов
def show_selected():
    print(get_checked_items())

def get_paths():
    path = entry_path.get()
    outpath = entry_outpath.get()
    return path, outpath
def get_checked_items():
    checked_items = []
    if fio_var.get() == 1:
        checked_items.append("ФИО")
    if passport_var.get() == 1:
        checked_items.append("Паспорт")
    if from_var.get() == 1:
        checked_items.append("Откуда")
    if to_var.get() == 1:
        checked_items.append("Куда")
    if departure_date_var.get() == 1:
        checked_items.append("Дата отъезда")
    if arrival_date_var.get() == 1:
        checked_items.append("Дата приезда")
    if flight_var.get() == 1:
        checked_items.append("Рейс")
    if seat_var.get() == 1:
        checked_items.append("Выбор вагона и места")
    if price_var.get() == 1:
        checked_items.append("Стоимость")
    if card_var.get() == 1:
        checked_items.append("Карта оплаты")

    return checked_items
def set_entries(values):
    print(values)
    for i in range(1,len(values)+1):
        entries[i].config(state='normal')
        entries[i].delete(0, tk.END)
        entries[i].insert(0, str(values[i-1]))
        entries[i].config(state='readonly')
    return 0


def anon():
    path, outpath = get_paths()
    df = utils2.anonymise_tickets(path, outpath)
    df.to_excel(outpath, index=False)
    return df
def open():
    path, outpath = get_paths()
    df = utils2.open_tickets(path)
    return df
def open_anon():
    path, outpath = get_paths()
    df = utils2.open_tickets(outpath)
    return df
def calculation():
    identifiers = get_checked_items()
    if (identifiers != []):
        df = open_anon()
        df_suppressed, suppressed_count = utils2.suppress(df, identifiers, 4000)
        k,top_bad = utils2.calculate_k_anonymity(df_suppressed, identifiers)
        set_entries(top_bad)
        entries[7].config(state='normal')
        entries[7].delete(0, tk.END)
        entries[7].insert(0, f"k = {k}")
        entries[7].config(state='readonly')
    else: messagebox.showerror("Error", "Choose at least one identifier!")





root = tk.Tk()
root.title("Window")

fio_var = tk.IntVar()
passport_var = tk.IntVar()
from_var = tk.IntVar()
to_var = tk.IntVar()
departure_date_var = tk.IntVar()
arrival_date_var = tk.IntVar()
flight_var = tk.IntVar()
seat_var = tk.IntVar()
price_var = tk.IntVar()
card_var = tk.IntVar()

check_fio = tk.Checkbutton(root, text="ФИО", variable=fio_var)
check_passport = tk.Checkbutton(root, text="Паспорт", variable=passport_var)
check_from = tk.Checkbutton(root, text="Откуда", variable=from_var)
check_to = tk.Checkbutton(root, text="Куда", variable=to_var)
check_departure_date = tk.Checkbutton(root, text="Дата отъезда", variable=departure_date_var)
check_arrival_date = tk.Checkbutton(root, text="Дата приезда", variable=arrival_date_var)
check_flight = tk.Checkbutton(root, text="Рейс", variable=flight_var)
check_seat = tk.Checkbutton(root, text="Выбор вагона и места", variable=seat_var)
check_price = tk.Checkbutton(root, text="Стоимость", variable=price_var)
check_card = tk.Checkbutton(root, text="Карта оплаты", variable=card_var)

check_fio.grid(row = 1, column = 1,sticky="w")
check_passport.grid(row = 2, column = 1,sticky="w")
check_from.grid(row = 3, column = 1,sticky="w")
check_to.grid(row = 4, column = 1,sticky="w")
check_departure_date.grid(row = 5, column = 1,sticky="w")
check_arrival_date.grid(row = 6, column = 1,sticky="w")
check_flight.grid(row = 7, column = 1,sticky="w")
check_seat.grid(row = 8, column = 1,sticky="w")
check_price.grid(row = 9, column = 1,sticky="w")
check_card.grid(row = 10, column = 1,sticky="w")

entries = []
for i in range(7+1):
    entry = tk.Entry(root, width=35)
    entry.grid(row=i, column=2)
    entries.append(entry)
    entry.config(state='readonly')

entries[0].config(state='normal')
entries[6].config(state='normal')
entries[0].insert(0, "Top of 5 bad k_anonimity after supress")
entries[6].insert(0, "k_anonimity after supress")
entries[0].config(state='readonly')
entries[6].config(state='readonly')

entry_path = tk.Entry(root, width=35)
entry_path.grid(row=1, column=3)
entry_path.insert(0,'../data/Tickets.xlsx')

entry_outpath = tk.Entry(root, width=35)
entry_outpath.grid(row=2, column=3)
entry_outpath.insert(0,'../data/Tickets_anon.xlsx')

entry_name = tk.Entry(root, width=35)
entry_name.grid(row=0, column=1)
entry_name.insert(0,'Выберите квази - идентификаторы:')
entry_name.config(state='readonly')

entry_name = tk.Entry(root, width=35)
entry_name.grid(row=0, column=3)
entry_name.insert(0,'Введите путь к файлу ввода и файлу вывода:')
entry_name.config(state='readonly')

calculate_button = tk.Button(root, text="Рассчитать", command=calculation)
calculate_button.grid(row=14, column=2, sticky="nsew")

anon_button = tk.Button(root, text="Обезличить", command=anon)
anon_button.grid(row=12, column=2, sticky="nsew")




root.mainloop()
