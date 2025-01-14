import os

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
        # Leer solo las primeras 10 líneas del archivo
        lines = []
        for i, line in enumerate(file):
            if i >= 10:  # Detener la lectura después de las 10 líneas
                break
            lines.append(line)

        # Asegurarse de que haya al menos 3 líneas (2 encabezados + datos)
        if len(lines) < 3:
            print(f"El archivo {filepath} tiene menos de 3 líneas, lo cual no es válido.")
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
            print(f"No se pudo detectar un delimitador en el archivo {filepath}.")
            return False

        # Validar consistencia de columnas y contenido de las 8 líneas restantes
        column_counts = []
        for i, line in enumerate(data_lines, start=3):  # Línea 3 en adelante (datos)
            # Dividir la línea según el delimitador
            columns = line.strip().split(delimitador)

            # Contar el número de columnas
            num_columns = len(columns)

            # Verificar que el número de columnas sea consistente
            if column_counts and num_columns != column_counts[0]:
                print(
                    f"El archivo {filepath} tiene un número de columnas inconsistente en la línea {i}: {line.strip()}")
                return False

            # Validar que las columnas después de la primera contengan números válidos
            for valor in columns[1:]:
                if not es_numero(valor):
                    print(
                        f"El archivo {filepath} tiene un valor no válido en la línea {i}: {valor}")
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
                print(f"El archivo {filename} tiene errores de formato.")
            else:
                print(f"El archivo {filename} es válido.")


# Ruta de la carpeta que contiene los archivos .dat
carpeta = "precip.MIROC5.RCP60.2006-2100.SDSM_REJ"  # Cambia esta ruta según corresponda
validar_archivos_en_carpeta(carpeta)
