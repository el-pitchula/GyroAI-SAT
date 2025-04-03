# utils/math_functions.py
import numpy as np

def quaternion_multiply(q1, q2):
    """
    Multiplica dois quaternions.

    Args:
        q1 (np.ndarray): Quaternion 1 (q0, q1, q2, q3).
        q2 (np.ndarray): Quaternion 2 (q0, q1, q2, q3).

    Returns:
        np.ndarray: Produto dos quaternions.
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - z1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def quaternion_normalize(q):
    """
    Normaliza um quaternion.

    Args:
        q (np.ndarray): Quaternion (q0, q1, q2, q3).

    Returns:
        np.ndarray: Quaternion normalizado.
    """
    return q / np.linalg.norm(q)

def quaternion_to_rotation_matrix(q):
    """
    Converte um quaternion para uma matriz de rotação.

    Args:
        q (np.ndarray): Quaternion (q0, q1, q2, q3).

    Returns:
        np.ndarray: Matriz de rotação 3x3.
    """
    q0, q1, q2, q3 = q
    R = np.array([
        [1 - 2 * (q2**2 + q3**2), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
        [2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1**2 + q3**2), 2 * (q2 * q3 - q0 * q1)],
        [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1**2 + q2**2)]
    ])
    return R

def quaternion_derivative(q, omega):
    """
    Calcula a derivada do quaternion.

    Args:
        q (np.ndarray): Quaternion (q0, q1, q2, q3).
        omega (np.ndarray): Velocidade angular (wx, wy, wz).

    Returns:
        np.ndarray: Derivada do quaternion.
    """
    q0, q1, q2, q3 = q
    wx, wy, wz = omega
    Q = np.array([
        [0, -wx, -wy, -wz],
        [wx, 0, wz, -wy],
        [wy, -wz, 0, wx],
        [wz, wy, -wx, 0]
    ])
    return 0.5 * Q @ q

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

# utils/data_handler.py
import numpy as np

def generate_initial_data(num_points):
    """
    Gera dados de simulação iniciais para teste.

    Args:
        num_points (int): Número de pontos de dados a serem gerados.

    Returns:
        tuple: Tupla contendo quaternions e velocidades angulares.
    """
    quaternions = np.random.rand(num_points, 4)
    quaternions = np.array([quaternion_normalize(q) for q in quaternions])
    angular_velocities = np.random.rand(num_points, 3)
    return quaternions, angular_velocities

def preprocess_data(quaternions, angular_velocities):
    """
    Pré-processa os dados (normalização).

    Args:
        quaternions (np.ndarray): Array de quaternions.
        angular_velocities (np.ndarray): Array de velocidades angulares.

    Returns:
        tuple: Tupla contendo quaternions e velocidades angulares pré-processados.
    """
    # Normaliza os quaternions
    normalized_quaternions = np.array([quaternion_normalize(q) for q in quaternions])
    return normalized_quaternions, angular_velocities

# main.py
import numpy as np
import os
import sys

# Verifica se o script está sendo executado como um módulo
if __name__ == "__main__" and __package__ is None:
    print("Erro: Este script deve ser executado como um módulo.")
    print("Por favor, use 'python -m main' para executar.")
    #sys.exit(1)  # Remove a chamada sys.exit()

#from .simulation.environment import SatelliteEnvironment  # Importação relativa
#from .utils.data_handler import generate_initial_data, preprocess_data  # Importação relativa
from simulation.environment import SatelliteEnvironment  # Importação absoluta
from utils.data_handler import generate_initial_data, preprocess_data  # Importação absoluta

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