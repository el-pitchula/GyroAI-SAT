# simulation/environment.py
import numpy as np
from .utils.math_functions import quaternion_normalize, quaternion_derivative  # Importação relativa

class SatelliteEnvironment:
    def __init__(self, inertia_matrix, initial_quaternion, initial_angular_velocity, dt):
        """
        Inicializa o ambiente de simulação do satélite.

        Args:
            inertia_matrix (np.ndarray): Matriz de inércia do satélite.
            initial_quaternion (np.ndarray): Quaternion inicial.
            initial_angular_velocity (np.ndarray): Velocidade angular inicial.
            dt (float): Intervalo de tempo da simulação.
        """
        self.inertia_matrix = inertia_matrix
        self.quaternion = initial_quaternion
        self.angular_velocity = initial_angular_velocity
        self.dt = dt

    def step(self, control_torque):
        """
        Atualiza o estado do satélite.

        Args:
            control_torque (np.ndarray): Torque de controle aplicado ao satélite.

        Returns:
            np.ndarray: Novo quaternion.
            np.ndarray: Nova velocidade angular.
        """
        # Calcula a derivada da velocidade angular
        angular_acceleration = np.linalg.inv(self.inertia_matrix) @ (control_torque - np.cross(self.angular_velocity, self.inertia_matrix @ self.angular_velocity))

        # Atualiza a velocidade angular
        self.angular_velocity = self.angular_velocity + angular_acceleration * self.dt

        # Atualiza o quaternion
        self.quaternion = quaternion_normalize(self.quaternion + quaternion_derivative(self.quaternion, self.angular_velocity) * self.dt)

        return self.quaternion, self.angular_velocity

    def get_state(self):
        """
        Retorna o estado atual do satélite.

        Returns:
            np.ndarray: Quaternion atual.
            np.ndarray: Velocidade angular atual.
        """
        return self.quaternion, self.angular_velocity

# main.py
import numpy as np
from simulation.environment import SatelliteEnvironment
from utils.data_handler import generate_initial_data, preprocess_data

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