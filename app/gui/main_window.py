import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.database.db_handler import (
    obter_quaternions,
    obter_ultimo_sim_id_com_dados
)

class GyroAISimplified:
    def __init__(self, root):
        self.root = root
        self.root.title("GyroAI Viewer")
        self.root.geometry("1000x700")

        self.sim_id = obter_ultimo_sim_id_com_dados()
        self.running = False
        self.speed = 200

        self.build_ui()

    def build_ui(self):
        # Botões principais
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Iniciar", command=self.start).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Parar", command=self.stop).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Resetar", command=self.reset).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="IA", command=self.run_ai).pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Velocidade:").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        tk.Scale(control_frame, from_=0.1, to=5.0, resolution=0.1,
                 orient=tk.HORIZONTAL, variable=self.speed_var).pack(side=tk.LEFT)

        # Monitor serial
        self.monitor = tk.Text(self.root, height=6, bg="black", fg="lime")
        self.monitor.pack(fill=tk.X, padx=10, pady=5)

        # Gráfico de quaternions
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.init_quaternion_plot()

    def log(self, msg):
        self.monitor.insert(tk.END, msg + "\n")
        self.monitor.see(tk.END)

    def init_quaternion_plot(self):
        dados = obter_quaternions(self.sim_id)
        if not dados:
            self.log("Nenhum dado de quaternions encontrado.")
            return

        self.t = [d['tempo'] for d in dados]
        self.q0 = [d['q0'] for d in dados]
        self.q1 = [d['q1'] for d in dados]
        self.q2 = [d['q2'] for d in dados]
        self.q3 = [d['q3'] for d in dados]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title("Quaternions")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")
        ax.grid()

        self.line0, = ax.plot([], [], label="q0")
        self.line1, = ax.plot([], [], label="q1")
        self.line2, = ax.plot([], [], label="q2")
        self.line3, = ax.plot([], [], label="q3")
        ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax = ax
        self.index = 0

    def update_plot(self):
        n = len(self.t)
        if not self.running or n == 0:
            return

        i = self.index % n
        window = 50
        start = max(0, i - window)

        self.line0.set_data(self.t[start:i], self.q0[start:i])
        self.line1.set_data(self.t[start:i], self.q1[start:i])
        self.line2.set_data(self.t[start:i], self.q2[start:i])
        self.line3.set_data(self.t[start:i], self.q3[start:i])
        self.ax.set_xlim(self.t[start], self.t[i])
        self.ax.set_ylim(-1.1, 1.1)
        self.canvas.draw_idle()

        self.index += 1
        self.root.after(int(1000 / self.speed_var.get()), self.update_plot)

    def start(self):
        if not self.running:
            self.log("Simulação iniciada.")
            self.running = True
            self.update_plot()

    def stop(self):
        self.log("Simulação pausada.")
        self.running = False

    def reset(self):
        self.log("Simulação resetada.")
        self.index = 0

    def run_ai(self):
        self.log("[IA] Função de IA a ser implementada...")


def create_main_window():
    root = tk.Tk()
    app = GyroAISimplified(root)
    return root

if __name__ == "__main__":
    create_main_window().mainloop()


