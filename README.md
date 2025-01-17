# Script de Validación de Datos
	
Script para validar archivos de datos y asegurarse que cumplen con el formato esperado y si los datos son correctos y no provocan ningun tpo de error.

## Pas 1

### 1. Configuración de Logging
Configurar un registro de errores que guarda los mensajes de error en el archivo `error_log.log`.

### 2. Función `revisar_format`
Creamos una funcion que verifica si el archivo tiene la extensión `.dat`, para eso utilizamos el *endswith*.

### 3. Función `llegir_fitxer`
Lee el contenido inicial del archivo para identificar el delimitador usado, abriendo los archivos en modo lectura y guardando el delimitador.

### 4. Función `hi_ha_comentaris`
Comprueba si el archivo contiene comentarios que empiezan con `#`, para eso utilizamos el *startswith*.

### 5. Función `revisar_capcaleres`
Valida que la primera fila de encabezado sea idéntica en todos los archivos y que la segunda fila tenga el formato correcto.
- Primero hacemos que valide que tenga dos filas de encabezo
- Pasamos a que valide a primera fila, hacemos que las vaya comparando en todos los archivos a ver si son igual. 
- Seguimos con la segunda fila, hacemos que mire y compare el formato de los valores para detectar si hay alguno diferente.
  
### 6. Función `processar_fitxers`
Procesa todos los archivos `.dat` en el directorio especificado:
- Verifica la extensión del archivo.
- Detecta el delimitador (coma, tabulación o espacio).
- Revisa si hay comentarios.
- Comprueba que los encabezados sean consistentes.

### 7. Función `main`
Define el directorio a procesar y ejecuta la validación de los archivos.
 

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
