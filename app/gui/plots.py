import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.database.db_handler import obter_quaternions, obter_dados_orbitais
from app.gui.simulation import running

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
