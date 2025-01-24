import os
import logging

LOG_FILE = "error_log.log"

logging.basicConfig(filename=LOG_FILE, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

def log_error(filepath, line_number, message):
    if line_number is None:
        logging.error(f"{filepath}: {message}")
    else:
        logging.error(f"{filepath} - Línea {line_number}: {message}")

def detectar_delimitador(line):
    if '\t' in line:
        return '\t'
    elif ' ' in line:
        return ' '
    return None

def es_numero(valor):
    try:
        valor = valor.replace(',', '.')
        float(valor)
        return True
    except ValueError:
        return False

def tiene_decimales(valor):
    try:
        numero = float(valor.replace(',', '.'))
        return numero != int(numero)
    except ValueError:
        return False

def validar_archivo(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

        if len(lines) < 3:
            log_error(filepath, None, "El archivo tiene menos de 3 líneas, lo cual no es válido.")
            return False

        data_lines = lines[2:]

        delimitador = None
        for line in data_lines:
            delimitador = detectar_delimitador(line.strip())
            if delimitador:
                break

        if delimitador is None:
            log_error(filepath, None, "No se pudo detectar un delimitador en el archivo.")
            return False

        column_counts = []
        meses_contados = 0
        for i, line in enumerate(data_lines, start=3):
            actual_line_number = i
            columns = line.strip().split(delimitador)

            num_columns = len(columns)

            if column_counts and num_columns != column_counts[0]:
                log_error(filepath, actual_line_number, f"Número de columnas inconsistente: {line.strip()}")
                return False

            for j, valor in enumerate(columns[1:], start=2):
                if valor.strip() == "":
                    log_error(filepath, actual_line_number, f"Valor vacío en la columna {j}")
                    return False
                if not es_numero(valor):
                    log_error(filepath, actual_line_number, f"Valor no válido en la columna {j}: {valor}")
                    return False

                if tiene_decimales(valor):
                    log_error(filepath, actual_line_number, f"Valor con decimales no permitido en la columna {j}: {valor}")
                    return False

            meses_contados += 1
            if meses_contados == 12:
                meses_contados = 0

            column_counts.append(num_columns)

        if meses_contados != 0:
            log_error(filepath, None, f"El archivo no tiene 12 meses completos para el año. Se encontraron {meses_contados} meses.")
            return False

        return True

def validar_archivos_en_carpeta(folder_path):
    if not os.path.exists(folder_path):
        log_error(folder_path, None, "El directorio no existe. El programa ha finalizado.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith('.dat'):
            filepath = os.path.join(folder_path, filename)
            if not validar_archivo(filepath):
                log_error(filepath, None, "El archivo tiene errores de formato.")

carpeta = os.path.join(os.path.dirname(__file__), 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ')
validar_archivos_en_carpeta(carpeta)