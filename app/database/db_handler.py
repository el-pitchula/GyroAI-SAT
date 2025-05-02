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

def obter_dados_orbitais(sim_id):
    """Lê os dados orbitais do banco para uma simulação específica."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tempo, x_km, y_km, z_km,
               vx_km_s, vy_km_s, vz_km_s,
               roll_deg, pitch_deg, yaw_deg
        FROM dados_orbitais
        WHERE sim_id = ?
        ORDER BY tempo ASC
    """, (sim_id,))
    
    rows = cursor.fetchall()
    conn.close()

    # Converte os dados em dicionários
    dados = []
    for row in rows:
        dados.append({
            'tempo': row[0],
            'x_km': row[1], 'y_km': row[2], 'z_km': row[3],
            'vx_km_s': row[4], 'vy_km_s': row[5], 'vz_km_s': row[6],
            'roll_deg': row[7], 'pitch_deg': row[8], 'yaw_deg': row[9]
        })

    return dados

def obter_ultimo_sim_id():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM simulacoes")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else None
