import json
import os
import random  # Nueva importación
from grafo_biblioteca import GrafoBiblioteca  # Nueva importación

# -----------------------------------
# ESTRUCTURAS DE DATOS PRINCIPALES
# -----------------------------------
class NodoLibro:
    def __init__(self, libro):
        self.libro = libro
        self.izquierda = None
        self.derecha = None

class ArbolLibros:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro):
        if not self.raiz:
            self.raiz = NodoLibro(libro)
        else:
            self._insertar_recursivo(self.raiz, libro)

    def _insertar_recursivo(self, nodo, libro):
        if libro['id'] < nodo.libro['id']:
            if nodo.izquierda:
                self._insertar_recursivo(nodo.izquierda, libro)
            else:
                nodo.izquierda = NodoLibro(libro)
        else:
            if nodo.derecha:
                self._insertar_recursivo(nodo.derecha, libro)
            else:
                nodo.derecha = NodoLibro(libro)

    def buscar(self, id_libro):
        return self._buscar_recursivo(self.raiz, id_libro)

    def _buscar_recursivo(self, nodo, id_libro):
        if nodo is None:
            return None
        if id_libro == nodo.libro['id']:
            return nodo.libro
        elif id_libro < nodo.libro['id']:
            return self._buscar_recursivo(nodo.izquierda, id_libro)
        else:
            return self._buscar_recursivo(nodo.derecha, id_libro)

    def buscar_por_titulo(self, titulo):
        return self._buscar_por_titulo_recursivo(self.raiz, titulo)

    def _buscar_por_titulo_recursivo(self, nodo, titulo):
        if nodo is None:
            return None
        if nodo.libro['titulo'].lower() == titulo.lower():
            return nodo.libro
        izquierda = self._buscar_por_titulo_recursivo(nodo.izquierda, titulo)
        if izquierda:
            return izquierda
        return self._buscar_por_titulo_recursivo(nodo.derecha, titulo)

    def inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierda, resultado)
            resultado.append(nodo.libro)
            self._inorden_recursivo(nodo.derecha, resultado)

# Instancias de estructuras
arbol_libros = ArbolLibros()
usuarios = []
cola_prestamos = []
pila_devoluciones = []
grafo_biblioteca = GrafoBiblioteca()  # Nueva instancia del grafo

# Listas para generación aleatoria de libros
titulos_genericos = ["El Viaje", "Misterio en la Niebla", "Horizontes Perdidos", "La Última Aventura", "Crónicas del Tiempo"]
autores_genericos = ["J. Doe", "A. Pérez", "L. Martínez", "M. Gómez", "C. Ramírez"]

# -----------------------------------
# FUNCIONES DE ARCHIVOS (PERSISTENCIA)
# -----------------------------------
def guardar_datos():
    with open('libros.json', 'w') as f:
        json.dump(arbol_libros.inorden(), f)
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f)
    with open('cola_prestamos.json', 'w') as f:
        json.dump(cola_prestamos, f)
    with open('pila_devoluciones.json', 'w') as f:
        json.dump(pila_devoluciones, f)
    grafo_biblioteca.guardar_grafo()  # Guardar el grafo

def cargar_datos():
    global usuarios, cola_prestamos, pila_devoluciones
    if os.path.exists('libros.json'):
        with open('libros.json', 'r') as f:
            libros = json.load(f)
            for libro in libros:
                arbol_libros.insertar(libro)
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            usuarios = json.load(f)
    if os.path.exists('cola_prestamos.json'):
        with open('cola_prestamos.json', 'r') as f:
            cola_prestamos = json.load(f)
    if os.path.exists('pila_devoluciones.json'):
        with open('pila_devoluciones.json', 'r') as f:
            pila_devoluciones = json.load(f)
    grafo_biblioteca.cargar_grafo()  # Cargar el grafo

# -----------------------------------
# NUEVA FUNCIÓN: Generar libros aleatorios
# -----------------------------------
def generar_libros_aleatorios(cantidad):
    libros_actuales = arbol_libros.inorden()
    id_actual = len(libros_actuales) + 1

    for _ in range(cantidad):
        titulo = random.choice(titulos_genericos) + " " + str(random.randint(1, 100))
        autor = random.choice(autores_genericos)
        libro = {'id': id_actual, 'titulo': titulo, 'autor': autor, 'disponible': True}
        arbol_libros.insertar(libro)
        id_actual += 1
    
    guardar_datos()
    print(f"✅ {cantidad} libros generados aleatoriamente y agregados al catálogo.")

# -----------------------------------
# FUNCIONES PRINCIPALES
# -----------------------------------
def agregar_libro(titulo, autor):
    nuevo_id = len(arbol_libros.inorden()) + 1
    libro = {'id': nuevo_id, 'titulo': titulo, 'autor': autor, 'disponible': True}
    arbol_libros.insertar(libro)
    guardar_datos()
    print(f"✅ Libro agregado: {titulo} (ID: {nuevo_id})")

def buscar_libro_por_titulo(titulo):
    libro = arbol_libros.buscar_por_titulo(titulo)
    if libro:
        estado = "Disponible" if libro['disponible'] else "Prestado"
        print(f"Libro encontrado: ID: {libro['id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Estado: {estado}")
    else:
        print("❌ Libro no encontrado.")

