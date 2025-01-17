import os
import logging

# Archivo para registrar errores
LOG_FILE = "error_log.log"

# Configuración de logging para añadir a un archivo
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

def log_error(filepath, line_number, message):
    """Registra un mensaje de error en el archivo log con fecha y hora."""
    if line_number is None:
        # Mensajes generales sin línea específica
        logging.error(f"{filepath}: {message}")
    else:
        # Mensajes asociados a una línea específica
        logging.error(f"{filepath} - Línea {line_number}: {message}")

def detectar_delimitador(line):
    # Detectar el delimitador más probable entre tabuladores y espacios
    if '\t' in line:
        return '\t'
    elif ' ' in line:
        return ' '
    return None

def es_numero(valor):
    # Verifica si un valor es un número válido
    try:
        float(valor)
        return True
    except ValueError:
        return False

def validar_archivo(filepath):
    with open(filepath, 'r') as file:
        # Leer el archivo
        lines = file.readlines()

        # Asegurarse de que haya al menos 3 líneas (2 encabezados + datos)
        if len(lines) < 3:
            log_error(filepath, None, "El archivo tiene menos de 3 líneas, lo cual no es válido.")
            return False

        # Ignorar las dos primeras líneas (encabezados)
        data_lines = lines[2:]

        # Determinar el delimitador a utilizar
        delimitador = None
        for line in data_lines:
            delimitador = detectar_delimitador(line.strip())
            if delimitador:
                break

        if delimitador is None:
            log_error(filepath, None, "No se pudo detectar un delimitador en el archivo.")
            return False

        # Validar consistencia de columnas y contenido de las líneas restantes
        column_counts = []
        for i, line in enumerate(data_lines, start=3):  # Línea 3 en adelante (datos)
            actual_line_number = i  # Contar desde la primera línea del archivo
            # Dividir la línea según el delimitador
            columns = line.strip().split(delimitador)

            # Contar el número de columnas
            num_columns = len(columns)

            # Verificar que el número de columnas sea consistente
            if column_counts and num_columns != column_counts[0]:
                log_error(filepath, actual_line_number, f"Número de columnas inconsistente: {line.strip()}")
                return False

            # Validar que las columnas después de la primera contengan números válidos
            for j, valor in enumerate(columns[1:], start=2):  # Comienza en la columna 2 (índice 1)
                if valor.strip() == "":
                    log_error(filepath, actual_line_number, f"Valor vacío en la columna {j}")
                    return False
                if not es_numero(valor):
                    log_error(filepath, actual_line_number, f"Valor no válido en la columna {j}: {valor}")
                    return False

            column_counts.append(num_columns)

        # Si todas las verificaciones pasaron, el archivo es válido
        return True

def validar_archivos_en_carpeta(folder_path):
    # Iterar sobre todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        # Verificar que el archivo tenga la extensión .dat
        if filename.endswith('.dat'):
            filepath = os.path.join(folder_path, filename)
            if not validar_archivo(filepath):
                log_error(filepath, None, "El archivo tiene errores de formato.")

# Ruta de la carpeta que contiene los archivos .dat
carpeta = "precip.MIROC5.RCP60.2006-2100.SDSM_REJ"  # Cambia esta ruta según corresponda
validar_archivos_en_carpeta(carpeta)
