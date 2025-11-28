Biblioteca Personal con KeyDB

Aplicación de línea de comandos para gestionar una biblioteca personal utilizando KeyDB como sistema de almacenamiento en memoria. Cada libro se almacena como un objeto serializado en formato JSON.

Objetivo

Modificar el sistema original para reemplazar el uso de MongoDB por KeyDB, aprovechando operaciones rápidas y eficientes mediante redis-py.

Requisitos

La aplicación permite:

Agregar libros con título, autor, género y estado de lectura

Actualizar información de libros

Eliminar libros del sistema

Ver todos los libros registrados

Buscar libros por título, autor o género

Finalizar la aplicación correctamente

Instalación de KeyDB
Opción 1: Instalar KeyDB en local

Descargar KeyDB desde: https://docs.keydb.dev

Instalar según el sistema operativo

Iniciar el servidor:

keydb-server

Opción 2: Usar contenedor Docker
docker run -p 6379:6379 eqalpha/keydb

Opción 3: Usar Redis como reemplazo temporal

La aplicación también funciona si instalas Redis:

sudo apt install redis
redis-server

Configuración de entorno

Crear un archivo .env en la raíz del proyecto:

KEYDB_HOST=localhost
KEYDB_PORT=6379
KEYDB_PASSWORD=

Instalación de dependencias

Ejecutar:

pip install -r requirements.txt

Ejecutar la aplicación
python main.py

Estructura interna de los datos

Cada libro se almacena como una clave:

libro:<id>


Ejemplo de documento JSON almacenado en KeyDB:

{
  "id": "1",
  "titulo": "El Principito",
  "autor": "Antoine de Saint-Exupéry",
  "genero": "Ficción",
  "estado": "Leído"
}

Operaciones CRUD implementadas
Agregar libro

Crea una clave con un identificador único e inserta el libro serializado.

Actualizar libro

Modifica solamente los campos que el usuario indique.

Eliminar libro

Elimina la clave asociada al libro.

Listar libros

Recupera todas las claves que comienzan con libro:.

Buscar libros

Filtra por título, autor o género recorriendo los documentos almacenados.

Errores manejados

Fallos de conexión

Claves inexistentes

Entrada inválida del usuario

Estructuras JSON mal formadas

Dependencias principales

redis

python-dotenv
