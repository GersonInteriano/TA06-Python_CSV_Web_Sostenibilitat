import os
import numpy as np
import pandas as pd
import logging

# Configuración del logger
logging.basicConfig(filename='error_log.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def calcular_estadisticas(directorio):
    if not os.path.exists(directorio):
        logging.error(f"El directorio {directorio} no existe. El programa ha finalizado.")
        return

    datos_anuales = {}
    datos_faltantes = 0
    total_datos = 0

    for archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, archivo)
        if os.path.isfile(ruta_archivo):
            try:
                # Leer el archivo con pandas
                df = pd.read_csv(ruta_archivo, skiprows=2, delim_whitespace=True, header=None)
                anyo_col = df[1]
                valores_cols = df.iloc[:, 3:]

                for anyo, valores in zip(anyo_col, valores_cols.values):
                    if anyo not in datos_anuales:
                        datos_anuales[anyo] = []

                    valores = np.array([int(x) for x in valores])
                    datos_anuales[anyo].extend(valores)
                    datos_faltantes += np.sum(valores == -999)
                    total_datos += len(valores)
            except Exception as e:
                logging.error(f"Error processing file {ruta_archivo}: {e}")

    # Calcular estadísticas
    try:
        porcentaje_faltantes = (datos_faltantes / total_datos) * 100
        estadisticas = {}
        for anyo, valores in datos_anuales.items():
            valores = np.array(valores)
            valores_validos = valores[valores != -999]
            total_mm = np.sum(valores_validos)
            media_mm = np.mean(valores_validos)
            desviacion_estandar_mm = np.std(valores_validos)
            coeficiente_variacion = desviacion_estandar_mm / media_mm

            estadisticas[anyo] = {
                'total_mm': total_mm,
                'total_m': total_mm / 1000,
                'media_mm': media_mm,
                'media_m': media_mm / 1000,
                'desviacion_estandar_mm': desviacion_estandar_mm,
                'desviacion_estandar_m': desviacion_estandar_mm / 1000,
                'coeficiente_variacion': coeficiente_variacion
            }

        tendencia_cambio = {
            anyo: estadisticas[anyo]['total_mm'] - estadisticas[anyo-1]['total_mm']
            for anyo in sorted(estadisticas.keys())[1:]
        }
        anyo_mas_plujoso = max(estadisticas, key=lambda x: estadisticas[x]['total_mm'])
        anyo_mas_sec = min(estadisticas, key=lambda x: estadisticas[x]['total_mm'])

        # Mostrar resultados
        print("Estadísticas generales:")
        print("----------------------------------------")
        print(f"Total de datos faltantes: {datos_faltantes}")
        print(f"Total de datos: {total_datos}")
        print(f"Porcentaje de datos faltantes: {porcentaje_faltantes:.2f}%")
        print("Estadísticas anuales:")
        print("---------------------")
        for anyo, stats in estadisticas.items():
            print(f"Año {anyo}: Total = {stats['total_mm']} mm ({stats['total_m']} m), Media = {stats['media_mm']:.2f} mm ({stats['media_m']:.2f} m), Desviación Estándar = {stats['desviacion_estandar_mm']:.2f} mm ({stats['desviacion_estandar_m']:.2f} m), Coeficiente de Variación = {stats['coeficiente_variacion']:.2f}")
        print("Tendencia de cambio anual:")
        print("---------------------------")
        for anyo, cambio in tendencia_cambio.items():
            print(f"Año {anyo}: Cambio = {cambio} mm")
        print("---------------------------------------")
        print(f"Any més plujós: {anyo_mas_plujoso} con {estadisticas[anyo_mas_plujoso]['total_mm']} mm ({estadisticas[anyo_mas_plujoso]['total_m']} m)")
        print(f"Any més sec: {anyo_mas_sec} con {estadisticas[anyo_mas_sec]['total_mm']} mm ({estadisticas[anyo_mas_sec]['total_m']} m)")
    except Exception as e:
        logging.error(f"Error calculating statistics: {e}")

# Ejemplo de uso
directorio = os.path.join(os.path.dirname(__file__), 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ')
calcular_estadisticas(directorio)
