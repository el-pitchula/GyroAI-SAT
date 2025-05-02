import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from app.database.db_setup import create_db
from app.database.db_handler import iniciar_simulacao, obter_dados_orbitais

# --- Funções de Simulação ---
def start_simulation():
    print("Simulação iniciada")

def stop_simulation():
    print("Simulação parada")

def reset_simulation():
    print("Simulação resetada")

def update_satellite_simulation(canvas_satellite):
    canvas_satellite.delete("all")
    canvas_satellite.create_rectangle(50, 50, 100, 100, fill="blue")
    canvas_satellite.after(100, update_satellite_simulation, canvas_satellite)

def update_gyroscope_simulation(canvas_gyroscope):
    canvas_gyroscope.delete("all")
    canvas_gyroscope.create_oval(50, 50, 100, 100, fill="red")
    canvas_gyroscope.after(100, update_gyroscope_simulation, canvas_gyroscope)

# --- Plots ---
def create_angular_velocity_plot(parent):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title("Velocidade Angular")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Velocidade (rad/s)")
    ax.grid()

    t = np.linspace(0, 10, 100)
    omega = np.sin(t)
    line, = ax.plot(t, omega, label="\u03C9 (rad/s)")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().pack(pady=10, fill=tk.X)
    canvas.draw()

    def update_plot():
        nonlocal t, omega
        t = np.linspace(0, 10, 100) + (t[-1] - t[0]) + 0.1
        omega = np.sin(t)
        line.set_data(t, omega)
        ax.relim()
        ax.autoscale_view()
        canvas.draw_idle()
        parent.after(50, update_plot)

    update_plot()

def create_quaternion_plot(parent):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title("Evolução dos Quaternions")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Valor")
    ax.grid()

    t = np.linspace(0, 10, 100)
    q0 = np.cos(t / 2)
    q1 = np.sin(t / 2)
    line1, = ax.plot(t, q0, label="q0")
    line2, = ax.plot(t, q1, label="q1")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().pack(pady=10, fill=tk.X)
    canvas.draw()

    def update_plot():
        nonlocal t, q0, q1
        t = np.linspace(0, 10, 100) + (t[-1] - t[0]) + 0.1
        q0 = np.cos(t / 2)
        q1 = np.sin(t / 2)
        line1.set_data(t, q0)
        line2.set_data(t, q1)
        ax.relim()
        ax.autoscale_view()
        canvas.draw_idle()
        parent.after(50, update_plot)

    update_plot()

# --- Dados GUI (agora vindo do banco!) ---
def create_data_display(parent, sim_id):
    frame = tk.Frame(parent)
    frame.pack(pady=10, fill=tk.X)

    data_label = tk.Label(frame, text="Dados da Órbita (Banco de Dados)", font=("Arial", 10, "bold"))
    data_label.pack(side=tk.LEFT)

    data_text = tk.StringVar()
    data_display = tk.Label(frame, textvariable=data_text)
    data_display.pack(side=tk.LEFT)

    dados = obter_dados_orbitais(sim_id)
    total = len(dados)

    def update_data(i=[0]):
        if total == 0:
            data_text.set("Nenhum dado no banco.")
            return
        d = dados[i[0] % total]
        text = f"t={d['tempo']:.0f}s | Pos: ({d['x_km']:.2f}, {d['y_km']:.2f}, {d['z_km']:.2f}) km | " \
               f"Vel: ({d['vx_km_s']:.2f}, {d['vy_km_s']:.2f}, {d['vz_km_s']:.2f}) km/s | " \
               f"Euler: ({d['roll_deg']:.2f}, {d['pitch_deg']:.2f}, {d['yaw_deg']:.2f})°"
        data_text.set(text)
        i[0] += 1
        parent.after(200, update_data)

    update_data()

# --- Painéis Info ---
def create_info_panel(parent, title, content):
    frame = tk.Frame(parent, bd=2, relief=tk.GROOVE)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)
    tk.Label(frame, text=title, font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(frame, text=content, justify=tk.LEFT).pack(padx=5, pady=5)

# --- MAIN GUI ---
def create_main_window():
    create_db()

    from app.database.db_handler import obter_ultimo_sim_id_com_dados
    sim_id = obter_ultimo_sim_id_com_dados()  # <-- use o sim_id que já tem dados

    root = tk.Tk()
    root.title("GyroAI-SAT")
    root.geometry("1200x800")

    frame_left = tk.Frame(root, width=400, padx=10, pady=10)
    frame_left.pack(side=tk.LEFT, fill=tk.Y)

    frame_middle = tk.Frame(root, width=400, padx=10, pady=10)
    frame_middle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_right = tk.Frame(root, width=400, padx=10, pady=10)
    frame_right.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(frame_left, text="Controles de Simulação", font=("Arial", 12, "bold")).pack(pady=(10, 0))
    tk.Button(frame_left, text="Iniciar Simulação", command=start_simulation).pack(pady=5, fill=tk.X)
    tk.Button(frame_left, text="Parar Simulação", command=stop_simulation).pack(pady=5, fill=tk.X)
    tk.Button(frame_left, text="Resetar", command=reset_simulation).pack(pady=5, fill=tk.X)
    tk.Label(frame_left, text="Velocidade de Simulação:").pack(pady=(10, 0))
    tk.Scale(frame_left, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL).pack(fill=tk.X)

    # Meio
    tk.Label(frame_middle, text="Simulação Satélite (2D)", font=("Arial", 12, "bold")).pack(pady=(10, 0))
    canvas_sat = tk.Canvas(frame_middle, bg="white", height=200)
    canvas_sat.pack(pady=5, fill=tk.X)
    update_satellite_simulation(canvas_sat)

    tk.Label(frame_middle, text="Simulação Giroscópio (3D)", font=("Arial", 12, "bold")).pack(pady=(10, 0))
    canvas_gyro = tk.Canvas(frame_middle, bg="white", height=200)
    canvas_gyro.pack(pady=5, fill=tk.X)
    update_gyroscope_simulation(canvas_gyro)

    tk.Label(frame_middle, text="Gráfico Velocidade Angular", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    create_angular_velocity_plot(frame_middle)
    tk.Label(frame_middle, text="Gráfico Quaternions", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    create_quaternion_plot(frame_middle)

    # Direita
    tk.Label(frame_right, text="Dados da Órbita", font=("Arial", 12, "bold")).pack(pady=(10, 0))
    create_data_display(frame_right, sim_id)

    notebook = ttk.Notebook(frame_right)
    notebook.pack(pady=10, fill=tk.BOTH, expand=True)
    tab_modelagem = ttk.Frame(notebook)
    tab_alg = ttk.Frame(notebook)
    tab_gimbal = ttk.Frame(notebook)
    tab_func = ttk.Frame(notebook)

    notebook.add(tab_modelagem, text="Modelagem")
    notebook.add(tab_alg, text="Algoritmo IA")
    notebook.add(tab_gimbal, text="Gimbal Lock")
    notebook.add(tab_func, text="Funcionamento")

    create_info_panel(tab_modelagem, "Modelagem Matemática", "Conteúdo aqui...")
    create_info_panel(tab_alg, "Algoritmo IA", "Conteúdo IA...")
    create_info_panel(tab_gimbal, "Gimbal Lock", "Explicação Gimbal Lock...")
    create_info_panel(tab_func, "Funcionamento Geral", "Resumo e etapas do projeto.")

    return root
