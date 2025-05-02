# Inserção de dados nas tabelas

import sqlite3
import os

# Define o caminho absoluto para o arquivo do banco de dados na raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))              # Caminho de onde está este arquivo
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../gyroai.db'))  # Sobe dois níveis até a raiz

def iniciar_simulacao(descricao="Simulação"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO simulacoes (descricao) VALUES (?)", (descricao,))
    conn.commit()
    sim_id = cursor.lastrowid
    conn.close()
    return sim_id

def salvar_dado_gyro(sim_id, tempo, omega_x, omega_y, omega_z):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dados_gyro (sim_id, tempo, omega_x, omega_y, omega_z)
        VALUES (?, ?, ?, ?, ?)
    """, (sim_id, tempo, omega_x, omega_y, omega_z))
    conn.commit()
    conn.close()

def salvar_quaternion(sim_id, tempo, q0, q1, q2, q3):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dados_quaternions (sim_id, tempo, q0, q1, q2, q3)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sim_id, tempo, q0, q1, q2, q3))
    conn.commit()
    conn.close()

def salvar_log_serial(sim_id, tempo, valor):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO serial_log (sim_id, tempo, valor)
        VALUES (?, ?, ?)
    """, (sim_id, tempo, valor))
    conn.commit()
    conn.close()

def salvar_dado_orbital(sim_id, tempo, x, y, z, vx, vy, vz, roll, pitch, yaw, tipo="simulado"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dados_orbitais (
            sim_id, tempo, x_km, y_km, z_km,
            vx_km_s, vy_km_s, vz_km_s,
            roll_deg, pitch_deg, yaw_deg,
            tipo_dado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (sim_id, tempo, x, y, z, vx, vy, vz, roll, pitch, yaw, tipo))
    conn.commit()
    conn.close()
