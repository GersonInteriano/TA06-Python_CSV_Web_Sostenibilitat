# Script de Validación de Datos

El segundo script que hay que hacer es uno que se asegure de que los datos introducidos son correctos. Para ello, haremos un script de validación de datos.

## Estructura del Script

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
