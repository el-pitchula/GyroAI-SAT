import tkinter as tk

# Variável de controle global
running = False

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
    from app.gui.simulation import running
    if running:
        canvas.delete("all")
        canvas.create_rectangle(120, 80, 220, 180, fill="blue")
    canvas.after(100, update_satellite_simulation, canvas)

def update_gyroscope_simulation(canvas):
    from app.gui.simulation import running
    if running:
        canvas.delete("all")
        canvas.create_oval(90, 90, 210, 210, fill="red")
    canvas.after(100, update_gyroscope_simulation, canvas)
