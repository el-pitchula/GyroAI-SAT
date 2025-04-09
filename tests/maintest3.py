def create_main_window():
    root = tk.Tk()
    root.title("GyroAI-SAT")
    root.geometry("1280x800")
    root.configure(bg="#f0f0f0")  # Cor de fundo clara para destacar blocos

    # --- Grid Principal (3 colunas) ---
    root.grid_columnconfigure(0, weight=1, uniform="group")
    root.grid_columnconfigure(1, weight=2, uniform="group")
    root.grid_columnconfigure(2, weight=1, uniform="group")

    # --- Frame Esquerdo (Controles) ---
    frame_left = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE, padx=10, pady=10)
    frame_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    tk.Label(frame_left, text="Controles de Simulação", font=("Arial", 12, "bold"), bg="white").pack(pady=(0, 10))
    tk.Button(frame_left, text="Iniciar Simulação", command=start_simulation).pack(fill=tk.X, pady=5)
    tk.Button(frame_left, text="Parar Simulação", command=stop_simulation).pack(fill=tk.X, pady=5)
    tk.Button(frame_left, text="Resetar", command=reset_simulation).pack(fill=tk.X, pady=5)

    tk.Label(frame_left, text="Velocidade de Simulação:", bg="white").pack(pady=(20, 5))
    tk.Scale(frame_left, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL).pack(fill=tk.X)

    # --- Frame Central (Canvas e Plots) ---
    frame_middle = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE, padx=10, pady=10)
    frame_middle.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    canvas_satellite = tk.Canvas(frame_middle, width=200, height=200, bg="lightblue")
    canvas_satellite.pack(pady=10)
    update_satellite_simulation(canvas_satellite)

    canvas_gyroscope = tk.Canvas(frame_middle, width=200, height=200, bg="lightcoral")
    canvas_gyroscope.pack(pady=10)
    update_gyroscope_simulation(canvas_gyroscope)

    create_angular_velocity_plot(frame_middle)
    create_quaternion_plot(frame_middle)

    # --- Frame Direito (Monitor + Dados) ---
    frame_right = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE, padx=10, pady=10)
    frame_right.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

    create_serial_monitor(frame_right)
    create_data_display(frame_right)
    create_neural_network_visualization(frame_right)
    create_info_panel(frame_right, "Sobre o Projeto", "Simulação de satélite com giroscópio e IA.")
    create_info_panel(frame_right, "Equipe", "Nome 1\nNome 2\nNome 3")

    root.mainloop()
