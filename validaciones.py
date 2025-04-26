"""
Módulo de validaciones para la gestión de vehículos."""
def validar_campos(datos):
    """
    Valida los campos de entrada antes de agregar un vehículo.
    :param datos: Diccionario con los datos a validar.
    :return: True si los datos son válidos, False si no.
    """
    marca, modelo, ano, precio, kilometraje, color, disponibilidad, estado = (
        datos.get("marca", "").strip(),
        datos.get("modelo", "").strip(),
        datos.get("ano", "").strip(),
        datos.get("precio", "").strip(),
        datos.get("kilometraje", "").strip(),
        datos.get("color", "").strip(),
        datos.get("disponibilidad", "").strip(),
        datos.get("estado", "").strip().lower(),
    )

    # Validar campos vacíos
    if not marca or not modelo or not color:
        print("Error: Los campos Marca, Modelo y Color no pueden estar vacíos.")
        return False

    # Validar año (número y rango lógico)
    if not ano.isdigit() or int(ano) < 1900 or int(ano) > 2025:
        print("Error: El año debe ser un número entre 1900 y 2025.")
        return False

    # Validar precio (número positivo)
    if not precio.isdigit() or int(precio) <= 0:
        print("Error: El precio debe ser un número positivo.")
        return False

    # Validar kilometraje (número positivo)
    if not kilometraje.isdigit() or int(kilometraje) < 0:
        print("Error: El kilometraje debe ser un número positivo.")
        return False

    # Validar disponibilidad (número positivo)
    if not disponibilidad.isdigit() or int(disponibilidad) < 0:
        print("Error: La disponibilidad debe ser un número positivo.")
        return False

    # Validar estado (solo "nuevo" o "usado")
    if estado not in ["nuevo", "usado"]:
        print("Error: El estado debe ser 'nuevo' o 'usado'.")
        return False

    # Si todas las validaciones pasan
    return True
