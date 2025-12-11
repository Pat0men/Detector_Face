import sqlite3
import os

DB_PATH = os.path.join("database", "asistencia.db")

def get_connection():
    """Retorna una conexión a la base de datos."""
    return sqlite3.connect(DB_PATH)


# ========================
#  INSERTAR PERSONA
# ========================

def persona_existe(identificador: str) -> bool:
    """Retorna True si ya existe una persona con ese identificador."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM personas WHERE identificador = ?",
        (identificador,)
    )

    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def insertar_persona(nombre: str, identificador: str, ruta_foto: str) -> int:
    """
    Inserta una persona en la base.
    Retorna el ID generado.
    """

    if persona_existe(identificador):
        raise Exception(f"Ya existe una persona con el identificador '{identificador}'.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO personas (nombre, identificador, ruta_foto)
        VALUES (?, ?, ?)
        """,
        (nombre, identificador, ruta_foto)
    )

    conn.commit()
    persona_id = cursor.lastrowid
    conn.close()

    print(f"[DB] Persona insertada con ID: {persona_id}")
    return persona_id


# ========================
#  INSERTAR ENCODING
# ========================

def insertar_encoding(persona_id: int, ruta_encoding: str):
    """Asocia un encoding a una persona existente."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO encodings (persona_id, ruta_encoding)
        VALUES (?, ?)
        """,
        (persona_id, ruta_encoding)
    )

    conn.commit()
    conn.close()
    print(f"[DB] Encoding registrado correctamente para persona ID {persona_id}")


# ========================
#  CONSULTAS ÚTILES
# ========================

def obtener_persona_por_id(persona_id: int):
    """Retorna una tupla (id, nombre, identificador, ruta_foto)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM personas WHERE id = ?", (persona_id,))
    datos = cursor.fetchone()

    conn.close()
    return datos


def obtener_todos_los_encodings():
    """
    Retorna lista de (persona_id, ruta_encoding)
    Para cargarlos en el módulo de detección.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT persona_id, ruta_encoding FROM encodings")
    datos = cursor.fetchall()

    conn.close()
    return datos
