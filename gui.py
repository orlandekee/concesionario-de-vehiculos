""" interfaz gráfica de usuario (GUI) para el concesionario de vehículos.
Esta clase maneja la visualización de datos y la interacción con el usuario."""
from tkinter import ttk
import ttkbootstrap as ttkb
import mysql.connector

class GUI:
    """
    Clase que representa la interfaz gráfica de usuario (GUI) para el concesionario de vehículos."""

    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager

        # Configurar ventana principal
        self.root.title("Interfaz de Concesionario de Vehículos")
        self.root.configure(bg="#2e3b4e")

        # Configurar estilos de Treeview
        self.style = ttk.Style()
        self.style.configure("Treeview",
                             font=("helvetica", 12),
                             rowheight=30,
                             background="#2e3b4e",
                             foreground="white",
                             borderwidth=1,
                             relief="solid")
        self.style.configure("Treeview.Heading",
                             font=("helvetica", 14, "bold"),
                             background="#4CAF50",
                             foreground="white")

        # Crear tabla para mostrar datos
        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Marca", "Modelo", "Año", "Precio",
                     "Kilometraje", "Color", "Disponibilidad", "Estado"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="x")

        # Agregar barra de desplazamiento
        scrollbar = ttkb.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botones
        self.agregar_btn = ttkb.Button(self.root, text="Agregar Vehículo", bootstyle="primary")
        self.agregar_btn.pack(pady=10)

        self.cargar_btn = ttkb.Button(self.root, text="Cargar todos los datos", bootstyle="info")
        self.cargar_btn.pack(pady=10)

    def cargar_datos(self):
        """
        Carga todos los datos de la tabla 'vehiculos' en el Treeview.
        """
        if not self.db_manager.connection:
            print("Error: No hay conexión a la base de datos.")
            return

        self.tree.delete(*self.tree.get_children())  # Limpia la tabla antes de cargar nuevos datos
        try:
            cursor = self.db_manager.connection.cursor()
            query = "SELECT * FROM vehiculos"
            cursor.execute(query)
            resultados = cursor.fetchall()
            for fila in resultados:
                self.tree.insert("", "end", values=fila)  # Inserta cada fila en el Treeview
            cursor.close()
            print("Datos cargados exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al cargar datos: {err}")
