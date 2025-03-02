import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="punto_venta"
    )

def ejecutar_consulta(query, valores=None):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(query, valores)
        conexion.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conexion.close()