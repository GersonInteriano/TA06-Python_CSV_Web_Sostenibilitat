# Script de Validación de Datos

Script para validar archivos de datos y asegurarse que cumplen con el formato esperado y si los datos son correctos y no provocan ningun tpo de error.

## Pas 1

### 1. Configuración de Logging
Configurar un registro de errores que guarda los mensajes de error en el archivo `error_log.log`, utilizando la función logging facilitamos el trabajo.

### 2. Función `revisar_format`
Creamos una función que verifica si el archivo tiene la extensión `.dat`, para eso utilizamos el *endswith*, que mira solo el final del nombre, ignorando el resto.

### 3. Función `llegir_fitxer`
Lee un archivo y detecta el delimitador utilizado en el archivo.
- Primero abrimos el archivo en modo lectura.
- Leemos las primeras 10 líneas del archivo para identificar el delimitador.
  - Si no se encuentra un delimitador, se asume que es un espacio.
    -   Si no se encuentra un delimitador, se asume que es un espacio.
  - Si se encuentra un delimitador, se guarda en la variable `delimitador`.
 
### 4. Función `hi_ha_comentaris`
Comprueba si el archivo contiene comentarios que empiezan con `#`, para eso utilizamos el *startswith*.
- Si encuentra un comentario, lo ignora y sigue leyendo el archivo.
- Si no encuentra un comentario, sigue leyendo el archivo.
- Si encuentra un comentario después de haber leído los datos, se detiene la lectura.

### 5. Función `revisar_capcaleres`
Válida que la primera fila de encabezado sea idéntica en todos los archivos y que la segunda fila tenga el formato correcto.
- Para esto, primero leemos las primeras dos líneas del archivo.
- Luego, comparamos la primera fila de encabezado con la primera fila de encabezado de los otros archivos.
- Comparamos la segunda fila de encabezado con el formato esperado.
- Si no se cumple alguna de las condiciones, se muestra un mensaje de error.
- Si se cumple, se muestra un mensaje de éxito.
 
### 6. Función `processar_fitxers`
Procesa todos los archivos `.dat` en el directorio especificado:
- Lee los archivos.
- Verifica la extensión del archivo.
- Detecta el delimitador (coma, tabulación o espacio).
- Revisa si hay comentarios.
- Comprueba que los encabezados sean consistentes.

### 7. Función `main`
Función principal que ejecuta el script.
 
---

## Pas2

Script que valida si los datos de los archivos .dat son correctos y en caso de no serlos enviar el error a  a error_log.log

### 1. Configuración de Logging
Configurar un registro de errores que guarda los mensajes de error en el archivo `error_log.log`.

### 2. Función `detectar_delimitador`
Para saber si los datos son correctos necesitamos saber que delimitador tiene el archivo, para asi saber separar valores.

### 2. Función `es_numero`
Verifica si un valor dado es un número. Esto lo logra intentando pasar un número a `float`. Si lo logra, significa que es un número; de lo contrario, es cualquier otro tipo de carácter.
Esta es la parte mas importante ya que con esto sabemos si el valor tiene el formato correcto.

### 3. Función `validar_archivo`
Valida un archivo de datos, verificando:

- Que tenga el encabezado (las primeras dos líneas) y que haya al menos una fila de datos.
- La consistencia en el número de columnas.
- Que los valores en las columnas sean números, excepto al principio, ya que tiene una letra.

Después de leer las primeras 10 líneas, deja de leer para que el código sea más óptimo.

### 4. Función `validar_archivos_en_carpeta`
Lee todos los archivos de la carpeta que son `.dat`. Si no ha pasado alguna de las pruebas de validación, el error sera redirigido a error_log.log indicando el archivo que contiene el error junto a la linea y columna.
