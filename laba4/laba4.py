import tkinter as tk
from tkinter import ttk
import numpy as np

def mutate(individual, mutation_rate, gene_min, gene_max):
    if np.random.rand() < mutation_rate:
        individual += np.random.normal(0, 0.1, size=individual.shape)
        individual = np.clip(individual, gene_min, gene_max)
    return individual

def crossover(parent1, parent2, crossover_rate):
    mask = np.random.rand(len(parent1)) < crossover_rate
    child = np.where(mask, parent1, parent2)
    return child

def function(scores):
    x1, x2, x3 = scores
    return (x1 - 1)**2 + (x2 - 3)**2 + 4 * (x3 + 5)**2
def make_population(size, gene_min, gene_max):
    return np.random.rand(size, 3) * (gene_max - gene_min) + gene_min
def choose_best_scores(population, fit_scores, elite_size):
    scores = list(enumerate(fit_scores))
    sorted_scores = sorted(scores, key=lambda x: x[1])
    best_indices = [idx for idx, _ in sorted_scores[:elite_size]]
    return population[best_indices]

def genetic_algorithm(population_size, generations, mutation_rate, gene_min, gene_max, elite_size, crossover_rate):
    population = make_population(population_size, gene_min, gene_max)
    best_solution = None
    best_fitness = float('inf')
    generation_data = []

    for generation in range(generations):
        fit_scores = np.array([function(ind) for ind in population])
        elites = choose_best_scores(population, fit_scores, elite_size)
        new_population = list(elites)
        while len(new_population) < population_size:
            parent_indices = np.random.choice(len(population), size=2, replace=False)
            parent1, parent2 = population[parent_indices]
            child = crossover(parent1, parent2, crossover_rate)
            child = mutate(child, mutation_rate, gene_min, gene_max)
            new_population.append(child)
        population = np.array(new_population)
        current_best_fitness = np.min(fit_scores)
        current_best_solution = population[np.argmin(fit_scores)]
        generation_data.append(
            (generation + 1, current_best_fitness, current_best_solution[0],
             current_best_solution[1], current_best_solution[2])
        )
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_solution = current_best_solution

    return best_solution, best_fitness, generation_data

def create_gui():
    root = tk.Tk()
    root.title("Генетический алгоритм")
    root.geometry("1300x700")
    root.resizable(True, True)

    style = ttk.Style()
    style.theme_use('default')

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame = ttk.Frame(root)
    main_frame.grid(sticky='nsew', padx=10, pady=10)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=3)
    main_frame.rowconfigure(0, weight=1)

    left_frame = ttk.Frame(main_frame)
    left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    left_frame.columnconfigure(0, weight=1)

    right_frame = ttk.Frame(main_frame)
    right_frame.grid(row=0, column=1, sticky='nsew')

    params_frame = ttk.LabelFrame(left_frame, text='Параметры')
    params_frame.grid(sticky='nsew', pady=5)
    params_frame.columnconfigure(1, weight=1)

    func_frame = ttk.Frame(params_frame)
    func_frame.grid(sticky='ew', pady=5)
    func_frame.columnconfigure(0, weight=1)

    ttk.Label(func_frame, text="Функция:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w')
    ttk.Label(func_frame, text="(x1 - 1)**2 + (x2 - 3)**2 + 4*(x3 + 5)**2").grid(row=1, column=0, sticky='w')

    labels = [
        "Вероятность мутации, %:",
        "Вероятность кроссовера, %:",
        "Количество хромосом:",
        "Минимальное значение гена:",
        "Максимальное значение гена:",
        "Количество элитных особей:"
    ]

    default_values = ["20", "70", "50", "-50", "50", "20"]
    entries = []

    for i, (label_text, default_value) in enumerate(zip(labels, default_values)):
        ttk.Label(params_frame, text=label_text).grid(row=i+2, column=0, sticky='w', pady=2)
        entry = ttk.Entry(params_frame)
        entry.grid(row=i+2, column=1, sticky='ew', pady=2)
        entry.insert(0, default_value)
        entries.append(entry)

    controls_frame = ttk.LabelFrame(left_frame, text='Управление')
    controls_frame.grid(sticky='ew', pady=5)
    controls_frame.columnconfigure(0, weight=1)

    gen_frame = ttk.Frame(controls_frame)
    gen_frame.grid(sticky='ew', pady=2)
    gen_frame.columnconfigure(1, weight=1)

    ttk.Label(gen_frame, text="Количество поколений:").grid(row=0, column=0, sticky='w')
    generations_entry = ttk.Entry(gen_frame, width=10)
    generations_entry.grid(row=0, column=1, sticky='ew', padx=5)
    generations_entry.insert(0, "1000")

    def add_generations(amount):
        current = int(generations_entry.get())
        generations_entry.delete(0, tk.END)
        generations_entry.insert(0, str(current + amount))

    ttk.Button(controls_frame, text="+1", command=lambda: add_generations(1)).grid(row=1, column=0, pady=5, padx=0)
    ttk.Button(controls_frame, text="+10", command=lambda: add_generations(10)).grid(row=1, column=1, pady=5, padx=0)
    ttk.Button(controls_frame, text="+100", command=lambda: add_generations(100)).grid(row=1, column=2, pady=5, padx=5)
    ttk.Button(controls_frame, text="+1000", command=lambda: add_generations(1000)).grid(row=1, column=3, pady=5, padx=5)

    def calculate_mod():
        mutation_rate = float(entries[0].get()) / 100
        crossover_rate = float(entries[1].get()) / 100
        population_size = int(entries[2].get())
        gene_min = float(entries[3].get())
        gene_max = float(entries[4].get())
        elite_size = int(entries[5].get())
        generations = int(generations_entry.get())

        best_solution, best_fitness, generation_data = genetic_algorithm(
            population_size, generations, mutation_rate, gene_min, gene_max, elite_size, crossover_rate
        )

        best_solution_label.config(text=f"x1 = {best_solution[0]:.5f}, x2 = {best_solution[1]:.5f}, x3 = {best_solution[2]:.5f}")
        best_fitness_label.config(text=f"{best_fitness:.5f}")

        for i in tree.get_children():
            tree.delete(i)

        for data in generation_data:
            generation, fitness, x1, x2, x3 = data
            tree.insert("", "end", values=(generation, f"{fitness:.5f}", f"{x1:.5f}", f"{x2:.5f}", f"{x3:.5f}"))

    ttk.Button(controls_frame, text="Рассчитать", command=calculate_mod).grid(pady=10)

    results_frame = ttk.LabelFrame(left_frame, text='Результаты')
    results_frame.grid(sticky='ew', pady=5)
    results_frame.columnconfigure(1, weight=1)

    ttk.Label(results_frame, text="Лучшее решение:").grid(row=0, column=0, sticky='w', pady=2)
    best_solution_label = ttk.Label(results_frame, text="")
    best_solution_label.grid(row=0, column=1, sticky='w', padx=10)

    ttk.Label(results_frame, text="Значение функции:").grid(row=1, column=0, sticky='w', pady=2)
    best_fitness_label = ttk.Label(results_frame, text="")
    best_fitness_label.grid(row=1, column=1, sticky='w', padx=10)

    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(0, weight=1)

    tree_frame = ttk.Frame(right_frame)
    tree_frame.grid(sticky='nsew', pady=5)
    tree_frame.columnconfigure(0, weight=1)
    tree_frame.rowconfigure(0, weight=1)

    columns = ("Номер", "Результат", "x1", "x2", "x3")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    tree.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

if __name__ == "__main__":
    create_gui()
