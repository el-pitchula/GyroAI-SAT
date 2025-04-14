import sqlite3

def create_db():
    conn = sqlite3.connect("gyroai_sat.db")
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS simulacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora_inicio DATETIME,
        data_hora_fim DATETIME,
        descricao TEXT
    );

    CREATE TABLE IF NOT EXISTS dados_gyro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        simulacao_id INTEGER,
        tempo REAL,
        velocidade_angular REAL,
        FOREIGN KEY (simulacao_id) REFERENCES simulacoes(id)
    );

    CREATE TABLE IF NOT EXISTS dados_quaternions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        simulacao_id INTEGER,
        tempo REAL,
        q0 REAL,
        q1 REAL,
        q2 REAL,
        q3 REAL,
        FOREIGN KEY (simulacao_id) REFERENCES simulacoes(id)
    );

    CREATE TABLE IF NOT EXISTS serial_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        simulacao_id INTEGER,
        timestamp DATETIME,
        mensagem TEXT,
        FOREIGN KEY (simulacao_id) REFERENCES simulacoes(id)
    );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
