"""
Módulo para manejar la conexión a una base de datos MySQL."""
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

        # Botones de acción
        self.agregar_btn = ttkb.Button(self.root, text="Agregar Vehículo",
                                        bootstyle="primary", command=self.agregar_vehiculo)
        self.agregar_btn.pack(pady=10)

        self.cargar_btn = ttkb.Button(self.root, text="Cargar todos los datos",
                                       bootstyle="info", command=self.cargar_datos)
        self.cargar_btn.pack(pady=10)

        self.eliminar_btn = ttkb.Button(self.root, text="Eliminar Vehículo",
                                         bootstyle="danger", command=self.eliminar_vehiculo)
        self.eliminar_btn.pack(pady=10)

        self.buscar_entry = ttkb.Entry(self.root)
        self.buscar_entry.pack(pady=10)
        self.buscar_btn = ttkb.Button(self.root, text="Buscar Vehículo", bootstyle="info",
                                    command=lambda: self.buscar_vehiculo(self.buscar_entry.get()))
        self.buscar_btn.pack(pady=10)

        self.filtrar_btn = ttkb.Button(self.root, text="Mostrar Disponibles",
                                        bootstyle="warning", command=self.filtrar_disponibles)
        self.filtrar_btn.pack(pady=10)

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

    def agregar_vehiculo(self):
        """ Agrega un nuevo vehículo a la base de datos. """
        if not self.db_manager.connection:
            print("Error: No hay conexión a la base de datos.")
            return

        # Ventana emergente para ingresar datos
        ventana = ttkb.Toplevel(self.root)
        ventana.title("Agregar Vehículo")

        campos = ["Marca", "Modelo", "Año", "Precio", "Kilometraje",
                   "Color", "Disponibilidad", "Estado"]
        entradas = {}

        for i, campo in enumerate(campos):
            label = ttkb.Label(ventana, text=campo)
            label.grid(row=i, column=0, padx=10, pady=5)
            entrada = ttkb.Entry(ventana)
            entrada.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entrada

        def guardar():
            valores = [entradas[campo].get() for campo in campos]
            try:
                cursor = self.db_manager.connection.cursor()
                query = "INSERT INTO vehiculos (marca, modelo, año, precio, kilometraje," \
                " color, disponibilidad, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, valores)
                self.db_manager.connection.commit()
                cursor.close()
                ventana.destroy()
                self.cargar_datos()  # Recargar los datos en la tabla
            except mysql.connector.Error as err:
                print(f"Error al agregar vehículo: {err}")

        btn_guardar = ttkb.Button(ventana, text="Guardar", bootstyle="success", command=guardar)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=10)

    def eliminar_vehiculo(self):
        """ Elimina el vehículo seleccionado en el Treeview. """
        seleccion = self.tree.selection()
        if not seleccion:
            print("Error: Selecciona un vehículo para eliminar.")
            return

        vehiculo_id = self.tree.item(seleccion[0])["values"][0]  # Obtener el ID del vehículo
        try:
            cursor = self.db_manager.connection.cursor()
            query = "DELETE FROM vehiculos WHERE VehiculoID = %s"
            cursor.execute(query, (vehiculo_id,))
            self.db_manager.connection.commit()
            cursor.close()
            self.cargar_datos()  # Actualizar la tabla
        except mysql.connector.Error as err:
            print(f"Error al eliminar vehículo: {err}")

    def buscar_vehiculo(self, criterio):
        """ Filtra vehículos según el criterio ingresado. """
        if not self.db_manager.connection:
            print("Error: No hay conexión a la base de datos.")
            return

        self.tree.delete(*self.tree.get_children())  # Limpiar tabla
        try:
            cursor = self.db_manager.connection.cursor()
            query = "SELECT * FROM vehiculos WHERE marca LIKE %s OR modelo LIKE %s OR año = %s"
            cursor.execute(query, (f"%{criterio}%", f"%{criterio}%", criterio))
            resultados = cursor.fetchall()
            for fila in resultados:
                self.tree.insert("", "end", values=fila)
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error al buscar vehículo: {err}")

    def filtrar_disponibles(self):
        """ Filtra solo los vehículos disponibles. """
        self.tree.delete(*self.tree.get_children())  # Limpiar tabla
        try:
            cursor = self.db_manager.connection.cursor()
            query = "SELECT * FROM vehiculos WHERE disponibilidad = 'Disponible'"
            cursor.execute(query)
            resultados = cursor.fetchall()
            for fila in resultados:
                self.tree.insert("", "end", values=fila)
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error al filtrar vehículos disponibles: {err}")
