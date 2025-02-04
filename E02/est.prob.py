import glob
import os
import numpy as np
import statistics
import csv
import matplotlib.pyplot as plt

# ------------------------------
# CONFIGURACIÓN DEL DIRECTORIO
# ------------------------------
# Ajusta la ruta donde se encuentran los archivos .dat.
# Ejemplo en Windows:
directorio = r"../E01/precip.MIROC5.RCP60.2006-2100.SDSM_REJ"
# Ejemplo en Linux/Mac:
# directorio = "/home/usuario/carpeta"

# Nombre del archivo CSV de salida
csv_salida = "estadisticos_anuales.csv"

# Construir la ruta para buscar archivos .dat en el directorio
ruta_archivos = os.path.join(directorio, "*.dat")

# ---------------------------------------------------------------
# Paso 1. Leer cada archivo y acumular, por estación, los totales
#         anuales. Cada archivo (estación) puede tener datos de varios años.
# ---------------------------------------------------------------
# Estructura: totales_por_año = { "2006": [total_estacion1, total_estacion2, ...],
#                                   "2007": [ ... ], ... }
totales_por_año = {}

for archivo in glob.glob(ruta_archivos):
    # Diccionario para acumular el total anual en el archivo actual (por estación)
    totales_estacion = {}

    with open(archivo, "r", encoding="utf-8") as f:
        # Leer todas las líneas y descartar las dos primeras (cabecera y metadatos)
        lineas = f.readlines()[2:]

    # Procesar cada línea (cada una corresponde a un mes)
    for linea in lineas:
        tokens = linea.split()
        # Verificar que la línea tenga al menos: ID, año, mes y valores diarios
        if len(tokens) < 4:
            continue

        # Extraer año (token 1)
        año = tokens[1]

        # Sumar los valores diarios (tokens a partir del índice 3), ignorando -999
        suma_mes = 0.0
        for valor in tokens[3:]:
            try:
                lluvia = float(valor)
            except ValueError:
                continue
            if lluvia == -999:
                continue
            suma_mes += lluvia

        # Acumular la suma mensual en el total anual para este archivo
        totales_estacion[año] = totales_estacion.get(año, 0.0) + suma_mes

    # Para cada año encontrado en este archivo, agregar el total (en décimas)
    # a la lista global (cada elemento de la lista corresponde a una estación)
    for año, total in totales_estacion.items():
        totales_por_año.setdefault(año, []).append(total)

# -------------------------------------------------------------------
# Paso 2. Calcular estadísticos anuales (convertir de décimas a l/m²)
# -------------------------------------------------------------------
# Se crea un diccionario con la siguiente estructura:
# estadisticos_por_año = { "2006": { 'media': ..., 'total': ...,
#                                    'desviacion': ..., 'cv': ... },
#                          "2007": { ... }, ... }
estadisticos_por_año = {}

for año, lista_totales in totales_por_año.items():
    # Convertir cada total (en décimas) a l/m² dividiendo entre 10
    valores = [v / 10 for v in lista_totales]

    # Calcular la media y el total acumulado
    media = sum(valores) / len(valores)
    total = sum(valores)

    # Calcular desviación estándar y coeficiente de variación (si hay al menos 2 datos)
    if len(valores) > 1:
        desv_std = statistics.stdev(valores)
        cv = (desv_std / media * 100) if media != 0 else 0
    else:
        desv_std = 0.0
        cv = 0.0

    estadisticos_por_año[año] = {
        'media': media,
        'total': total,
        'desviacion': desv_std,
        'cv': cv
    }

# -------------------------------------------------------------------
# Paso 3. Calcular la tendencia de cambio anual mediante regresión lineal
#         Usamos los promedios anuales y los años (convertidos a int)
# -------------------------------------------------------------------
años_ordenados = sorted(estadisticos_por_año.keys(), key=lambda a: int(a))
x = np.array([int(año) for año in años_ordenados])
y = np.array([estadisticos_por_año[año]['media'] for año in años_ordenados])