def registrar_usuario(nombre):
    id_usuario = len(usuarios) + 1001
    usuarios.append({'id': id_usuario, 'nombre': nombre, 'libros_prestados': []})
    guardar_datos()
    print(f"✅ Usuario registrado: {nombre} (ID: {id_usuario})")

def solicitar_prestamo(id_usuario, id_libro):
    cola_prestamos.append((id_usuario, id_libro))
    guardar_datos()
    print("📥 Solicitud de préstamo registrada.")

def procesar_prestamo():
    if cola_prestamos:
        id_usuario, id_libro = cola_prestamos.pop(0)
        libro = arbol_libros.buscar(id_libro)
        if libro and libro['disponible']:
            libro['disponible'] = False
            for usuario in usuarios:
                if usuario['id'] == id_usuario:
                    usuario['libros_prestados'].append(libro['titulo'])
                    # Actualizar el grafo
                    grafo_biblioteca.agregar_arista(id_usuario, id_libro)
                    guardar_datos()
                    print(f"📚 Préstamo exitoso: {libro['titulo']} a {usuario['nombre']}")
                    return
        print("❌ Libro no disponible o no encontrado.")
    else:
        print("ℹ️ No hay solicitudes de préstamo.")
    guardar_datos()

def devolver_libro(id_usuario, titulo_libro):
    for usuario in usuarios:
        if usuario['id'] == id_usuario:
            if titulo_libro in usuario['libros_prestados']:
                usuario['libros_prestados'].remove(titulo_libro)
                libros = arbol_libros.inorden()
                for libro in libros:
                    if libro['titulo'] == titulo_libro:
                        libro['disponible'] = True
                        pila_devoluciones.append(titulo_libro)
                        guardar_datos()
                        print(f"✅ Libro devuelto: {titulo_libro}")
                        return
            print("❌ El usuario no tiene ese libro.")
            return
    print("❌ Usuario no encontrado.")

def mostrar_historial_devoluciones():
    print("📤 Historial de devoluciones:")
    if not pila_devoluciones:
        print("No hay devoluciones registradas.")
    else:
        for libro in reversed(pila_devoluciones):
            print(f"- {libro}")

def mostrar_libros():
    print("\n📚 LIBROS EN LA BIBLIOTECA:")
    libros = arbol_libros.inorden()
    if not libros:
        print("No hay libros registrados.")
    else:
        for libro in libros:
            estado = "Disponible" if libro['disponible'] else "Prestado"
            print(f"ID: {libro['id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Estado: {estado}")

def mostrar_recomendaciones(id_usuario):
    """Muestra recomendaciones de libros para un usuario"""
    recomendaciones = grafo_biblioteca.obtener_recomendaciones_usuario(id_usuario)
    if recomendaciones:
        print(f"\n📚 RECOMENDACIONES PARA USUARIO {id_usuario}:")
        for libro_id, peso in recomendaciones:
            libro = arbol_libros.buscar(libro_id)
            if libro:
                print(f"- {libro['titulo']} (Autor: {libro['autor']})")
    else:
        print("No hay recomendaciones disponibles para este usuario.")

def mostrar_estadisticas_grafo():
    """Muestra estadísticas del grafo de interacciones"""
    grafo_biblioteca.mostrar_estadisticas()

# -----------------------------------
# MENÚ INTERACTIVO
# -----------------------------------
def menu():
    while True:
        print("\n--- MENÚ BIBLIOTECA ---")
        print("1. Agregar libro")
        print("2. Generar libros aleatorios")
        print("3. Registrar usuario")
        print("4. Solicitar préstamo")
        print("5. Procesar préstamo")
        print("6. Devolver libro")
        print("7. Ver libros registrados")
        print("8. Buscar libro por título")
        print("9. Ver historial de devoluciones")
        print("10. Ver recomendaciones de libros")
        print("11. Ver estadísticas del grafo")
        print("12. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            titulo = input("Título del libro: ")
            autor = input("Autor del libro: ")
            agregar_libro(titulo, autor)
        elif opcion == '2':
            cantidad = int(input("¿Cuántos libros aleatorios deseas generar?: "))
            generar_libros_aleatorios(cantidad)
        elif opcion == '3':
            nombre = input("Nombre del usuario: ")
            registrar_usuario(nombre)
        elif opcion == '4':
            id_usuario = int(input("ID del usuario: "))
            id_libro = int(input("ID del libro: "))
            solicitar_prestamo(id_usuario, id_libro)
        elif opcion == '5':
            procesar_prestamo()
        elif opcion == '6':
            id_usuario = int(input("ID del usuario: "))
            titulo_libro = input("Título del libro a devolver: ")
            devolver_libro(id_usuario, titulo_libro)
        elif opcion == '7':
            mostrar_libros()
        elif opcion == '8':
            titulo = input("Título del libro a buscar: ")
            buscar_libro_por_titulo(titulo)
        elif opcion == '9':
            mostrar_historial_devoluciones()
        elif opcion == '10':
            id_usuario = int(input("ID del usuario: "))
            mostrar_recomendaciones(id_usuario)
        elif opcion == '11':
            mostrar_estadisticas_grafo()
        elif opcion == '12':
            print("¡Hasta pronto!")
            break
        else:
            print("❌ Opción no válida")

# -----------------------------------
# INICIO DEL PROGRAMA
# -----------------------------------
cargar_datos()
menu()
