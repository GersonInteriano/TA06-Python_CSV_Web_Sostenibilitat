# Script de Validación de Datos
	
Este script valida archivos de datos con extensión `.dat` para asegurar que cumplen con el formato esperado.

## Pas 1

### 1. Configuración de Logging
Se configura un registro de errores que guarda los mensajes en el archivo `error_log.log`.

### 2. Función `revisar_format`
Creamos una funcion que verifica si el archivo tiene la extensión `.dat`.

### 3. Función `llegir_fitxer`
Lee el contenido inicial del archivo para identificar el delimitador usado.

### 4. Función `hi_ha_comentaris`
Comprueba si el archivo contiene comentarios que empiezan con `#`.

### 5. Función `revisar_capcaleres`
Valida que la primera fila de encabezado sea idéntica en todos los archivos y que la segunda fila tenga el formato correcto.

### 6. Función `processar_fitxers`
Procesa todos los archivos `.dat` en el directorio especificado:
- Verifica la extensión del archivo.
- Detecta el delimitador (coma, tabulación o espacio).
- Revisa si hay comentarios.
- Comprueba que los encabezados sean consistentes.

### 7. Función `main`
Define el directorio a procesar y ejecuta la validación de los archivos.


## Pas2

### 1. Función `detectar_delimitador`

En esta función he puesto los delimitadores que se usan en los archivos. Si estos no los tienen o tienen demasiados, estará mal:

- **Tabulaciones** (`\t`)
- **Espacios** (` `)

### 2. Función `es_numero`

Verifica si un valor dado es un número. Esto lo logra intentando pasar un número a `float`. Si lo logra, significa que es un número; de lo contrario, es cualquier otro tipo de carácter.

### 3. Función `validar_archivo`

Valida un archivo de datos, verificando:

- Que tenga el encabezado (las primeras dos líneas) y que haya al menos una fila de datos.
- La consistencia en el número de columnas.
- Que los valores en las columnas sean números, excepto al principio, ya que tiene una letra.

Después de leer las primeras 10 líneas, deja de leer para que el código sea más óptimo.

### 4. Función `validar_archivos_en_carpeta`

Lee todos los archivos de la carpeta que son `.dat`. Si no ha pasado alguna de las pruebas de validación, saldrá por pantalla que ese archivo no tiene el formato correcto. En caso de que pase todas las pruebas, saldrá que es válido.
