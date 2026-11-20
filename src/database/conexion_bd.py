import mysql.connector


class ConexionBD:
    """Fábrica de conexiones hacia la base de datos bd_molino_arroz."""

    @staticmethod
    def obtener_conexion():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="bd_molino_arroz"
        )
