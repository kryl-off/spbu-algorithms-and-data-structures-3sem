import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

positions, velocities, best_positions, best_values = None, None, None, None
global_best_position, global_best_value = None, float('inf')
current_iter = 0
num_particles = 30
max_iter = 100
bounds = np.array([[-10, 10], [-10, 10], [-10, 10]])
root = None


def function(x):
    return (x[0] - 1) ** 2 + (x[1] - 3) ** 2 + 4 * (x[2] + 5) ** 2
def initialize_swarm():
    global positions, velocities, best_positions, best_values
    positions = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(num_particles, 3))
    velocities = np.random.uniform(-1, 1, size=(num_particles, 3))
    best_positions = np.copy(positions)
    best_values = np.array([float('inf')] * num_particles)
def update_velocity(position, velocity, best_position, global_best_position):
    w = float(w_entry.get())
    c1 = float(c1_entry.get())
    c2 = float(c2_entry.get())
    max_velocity = float(max_velocity_entry.get())  #из интерфейса

    r1 = np.random.rand(3)
    r2 = np.random.rand(3)
    new_velocity = (w * velocity +
                    c1 * r1 * (best_position - position) +
                    c2 * r2 * (global_best_position - position))
    new_velocity = np.clip(new_velocity, -max_velocity, max_velocity)
    return new_velocity
def run_pso():
    global current_iter, global_best_position, global_best_value
    current_iter = 0
    global_best_position = np.copy(best_positions[0])
    global_best_value = float('inf')
    animate_pso()
def animate_pso():
    global current_iter, global_best_position, global_best_value

    if current_iter < max_iter:
        for i in range(num_particles):
            value = function(positions[i])

            if value < best_values[i]:
                best_values[i] = value
                best_positions[i] = np.copy(positions[i])

            if value < global_best_value:
                global_best_value = value
                global_best_position = np.copy(positions[i])

            velocities[i] = update_velocity(positions[i], velocities[i], best_positions[i], global_best_position)
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], bounds[:, 0], bounds[:, 1])

        ax.clear()
        ax.set_xlim(bounds[0])
        ax.set_ylim(bounds[1])
        ax.set_zlim(bounds[2])
        ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2])
        ax.scatter(global_best_position[0], global_best_position[1], global_best_position[2], color='red')
        iteration_counter.config(text=f"Шаг: {current_iter + 1} / {max_iter}")
        canvas.draw()

        current_iter += 1
        root.after(50, animate_pso)
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Лучшее положение: {global_best_position}\nЛучшее значение: {global_best_value}\n")


def create_particles():
    global num_particles, max_iter
    num_particles = int(num_particles_entry.get())
    max_iter = int(max_iter_entry.get())
    initialize_swarm()
    ax.clear()
    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])
    ax.set_zlim(bounds[2])
    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2])
    canvas.draw()


def create_gui():
    global w_entry, c1_entry, c2_entry, max_velocity_entry, num_particles_entry, max_iter_entry, result_text, iteration_counter, ax, canvas, root

    root = tk.Tk()
    root.title("оптимизация роем частиц")
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    left_frame = tk.Frame(main_frame, padx=10, pady=10)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    center_frame = tk.Frame(main_frame, padx=10, pady=10)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    right_frame = tk.Frame(main_frame, padx=10, pady=10)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)
    tk.Label(left_frame, text="коэффициент сохранения скорости (w):").pack(anchor="w")
    w_entry = tk.Entry(left_frame)
    w_entry.pack(anchor="w", fill=tk.X)
    w_entry.insert(0, "0.5")

    tk.Label(left_frame, text="коэффициент собственного лучшего значения (c1):").pack(anchor="w")
    c1_entry = tk.Entry(left_frame)
    c1_entry.pack(anchor="w", fill=tk.X)
    c1_entry.insert(0, "2")

    tk.Label(left_frame, text="коэффициент глобального лучшего значения (c2):").pack(anchor="w")
    c2_entry = tk.Entry(left_frame)
    c2_entry.pack(anchor="w", fill=tk.X)
    c2_entry.insert(0, "2")

    tk.Label(left_frame, text="Максимальная скорость:").pack(anchor="w")
    max_velocity_entry = tk.Entry(left_frame)
    max_velocity_entry.pack(anchor="w", fill=tk.X)
    max_velocity_entry.insert(0, "0.2")  # Значение по умолчанию

    tk.Label(left_frame, text="Количество частиц:").pack(anchor="w")
    num_particles_entry = tk.Entry(left_frame)
    num_particles_entry.pack(anchor="w", fill=tk.X)
    num_particles_entry.insert(0, "50")

    tk.Label(left_frame, text="Количество итераций:").pack(anchor="w")
    max_iter_entry = tk.Entry(left_frame)
    max_iter_entry.pack(anchor="w", fill=tk.X)
    max_iter_entry.insert(0, "100")

    create_button = tk.Button(left_frame, text="Создать частицы", command=create_particles)
    create_button.pack(anchor="w", fill=tk.X, pady=5)

    calculate_button = tk.Button(left_frame, text="Рассчитать", command=run_pso)
    calculate_button.pack(anchor="w", fill=tk.X, pady=5)

    iteration_counter = tk.Label(left_frame, text="Итерация: 0 / 0")
    iteration_counter.pack(anchor="w", pady=5)

    # График
    figure = plt.figure(figsize=(8, 6))
    ax = figure.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(figure, master=center_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])
    ax.set_zlim(bounds[2])

    # Результаты
    tk.Label(right_frame, text="Результаты:").pack(anchor="w")
    result_text = tk.Text(right_frame, height=20, width=40)
    result_text.pack(anchor="w", fill=tk.Y, expand=True)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
