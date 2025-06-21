"""
Módulo para la conexión a una base de datos MySQL."""

import mysql.connector

class DatabaseManager:
    """
    Clase que maneja la conexión a una base de datos MySQL.

    Proporciona métodos para establecer y cerrar la conexión con la base de datos,
    así como para manejar errores de conexión.
    """
    def __init__(self, host, user, password, database):
        """Establece la conexión con la base de datos MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos.")
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            self.connection = None

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")
