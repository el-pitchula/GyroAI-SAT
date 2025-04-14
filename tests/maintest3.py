import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- simulation.py ---
def start_simulation():
    print("Simulação iniciada")

def stop_simulation():
    print("Simulação parada")

def reset_simulation():
    print("Simulação resetada")

def update_satellite_simulation(canvas_satellite):
    """Atualiza a simulação visual do satélite (2D)."""
    canvas_satellite.delete("all")  # Limpa o canvas
    canvas_satellite.create_rectangle(50, 50, 100, 100, fill="blue")  # Desenha um quadrado (satélite)
    canvas_satellite.after(100, update_satellite_simulation, canvas_satellite)  # Atualiza a cada 100ms

def update_gyroscope_simulation(canvas_gyroscope):
    """Atualiza a simulação visual do giroscópio (3D)."""
    canvas_gyroscope.delete("all")
    canvas_gyroscope.create_oval(50, 50, 100, 100, fill="red")  # Desenha um círculo (giroscópio)
    canvas_gyroscope.after(100, update_gyroscope_simulation, canvas_gyroscope)

# --- plots.py ---
def create_angular_velocity_plot(parent):
    """Cria um gráfico de velocidade angular em tempo real."""
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
    canvas.get_tk_widget().pack(pady=10, fill=tk.X)  # Preenche horizontalmente
    canvas.draw()
    
    def update_plot():
        nonlocal t, omega
        t = np.linspace(0, 10, 100) + (t[-1] - t[0]) + 0.1  # Atualiza o tempo
        omega = np.sin(t)
        line.set_data(t, omega)
        ax.relim()
        ax.autoscale_view()
        canvas.draw_idle()
        parent.after(50, update_plot)  # Atualiza mais rápido
    
    update_plot()

def create_quaternion_plot(parent):
    """Cria um gráfico para visualizar a evolução dos quaternions."""
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
        t = np.linspace(0, 10, 100) + (t[-1] - t[0]) + 0.1  # Atualiza o tempo
        q0 = np.cos(t / 2)
        q1 = np.sin(t / 2)
        line1.set_data(t, q0)
        line2.set_data(t, q1)
        ax.relim()
        ax.autoscale_view()
        canvas.draw_idle()
        parent.after(50, update_plot)
    
    update_plot()

# --- data_display.py ---
def create_serial_monitor(parent):
    """Cria um monitor serial simulado."""
    frame = tk.Frame(parent)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    text_area = tk.Text(frame, height=5, bg="black", fg="white")
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, command=text_area.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area['yscrollcommand'] = scrollbar.set

    def update_serial_data():
        data = f"Tempo: {np.random.rand():.2f}, Valor: {np.random.randint(0, 100)}\n"
        text_area.insert(tk.END, data)
        text_area.see(tk.END)  # Mantém a rolagem automática
        parent.after(200, update_serial_data)

    update_serial_data()

def create_data_display(parent):
    """Exibe outros dados (posição, quaternions)."""
    frame = tk.Frame(parent)
    frame.pack(pady=10, fill=tk.X)

    data_label = tk.Label(frame, text="Dados de Posição/Quaternions:", font=("Arial", 10, "bold"))
    data_label.pack(side=tk.LEFT)

    data_text = tk.StringVar()
    data_display = tk.Label(frame, textvariable=data_text)
    data_display.pack(side=tk.LEFT)

    def update_data():
        position_data = f"X: {np.random.rand():.2f}, Y: {np.random.rand():.2f}, Z: {np.random.rand():.2f}"
        quaternion_data = f"q0: {np.random.rand():.2f}, q1: {np.random.rand():.2f}, q2: {np.random.rand():.2f}, q3: {np.random.rand():.2f}"
        data_text.set(f"{position_data}   |   {quaternion_data}")
        parent.after(100, update_data)

    update_data()

# neural_network.py
def create_neural_network_visualization(parent):
    """(Futuro) Visualização da rede neural."""
    label = tk.Label(parent, text="Visualização da Rede Neural (Futuro)", font=("Arial", 10))
    label.pack(pady=10)

# info_panels.py
def create_info_panel(parent, title, content):
    """Cria um painel de informações."""
    frame = tk.Frame(parent, bd=2, relief=tk.GROOVE)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text=title, font=("Arial", 10, "bold"))
    title_label.pack(pady=5)

    content_label = tk.Label(frame, text=content, justify=tk.LEFT)
    content_label.pack(padx=5, pady=5)

