# database/db_handler.py
import sqlite3

DB_NAME = "gyroai.db"

def iniciar_simulacao(descricao="Simulação"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO simulacoes (descricao) VALUES (?)", (descricao,))
    conn.commit()
    sim_id = cursor.lastrowid
    conn.close()
    return sim_id

def salvar_dado_gyro(sim_id, tempo, omega_x, omega_y, omega_z):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dados_gyro (sim_id, tempo, omega_x, omega_y, omega_z)
        VALUES (?, ?, ?, ?, ?)
    """, (sim_id, tempo, omega_x, omega_y, omega_z))
    conn.commit()
    conn.close()

def salvar_quaternion(sim_id, tempo, q0, q1, q2, q3):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dados_quaternions (sim_id, tempo, q0, q1, q2, q3)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sim_id, tempo, q0, q1, q2, q3))
    conn.commit()
    conn.close()

def salvar_log_serial(sim_id, tempo, valor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO serial_log (sim_id, tempo, valor)
        VALUES (?, ?, ?)
    """, (sim_id, tempo, valor))
    conn.commit()
    conn.close()