'''
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from app.database.db_setup import create_db
from app.database.db_handler import (
    iniciar_simulacao,
    obter_dados_orbitais,
    obter_ultimo_sim_id_com_dados,
    obter_quaternions
)

# Variáveis globais de controle
running = False

# --- Funções de Simulação ---
def start_simulation():
    global running
    running = True
    print("▶ Simulação iniciada")

def stop_simulation():
    global running
    running = False
    print("⏸ Simulação pausada")

def reset_simulation():
    global running
    running = False
    print("🔄 Simulação resetada")

def update_satellite_simulation(canvas):
    if running:
        canvas.delete("all")
        canvas.create_rectangle(120, 80, 220, 180, fill="blue")
    canvas.after(100, update_satellite_simulation, canvas)

def update_gyroscope_simulation(canvas):
    if running:
        canvas.delete("all")
        canvas.create_oval(90, 90, 210, 210, fill="red")
    canvas.after(100, update_gyroscope_simulation, canvas)

# --- Plot de velocidade angular ---
def create_angular_velocity_plot(parent, sim_id):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title("Velocidade Angular")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Velocidade (rad/s)")
    ax.grid()

    dados = obter_quaternions(sim_id)
    if dados:
        t_vals = np.array([d['tempo'] for d in dados])
        omega = np.gradient([d['q1'] for d in dados])
    else:
        t_vals = np.linspace(0, 10, 100)
        omega = np.sin(t_vals)

    line, = ax.plot([], [], label="\u03C9 (rad/s)")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)
    canvas.draw()

    i = [0]
    def update_plot():
        if running:
            end = i[0]
            if end > len(t_vals): return
            line.set_data(t_vals[:end], omega[:end])
            ax.set_xlim(t_vals[0], t_vals[min(end, -1)])
            ax.set_ylim(min(omega)-0.1, max(omega)+0.1)
            canvas.draw_idle()
            i[0] += 1
        parent.after(200, update_plot)

    update_plot()

# --- Plot de quaternions ---
def create_quaternion_plot(parent, sim_id):
    dados = obter_quaternions(sim_id)
    if not dados:
        return

    fig, ax = plt.subplots(figsize=(5, 2.5))
    ax.set_title("Quaternions")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Valor")
    ax.grid()

    t = [d['tempo'] for d in dados]
    q0 = [d['q0'] for d in dados]
    q1 = [d['q1'] for d in dados]
    q2 = [d['q2'] for d in dados]
    q3 = [d['q3'] for d in dados]

    line0, = ax.plot([], [], label="q0", color='blue')
    line1, = ax.plot([], [], label="q1", color='orange')
    line2, = ax.plot([], [], label="q2", color='green')
    line3, = ax.plot([], [], label="q3", color='red')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)
    canvas.draw()

    i = [0]
    def update_plot():
        if running:
            end = i[0]
            if end >= len(t): return
            line0.set_data(t[:end], q0[:end])
            line1.set_data(t[:end], q1[:end])
            line2.set_data(t[:end], q2[:end])
            line3.set_data(t[:end], q3[:end])
            ax.set_xlim(t[0], t[end])
            ax.set_ylim(-1.1, 1.1)
            canvas.draw_idle()
            i[0] += 1
        parent.after(200, update_plot)

    update_plot()

# --- Dados da órbita ---
def create_data_display(parent, sim_id):
    dados = obter_dados_orbitais(sim_id)
    total = len(dados)
    data_text = tk.StringVar()

    label = tk.Label(parent, textvariable=data_text, wraplength=800, justify=tk.LEFT)
    label.grid(row=0, column=0, sticky="w")

    if total == 0:
        data_text.set("❌ Nenhum dado disponível.")
        return

    i = [0]
    def update_data():
        if running:
            d = dados[i[0] % total]
            texto = (
                f"t={d['tempo']:.0f}s | Pos: ({d['x_km']:.2f}, {d['y_km']:.2f}, {d['z_km']:.2f}) km | "
                f"Vel: ({d['vx_km_s']:.2f}, {d['vy_km_s']:.2f}, {d['vz_km_s']:.2f}) km/s | "
                f"Euler: ({d['roll_deg']:.2f}, {d['pitch_deg']:.2f}, {d['yaw_deg']:.2f})°"
            )
            data_text.set(texto)
            i[0] += 1
        parent.after(500, update_data)

    update_data()

# --- Interface Principal ---
def create_main_window():
    create_db()
    sim_id = obter_ultimo_sim_id_com_dados()
    print(f"🛰 SIM ID: {sim_id}")

    root = tk.Tk()
    root.title("GyroAI-SAT")
    root.geometry("1280x720")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    main_frame = tk.Frame(root)
    main_frame.grid(sticky="nsew", padx=10, pady=10)

    # --- Esquerda (Simulações) ---
    left_frame = tk.Frame(main_frame)
    left_frame.grid(row=0, column=0, rowspan=2, sticky="nsw", padx=10)

    tk.Label(left_frame, text="Simulação Satélite").pack()
    canvas_satellite = tk.Canvas(left_frame, width=300, height=200, bg="white")
    canvas_satellite.pack(pady=5)

    tk.Label(left_frame, text="Simulação Giroscópio").pack()
    canvas_gyro = tk.Canvas(left_frame, width=300, height=200, bg="white")
    canvas_gyro.pack(pady=5)

    update_satellite_simulation(canvas_satellite)
    update_gyroscope_simulation(canvas_gyro)

    # --- Centro (Gráficos) ---
    center_frame = tk.Frame(main_frame)
    center_frame.grid(row=0, column=1, sticky="n")

    graph1_frame = tk.Frame(center_frame)
    graph1_frame.grid(row=0, column=0)
    create_angular_velocity_plot(graph1_frame, sim_id)

    graph2_frame = tk.Frame(center_frame)
    graph2_frame.grid(row=1, column=0)
    create_quaternion_plot(graph2_frame, sim_id)

    # --- Direita (Dados + Botões) ---
    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=0, column=2, sticky="ne", padx=20)

    create_data_display(right_frame, sim_id)

    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=1, column=2, sticky="se", pady=10)

    ttk.Button(button_frame, text="▶ Iniciar", command=start_simulation).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="⏸ Pausar", command=stop_simulation).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="🔄 Resetar", command=reset_simulation).grid(row=0, column=2, padx=5)

    root.mainloop()
'''