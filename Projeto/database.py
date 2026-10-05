import sqlite3
from werkzeug.security import generate_password_hash


def conectar():

    return sqlite3.connect("usuarios.db")


def criar_tabelas():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE,
            senha TEXT,
            role TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            action TEXT,
            details TEXT,
            ip TEXT,
            created_at TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT,
            tipo_recurso TEXT,
            valor_emergetico REAL,
            data_registro TEXT,
            criado_por TEXT
        )
        """
    )

    conexao.commit()

    conexao.close()


def criar_usuarios_teste():

    conexao = conectar()

    cursor = conexao.cursor()

    usuarios = [
        ("admin", generate_password_hash("123"), "admin"),
        ("user", generate_password_hash("123"), "user")
    ]

    for u in usuarios:

        try:

            cursor.execute(
                "INSERT INTO usuarios (login, senha, role) VALUES (?, ?, ?)",
                u
            )

        except sqlite3.IntegrityError:

            pass

    conexao.commit()

    conexao.close()