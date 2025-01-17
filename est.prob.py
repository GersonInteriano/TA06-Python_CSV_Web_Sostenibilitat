import os
import numpy as np

def calcular_estadisticas(directorio):
    datos_anuales = {}
    datos_faltantes = 0
    total_datos = 0

    for archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, archivo)
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r', encoding='utf-8') as fitxer:
                lineas = fitxer.readlines()[2:]  # Ignorar las dos primeras líneas

                for linea in lineas:
                    datos = linea.strip().split()
                    anyo = int(datos[1])
                    valores = np.array([int(x) for x in datos[3:]])

                    if anyo not in datos_anuales:
                        datos_anuales[anyo] = []

                    datos_anuales[anyo].extend(valores)
                    datos_faltantes += np.sum(valores == -999)
                    total_datos += len(valores)

    # Calcular estadísticas
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
    print(f"Total de datos faltantes: {datos_faltantes}")
    print(f"Total de datos: {total_datos}")
    print(f"Porcentaje de datos faltantes: {porcentaje_faltantes:.2f}%")
    print("Estadísticas anuales:")
    for anyo, stats in estadisticas.items():
        print(f"Año {anyo}: Total = {stats['total_mm']} mm ({stats['total_m']} m), Media = {stats['media_mm']:.2f} mm ({stats['media_m']:.2f} m), Desviación Estándar = {stats['desviacion_estandar_mm']:.2f} mm ({stats['desviacion_estandar_m']:.2f} m), Coeficiente de Variación = {stats['coeficiente_variacion']:.2f}")
    print("Tendencia de cambio anual:")
    for anyo, cambio in tendencia_cambio.items():
        print(f"Año {anyo}: Cambio = {cambio} mm")
    print(f"Any més plujós: {anyo_mas_plujoso} con {estadisticas[anyo_mas_plujoso]['total_mm']} mm ({estadisticas[anyo_mas_plujoso]['total_m']} m)")
    print(f"Any més sec: {anyo_mas_sec} con {estadisticas[anyo_mas_sec]['total_mm']} mm ({estadisticas[anyo_mas_sec]['total_m']} m)")

# Ejemplo de uso
calcular_estadisticas('precip.MIROC5.RCP60.2006-2100.SDSM_REJ')