# main.py
def create_main_window():
    root = tk.Tk()
    root.title("GyroAI-SAT")
    root.geometry("1200x800")  # Tamanho inicial da janela

    # frames Principais
    frame_left = tk.Frame(root, width=400, padx=10, pady=10)
    frame_left.pack(side=tk.LEFT, fill=tk.Y)

    frame_middle = tk.Frame(root, width=400, padx=10, pady=10)
    frame_middle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Corrigido aqui

    frame_right = tk.Frame(root, width=400, padx=10, pady=10)
    frame_right.pack(side=tk.RIGHT, fill=tk.Y)

    # controles de Simulação (frame_left)
    controls_label = tk.Label(frame_left, text="Controles de Simulação", font=("Arial", 12, "bold"))
    controls_label.pack(pady=(10, 0))

    start_button = tk.Button(frame_left, text="Iniciar Simulação", command=start_simulation)
    start_button.pack(pady=5, fill=tk.X)

    stop_button = tk.Button(frame_left, text="Parar Simulação", command=stop_simulation)
    stop_button.pack(pady=5, fill=tk.X)

    reset_button = tk.Button(frame_left, text="Resetar", command=reset_simulation)
    reset_button.pack(pady=5, fill=tk.X)

    speed_label = tk.Label(frame_left, text="Velocidade de Simulação:")
    speed_label.pack(pady=(10, 0))
    speed_slider = tk.Scale(frame_left, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
    speed_slider.pack(fill=tk.X)

    # --- Simulações Visuais (frame_middle) ---
    satellite_label = tk.Label(frame_middle, text="Simulação Satélite (2D)", font=("Arial", 12, "bold"))
    satellite_label.pack(pady=(10, 0))
    canvas_satellite = tk.Canvas(frame_middle, bg="white", height=200)
    canvas_satellite.pack(pady=5, fill=tk.X)
    update_satellite_simulation(canvas_satellite)

    gyroscope_label = tk.Label(frame_middle, text="Simulação Giroscópio (3D)", font=("Arial", 12, "bold"))
    gyroscope_label.pack(pady=(10, 0))
    canvas_gyroscope = tk.Canvas(frame_middle, bg="white", height=200)
    canvas_gyroscope.pack(pady=5, fill=tk.X)
    update_gyroscope_simulation(canvas_gyroscope)

    # --- Gráficos (frame_middle) ---
    angular_velocity_label = tk.Label(frame_middle, text="Gráfico Velocidade Angular", font=("Arial", 10, "bold"))
    angular_velocity_label.pack(pady=(10, 0))
    create_angular_velocity_plot(frame_middle)

    quaternion_label = tk.Label(frame_middle, text="Gráfico Quaternions", font=("Arial", 10, "bold"))
    quaternion_label.pack(pady=(10, 0))
    create_quaternion_plot(frame_middle)

    # --- Monitor Serial e Dados (frame_right) ---
    serial_label = tk.Label(frame_right, text="Monitor Serial", font=("Arial", 12, "bold"))
    serial_label.pack(pady=(10, 0))
    create_serial_monitor(frame_right)

    data_label = tk.Label(frame_right, text="Dados Adicionais", font=("Arial", 12, "bold"))
    data_label.pack(pady=(10, 0))
    create_data_display(frame_right)

    # --- Painéis de Informações (abas) ---
    notebook = ttk.Notebook(frame_right)
    notebook.pack(pady=10, fill=tk.BOTH, expand=True)

    tab_modelagem = ttk.Frame(notebook)
    notebook.add(tab_modelagem, text="Modelagem Matemática")
    create_info_panel(tab_modelagem, "Modelagem Matemática", "Informações sobre a modelagem...")

    tab_algoritmo_ia = ttk.Frame(notebook)
    notebook.add(tab_algoritmo_ia, text="Algoritmo da IA")
    create_info_panel(tab_algoritmo_ia, "Algoritmo da IA", "Detalhes do algoritmo da IA...")

    tab_simulacoes = ttk.Frame(notebook)
    notebook.add(tab_simulacoes, text="Simulações")
    create_info_panel(tab_simulacoes, "Simulações", "Explicações sobre os elementos das simulações...")

    tab_gimbal_lock = ttk.Frame(notebook)
    notebook.add(tab_gimbal_lock, text="Gimbal Lock")
    create_info_panel(tab_gimbal_lock, "Gimbal Lock", "Representação visual e explicação do gimbal lock...")

    tab_funcionamento = ttk.Frame(notebook)
    notebook.add(tab_funcionamento, text="Funcionamento Geral")
    create_info_panel(tab_funcionamento, "Funcionamento Geral", "Artigo resumido do projeto e planejamentos do Obsidian...")

    return root

if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()