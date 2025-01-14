import os
import pandas as pd
# Ruta de la carpeta que contiene los archivos
carpeta = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'

# Lista para almacenar los resultados de la validación
resultados = []

# Recorre los archivos en la carpeta
for archivo in os.listdir(carpeta):
    # Verifica si el archivo es un archivo de texto
    if archivo.endswith('.txt') or archivo.endswith('.csv'):
        # Lee las primeras 10 líneas del archivo
        with open(os.path.join(carpeta, archivo), 'r') as f:
            lineas = [f.readline().strip() for _ in range(10)]

        # Intenta leer el archivo con pandas
        try:
            df = pd.read_csv(os.path.join(carpeta, archivo), nrows=10)
            # Verifica el número de columnas y delimitadores
            num_columnas = len(df.columns)
            delimitador = ',' if ',' in lineas[0] else '\t'
            resultados.append((archivo, num_columnas, delimitador))
        except pd.errors.EmptyDataError:
            # Si el archivo está vacío, agrega un mensaje de error
            resultados.append((archivo, 'Archivo vacío', ''))
        except pd.errors.ParserError:
            # Si hay un error al parsear el archivo, agrega un mensaje de error
            resultados.append((archivo, 'Error al parsear', ''))

# Imprime los resultados
for archivo, num_columnas, delimitador in resultados:
    print(f'Archivo: {archivo}')
    print(f'Número de columnas: {num_columnas}')
    print(f'Delimitador: {delimitador}')
    print('---')