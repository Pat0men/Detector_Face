import sqlite3

def crear_tablas():
    conn = sqlite3.connect("asistencia.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        identificador TEXT UNIQUE NOT NULL,
        ruta_foto TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS encodings (
        id_encoding INTEGER PRIMARY KEY AUTOINCREMENT,
        id_persona INTEGER NOT NULL,
        ruta_encoding TEXT NOT NULL,
        FOREIGN KEY (id_persona) REFERENCES personas(id_persona)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencia (
        id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_persona INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        FOREIGN KEY (id_persona) REFERENCES personas(id_persona)
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos creada correctamente.")