if len(x) > 1:
    pendiente, intercepto = np.polyfit(x, y, 1)
else:
    pendiente, intercepto = 0.0, y[0] if len(y) > 0 else 0.0

# -------------------------------------------------------------------
# Paso 4. Identificar el año más lluvioso y el año más seco
#         (según el total acumulado)
# -------------------------------------------------------------------
año_mas_lluvioso = max(estadisticos_por_año.items(), key=lambda item: item[1]['total'])[0]
año_mas_seco = min(estadisticos_por_año.items(), key=lambda item: item[1]['total'])[0]

# -------------------------------------------------------------------
# Paso 5. Exportar los resultados a un archivo CSV y mostrarlos por pantalla
# -------------------------------------------------------------------
csv_ruta = os.path.join(directorio, csv_salida)
with open(csv_ruta, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # Escribir el encabezado del CSV
    writer.writerow(
        ["Año", "Media (l/m²)", "Total (l/m²)", "Desviación estándar (l/m²)", "Coeficiente de variación (%)"])

    # Imprimir y escribir cada fila de datos
    print("Estadísticos anuales de precipitación (en l/m²):\n")
    for año in años_ordenados:
        datos = estadisticos_por_año[año]
        fila = [
            año,
            f"{datos['media']:.2f}",
            f"{datos['total']:.2f}",
            f"{datos['desviacion']:.2f}",
            f"{datos['cv']:.2f}"
        ]
        writer.writerow(fila)
        print(f"Año {año}:")
        print(f"  Media: {datos['media']:.2f} l/m²")
        print(f"  Total: {datos['total']:.2f} l/m²")
        print(f"  Desviación estándar: {datos['desviacion']:.2f} l/m²")
        print(f"  Coeficiente de variación: {datos['cv']:.2f}%\n")

print("Tendencia de cambio anual (usando media anual):")
print(f"  Pendiente de la regresión: {pendiente:.2f} l/m² por año\n")

print("Resumen global:")
print(f"  Año más lluvioso: {año_mas_lluvioso} (Total: {estadisticos_por_año[año_mas_lluvioso]['total']:.2f} l/m²)")
print(f"  Año más seco: {año_mas_seco} (Total: {estadisticos_por_año[año_mas_seco]['total']:.2f} l/m²)")

print(f"\nLos resultados se han exportado a '{csv_ruta}'.")

# -------------------------------------------------------------------
# Paso 6. Generar gráficos estadísticos y exportarlos en formato PNG
# -------------------------------------------------------------------

# Convertir años ordenados a enteros para los gráficos
x_years = [int(a) for a in años_ordenados]

# Listas con los valores a graficar
totales_anuales = [estadisticos_por_año[a]['total'] for a in años_ordenados]
medias_anuales = [estadisticos_por_año[a]['media'] for a in años_ordenados]
desviaciones = [estadisticos_por_año[a]['desviacion'] for a in años_ordenados]

# Gráfico 1: Totales anuales (barras) - Versión mejorada
plt.figure(figsize=(18, 8))

# Calcular el paso para mostrar años (mostrar cada 5, 10, o más años según cantidad)
num_años = len(años_ordenados)
if num_años > 50:
    paso = 10
elif num_años > 20:
    paso = 5
else:
    paso = 1

# Crear lista de años a mostrar
indices_seleccionados = range(0, num_años, paso)
años_a_mostrar = [años_ordenados[i] for i in indices_seleccionados]

# Crear el gráfico de barras con espacio entre ellas
bars = plt.bar(
    range(num_años),  # Usar índices numéricos para posicionamiento
    totales_anuales,
    color='skyblue',
    edgecolor='grey',
    width=0.7  # Reducir ancho de barras para aumentar espacio
)

# Ajustar etiquetas eje X
plt.xticks(
    indices_seleccionados,  # Posiciones
    años_a_mostrar,         # Etiquetas
    rotation=45,
    ha='right',
    fontsize=10
)

# Líneas de guía verticales opcionales
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))

