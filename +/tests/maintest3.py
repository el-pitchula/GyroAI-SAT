import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def create_controls(parent):
    """Cria os controles da interface para simulação e ajustes."""
    label = tk.Label(parent, text="Controles de Simulação", font=("Arial", 12, "bold"))
    label.pack(pady=10)
    
    start_button = tk.Button(parent, text="Iniciar Simulação", command=start_simulation)
    start_button.pack(pady=5)
    
    stop_button = tk.Button(parent, text="Parar Simulação", command=stop_simulation)
    stop_button.pack(pady=5)
    
    reset_button = tk.Button(parent, text="Resetar", command=reset_simulation)
    reset_button.pack(pady=5)
    
    # Controle de velocidade de simulação
    speed_label = tk.Label(parent, text="Velocidade de Simulação:")
    speed_label.pack(pady=5)
    speed_slider = tk.Scale(parent, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
    speed_slider.pack()
    
    # Gráfico de Velocidade Angular
    create_angular_velocity_plot(parent)
    
    # Gráfico de Quaternions
    create_quaternion_plot(parent)
    
    # Diagrama de Blocos
    create_block_diagram(parent)

def create_angular_velocity_plot(parent):
    """Cria um gráfico de velocidade angular em tempo real."""
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title("Velocidade Angular")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Velocidade (rad/s)")
    ax.grid()
    
    t = np.linspace(0, 10, 100)
    omega = np.sin(t)
    ax.plot(t, omega, label="\u03C9 (rad/s)")
    ax.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

def create_quaternion_plot(parent):
    """Cria um gráfico para visualizar a evolução dos quaternions."""
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title("Evolução dos Quaternions")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Valor")
    ax.grid()
    
    t = np.linspace(0, 10, 100)
    q = [np.cos(t / 2), np.sin(t / 2)]
    ax.plot(t, q[0], label="q0")
    ax.plot(t, q[1], label="q1")
    ax.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

def create_block_diagram(parent):
    """Cria um diagrama de blocos ilustrando o fluxo da simulação."""
    diagram_label = tk.Label(parent, text="Diagrama de Blocos - Fluxo da Simulação", font=("Arial", 10, "bold"))
    diagram_label.pack(pady=5)
    
    diagram_text = """
    [ Entrada de Dados ] → [ Processamento ] → [ Controle de Atitude ] → [ Visualização ]
    """
    diagram_display = tk.Label(parent, text=diagram_text, font=("Courier", 10))
    diagram_display.pack(pady=5)

def start_simulation():
    print("Simulação iniciada")

def stop_simulation():
    print("Simulação parada")

def reset_simulation():
    print("Simulação resetada")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Testando Controles")
    create_controls(root)
    root.mainloop()