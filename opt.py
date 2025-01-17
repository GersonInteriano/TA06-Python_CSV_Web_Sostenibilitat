import os
import pandas as pd
import numpy as np

def calcular_estadisticas(directorio):
    """
    Calcula estadísticas climáticas a partir de archivos de datos en un directorio.

    Args:
        directorio: Ruta al directorio que contiene los archivos de datos.

    Returns:
        None
    """

    # Unidad de medida de la precipitación
    unidad_precipitacion = "mm"

    # Inicializar contadores
    total_valores_procesados = 0
    valores_faltantes = 0
    archivos_procesados = 0
    lineas_procesadas = 0

    # Leer todos los archivos en un DataFrame
    all_data = []
    for archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, archivo)
        df = pd.read_csv(ruta_archivo, skiprows=2, sep=' ', header=None,
                         usecols=[1, 3], names=['año', 'precipitacion'], dtype={'año': int, 'precipitacion': np.float64})
        all_data.append(df)

        # Actualizar contadores
        archivos_procesados += 1
        lineas_procesadas += len(df)
        total_valores_procesados += df.shape[0] * df.shape[1]
        valores_faltantes += df['precipitacion'].isna().sum()

    # Concatenar todos los DataFrames en uno solo
    df_total = pd.concat(all_data, ignore_index=True)

    # Calcular estadísticas agrupando por año
    estadisticas = df_total.groupby('año')['precipitacion'].agg(
        total_mm=lambda x: x.sum(),
        total_m=lambda x: x.sum() / 1000,
        media_mm=lambda x: x.mean(),
        media_m=lambda x: x.mean() / 1000,
        desviacion_estandar_mm=lambda x: x.std(),
        desviacion_estandar_m=lambda x: x.std() / 1000,
        coeficiente_variacion=lambda x: x.std() / x.mean()
    )

    # Calcular la tendencia de cambio anual
    tendencia_cambio = estadisticas['total_mm'].diff()
    anyo_mas_plujoso = estadisticas['total_mm'].idxmax()
    anyo_mas_seco = estadisticas['total_mm'].idxmin()

    # Mostrar resultados
    print(f"Porcentaje de datos faltantes: {df_total['precipitacion'].isna().mean() * 100:.2f}%")
    print(f"Valores faltantes: {valores_faltantes}")
    print(f"Total de valores procesados: {total_valores_procesados}")
    print(f"Archivos procesados: {archivos_procesados}")
    print(f"Líneas procesadas: {lineas_procesadas}")
    print("Estadísticas anuales:")
    print(estadisticas)
    print("\nTendencia de cambio anual (mm):")
    print(tendencia_cambio)
    print(f"\nAño más plujoso: {anyo_mas_plujoso} con {estadisticas.loc[anyo_mas_plujoso, 'total_mm']} mm ({estadisticas.loc[anyo_mas_plujoso, 'total_m']} m)")
    print(f"Año más seco: {anyo_mas_seco} con {estadisticas.loc[anyo_mas_seco, 'total_mm']} mm ({estadisticas.loc[anyo_mas_seco, 'total_m']} m)")

# Ejemplo de uso
calcular_estadisticas('precip.MIROC5.RCP60.2006-2100.SDSM_REJ')