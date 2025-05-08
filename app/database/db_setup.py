# Criação e estrutura das tabelas

import sqlite3
import os

# Define caminho absoluto para criar o banco na raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../gyroai.db'))

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela 1 - Simulações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Tabela 2 - Dados do Giroscópio
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_gyro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sim_id INTEGER,
            tempo REAL,
            omega_x REAL,
            omega_y REAL,
            omega_z REAL,
            FOREIGN KEY (sim_id) REFERENCES simulacoes(id)
        );
    """)

    # Tabela 3 - Quaternions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_quaternions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sim_id INTEGER,
            tempo REAL,
            q0 REAL,
            q1 REAL,
            q2 REAL,
            q3 REAL,
            FOREIGN KEY (sim_id) REFERENCES simulacoes(id)
        );
    """)

    # Tabela 4 - Log serial
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS serial_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sim_id INTEGER,
            tempo REAL,
            valor TEXT,
            FOREIGN KEY (sim_id) REFERENCES simulacoes(id)
        );
    """)

    # Tabela 5 - Dados orbitais (posição, velocidade, ângulos de Euler)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_orbitais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sim_id INTEGER,
            tempo REAL,
            x_km REAL,
            y_km REAL,
            z_km REAL,
            vx_km_s REAL,
            vy_km_s REAL,
            vz_km_s REAL,
            roll_deg REAL,
            pitch_deg REAL,
            yaw_deg REAL,
            tipo_dado TEXT DEFAULT 'simulado',
            FOREIGN KEY (sim_id) REFERENCES simulacoes(id)
        );
    """)

    conn.commit()
    conn.close()
