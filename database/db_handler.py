import sqlite3
from datetime import datetime

DB = "gyroai_sat.db"

def iniciar_simulacao(descricao="Simulação via GUI"):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO simulacoes (data_hora_inicio, descricao) VALUES (?, ?)", (datetime.now(), descricao))
    conn.commit()
    sim_id = cursor.lastrowid
    conn.close()
    return sim_id

def salvar_dado_gyro(sim_id, tempo, velocidade):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dados_gyro (simulacao_id, tempo, velocidade_angular) VALUES (?, ?, ?)",
                   (sim_id, tempo, velocidade))
    conn.commit()
    conn.close()

def salvar_quaternion(sim_id, tempo, q0, q1, q2, q3):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dados_quaternions (simulacao_id, tempo, q0, q1, q2, q3) VALUES (?, ?, ?, ?, ?, ?)",
                   (sim_id, tempo, q0, q1, q2, q3))
    conn.commit()
    conn.close()

def salvar_log_serial(sim_id, mensagem):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO serial_log (simulacao_id, timestamp, mensagem) VALUES (?, ?, ?)",
                   (sim_id, datetime.now(), mensagem))
    conn.commit()
    conn.close()
