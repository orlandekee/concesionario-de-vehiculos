"""
Archivo principal del proyecto 'Concesionario de Vehículos'.

Este módulo sirve como punto de entrada para la aplicación. Inicializa la conexión
a la base de datos, configura la interfaz gráfica (GUI) y ejecuta el bucle principal
de la aplicación.

Clases y funciones principales:
- DatabaseManager: Clase para manejar la conexión con la base de datos.
- ConcesionarioGUI: Clase para la interfaz gráfica de usuario.
- main: Punto de entrada que inicializa y ejecuta la aplicación.
"""
from database_manager import DatabaseManager
from gui import GUI
import ttkbootstrap as ttkb

# Crear instancia de DatabaseManager
db_manager = DatabaseManager(
    host="localhost",
    user="root",
    password="123456789",
    database="concesionario_de_vehiculos"
)

# Crear ventana principal
root = ttkb.Window(themename="darkly")
gui = GUI(root, db_manager)

# Configurar botones
gui.cargar_btn.configure(command=gui.cargar_datos)

# Configurar cierre de ventana
root.protocol("WM_DELETE_WINDOW", lambda: [db_manager.cerrar_conexion(), root.destroy()])

# Iniciar loop principal
root.mainloop()