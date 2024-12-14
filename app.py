from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

db_path = 'nombres.db'

def init_db():
    """Inicializa la base de datos SQLite y crea la tabla si no existe."""
    if not os.path.exists(db_path):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nombres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL
                )
            ''')
            # Insertar datos de ejemplo
            cursor.executemany('''
                INSERT INTO nombres (nombre) VALUES (?)
            ''', [("Juan",), ("María",), ("Carlos",)])
            conn.commit()

@app.route('/')
def home():
    """Devuelve la lista de nombres almacenados en la base de datos."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nombre FROM nombres')
        nombres = [row[0] for row in cursor.fetchall()]
    return jsonify(nombres)

if __name__ == '__main__':
    # Inicializa la base de datos antes de ejecutar la app
    init_db()
    app.run(host='0.0.0.0', port=5000)