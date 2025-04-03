# main.py
import numpy as np
import os
import sys

# Verifica se o script está sendo executado como um módulo
if __name__ == "__main__" and __package__ is None:
    print("Erro: Este script deve ser executado como um módulo.")
    print("Por favor, use 'python -m main' para executar.")
    #sys.exit(1)  # Remove a chamada sys.exit()

from .simulation.environment import SatelliteEnvironment  # Importação relativa
from .utils.data_handler import generate_initial_data, preprocess_data  # Importação relativa

def main():
    # Parâmetros do satélite
    inertia_matrix = np.array([[100, 0, 0], [0, 200, 0], [0, 0, 300]])  # Exemplo
    initial_quaternion = np.array([1, 0, 0, 0])  # Sem rotação inicial
    initial_angular_velocity = np.array([0.1, 0.1, 0.1])  # Velocidade angular inicial
    dt = 0.1  # Intervalo de tempo

    # Cria o ambiente de simulação
    env = SatelliteEnvironment(inertia_matrix, initial_quaternion, initial_angular_velocity, dt)

    # Gera dados iniciais
    num_points = 100
    quaternions, angular_velocities = generate_initial_data(num_points)

    # Pré-processa os dados
    processed_quaternions, processed_angular_velocities = preprocess_data(quaternions, angular_velocities)

    # Simulação básica
    for _ in range(10):
        control_torque = np.array([0.01, 0.01, 0.01])  # Torque de controle de exemplo
        new_quaternion, new_angular_velocity = env.step(control_torque)
        print("Quaternion:", new_quaternion)
        print("Velocidade Angular:", new_angular_velocity)

if __name__ == "__main__":
    main()