import json
import redis
from dotenv import load_dotenv
import os

# Biblioteca Personal con KeyDB (Redis compatible) + redis-py

load_dotenv()

# Conexión con KeyDB

def conectar_keydb():
    try:
        host = os.getenv("KEYDB_HOST", "localhost")
        port = int(os.getenv("KEYDB_PORT", 6379))
        password = os.getenv("KEYDB_PASSWORD", None)

        cliente = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )

        cliente.ping()  # Verificar conexión
        return cliente
    except redis.exceptions.ConnectionError:
        print("Error: No se pudo conectar a KeyDB. Verifique el servidor o la configuración.")
        exit()
    except Exception as e:
        print(f"Falla inesperada al conectar: {e}")
        exit()

# Generador de IDs

def generar_id(cliente):
    return cliente.incr("libros:id")  # Auto-incremento


# CRUD

def agregar_libro(cliente):
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()
    estado = input("Estado (Leído / No leído): ").strip()

    if estado not in ["Leído", "No leído"]:
        print("Estado inválido.\n")
        return

    libro_id = generar_id(cliente)
    clave = f"libro:{libro_id}"

    libro = {
        "id": libro_id,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    try:
        cliente.set(clave, json.dumps(libro))
        print("Libro agregado correctamente.\n")
    except Exception as e:
        print("Error al agregar libro:", e)


def actualizar_libro(cliente):
    ver_libros(cliente)

    id_buscar = input("Ingrese el ID del libro a actualizar: ").strip()
    clave = f"libro:{id_buscar}"

    if not cliente.exists(clave):
        print("No existe un libro con ese ID.\n")
        return

    libro = json.loads(cliente.get(clave))

    libro["titulo"] = input("Nuevo título: ").strip()
    libro["autor"] = input("Nuevo autor: ").strip()
    libro["genero"] = input("Nuevo género: ").strip()
    libro["estado"] = input("Nuevo estado (Leído / No leído): ").strip()

    if libro["estado"] not in ["Leído", "No leído"]:
        print("Estado inválido.\n")
        return

    try:
        cliente.set(clave, json.dumps(libro))
        print("Libro actualizado exitosamente.\n")
    except Exception as e:
        print("Error al actualizar libro:", e)


def eliminar_libro(cliente):
    ver_libros(cliente)

    id_buscar = input("Ingrese el ID del libro a eliminar: ").strip()
    clave = f"libro:{id_buscar}"

    if cliente.delete(clave):
        print("Libro eliminado.\n")
    else:
        print("No se encontró un libro con ese ID.\n")


def ver_libros(cliente):
    claves = cliente.scan_iter("libro:*")
    vacio = True

    print("\nLISTADO DE LIBROS")
    print("-" * 60)

    for clave in claves:
        vacio = False
        libro = json.loads(cliente.get(clave))
        print(f"ID: {libro['id']} | Título: {libro['titulo']} | "
              f"Autor: {libro['autor']} | Género: {libro['genero']} | Estado: {libro['estado']}")

    print("-" * 60 + "\n")

    if vacio:
        print("No hay libros registrados.\n")


def buscar_libros(cliente):
    campo = input("Buscar por (titulo/autor/genero): ").lower().strip()
    termino = input("Ingrese el término: ").strip()

    if campo not in ["titulo", "autor", "genero"]:
        print("Campo no válido.\n")
        return

    claves = cliente.scan_iter("libro:*")
    resultados = []

    for clave in claves:
        libro = json.loads(cliente.get(clave))
        if termino.lower() in libro[campo].lower():
            resultados.append(libro)

    if resultados:
        print("\nRESULTADOS DE BÚSQUEDA")
        print("-" * 60)
        for libro in resultados:
            print(f"ID: {libro['id']} | Título: {libro['titulo']} | "
                  f"Autor: {libro['autor']} | Género: {libro['genero']} | Estado: {libro['estado']}")
        print("-" * 60 + "\n")
    else:
        print("No se encontraron coincidencias.\n")

# Menú

def menu():
    cliente = conectar_keydb()

    while True:
        print("========= MENÚ BIBLIOTECA PERSONAL =========")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        print("=============================================")

        opcion = input("Seleccione una opción (1-6): ").strip()
        print()

        if opcion == "1":
            agregar_libro(cliente)
        elif opcion == "2":
            actualizar_libro(cliente)
        elif opcion == "3":
            eliminar_libro(cliente)
        elif opcion == "4":
            ver_libros(cliente)
        elif opcion == "5":
            buscar_libros(cliente)
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.\n")

# Ejecución principal

if __name__ == "__main__":
    menu()