# Formato profesional
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Etiquetas y título
plt.xlabel("Año", fontsize=12, labelpad=10)
plt.ylabel("Total Precipitación (l/m²)", fontsize=12, labelpad=10)
plt.title("Total Precipitación Anual", fontsize=14, pad=20)

# Guardar con alta resolución
grafico_total = os.path.join(directorio, "total_precipitacion_anual.png")
plt.savefig(grafico_total, dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 2: Media anual con error bars (desviación) y línea de tendencia
plt.figure(figsize=(10, 6))
plt.errorbar(x_years, medias_anuales, yerr=desviaciones, fmt='o', capsize=5, label='Media anual')
# Línea de regresión (tendencia)
x_line = np.linspace(min(x_years), max(x_years), 100)
y_line = pendiente * x_line + intercepto
plt.plot(x_line, y_line, 'r-', label=f"Regresión (pendiente = {pendiente:.2f})")
plt.xlabel("Año")
plt.ylabel("Media Precipitación (l/m²)")
plt.title("Media Precipitación Anual y Tendencia")
plt.legend()
grafico_media = os.path.join(directorio, "media_precipitacion_anual.png")
plt.savefig(grafico_media, dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# Gráfico 3: Desviación Estándar anual
# -------------------------------
plt.figure(figsize=(18, 8))
plt.bar(
    range(num_años),
    desviaciones,
    color='lightgreen',
    edgecolor='grey',
    width=0.7
)
plt.xticks(
    indices_seleccionados,
    [años_ordenados[i] for i in indices_seleccionados],
    rotation=45,
    ha='right',
    fontsize=10
)
plt.xlabel("Año", fontsize=12, labelpad=10)
plt.ylabel("Desviación Estándar (l/m²)", fontsize=12, labelpad=10)
plt.title("Desviación Estándar de Precipitación Anual", fontsize=14, pad=20)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
grafico_desviacion = os.path.join(directorio, "desviacion_estandar_anual.png")
plt.savefig(grafico_desviacion, dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------
# Gráfico 4: Coeficiente de Variación anual
# -------------------------------
coef_variacion = [estadisticos_por_año[a]['cv'] for a in años_ordenados]
plt.figure(figsize=(18, 8))
plt.bar(
    range(num_años),
    coef_variacion,
    color='salmon',
    edgecolor='grey',
    width=0.7
)
plt.xticks(
    indices_seleccionados,
    [años_ordenados[i] for i in indices_seleccionados],
    rotation=45,
    ha='right',
    fontsize=10
)
plt.xlabel("Año", fontsize=12, labelpad=10)
plt.ylabel("Coeficiente de Variación (%)", fontsize=12, labelpad=10)
plt.title("Coeficiente de Variación de Precipitación Anual", fontsize=14, pad=20)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
grafico_cv = os.path.join(directorio, "coeficiente_variacion_anual.png")
plt.savefig(grafico_cv, dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------
# Gráfico 5: Comparación entre el Año más Lluvioso y el Año más Seco
#         (se compara únicamente el total de precipitación)
# -----------------------------------------------------------
total_lluvioso = estadisticos_por_año[año_mas_lluvioso]['total']
total_seco = estadisticos_por_año[año_mas_seco]['total']

# Posiciones para cada barra
etiquetas = [f"Año {año_mas_lluvioso}", f"Año {año_mas_seco}"]
valores = [total_lluvioso, total_seco]

plt.figure(figsize=(8, 6))
bars = plt.bar(etiquetas, valores, color=['blue', 'orange'], edgecolor='grey', width=0.5)
plt.ylabel("Total Precipitación (l/m²)")
plt.title("Comparación: Año más lluvioso vs. Año más seco (Total de precipitación)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

grafico_comparacion = os.path.join(directorio, "comparacion_lluvioso_seco.png")
plt.savefig(grafico_comparacion, dpi=300, bbox_inches='tight')
plt.close()

print(f"Los gráficos se han exportado como:\n  {grafico_total}\n  {grafico_media}\n  {grafico_desviacion}\n  {grafico_cv}\n  {grafico_comparacion}")
