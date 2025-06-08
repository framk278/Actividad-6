from collections import defaultdict
import json
import os

class GrafoBiblioteca:
    def __init__(self):
        # Usamos defaultdict para manejar automáticamente nodos no existentes
        self.grafo = defaultdict(dict)
        self.usuarios = set()
        self.libros = set()
        
    def agregar_nodo(self, id_nodo, tipo):
        """Agrega un nodo al grafo (usuario o libro)"""
        if tipo == 'usuario':
            self.usuarios.add(id_nodo)
        elif tipo == 'libro':
            self.libros.add(id_nodo)
            
    def agregar_arista(self, id_usuario, id_libro, peso=1):
        """Agrega una arista dirigida de usuario a libro con un peso"""
        self.agregar_nodo(id_usuario, 'usuario')
        self.agregar_nodo(id_libro, 'libro')
        self.grafo[id_usuario][id_libro] = peso
        
    def obtener_libros_populares(self, n=5):
        """Retorna los n libros más populares basado en el número de préstamos"""
        contador_libros = defaultdict(int)
        for usuario in self.grafo:
            for libro, peso in self.grafo[usuario].items():
                contador_libros[libro] += peso
                
        return sorted(contador_libros.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def obtener_recomendaciones_usuario(self, id_usuario, n=3):
        """Retorna recomendaciones de libros basadas en el historial del usuario"""
        if id_usuario not in self.grafo:
            return []
            
        # Obtener libros que el usuario ya ha leído
        libros_leidos = set(self.grafo[id_usuario].keys())
        
        # Contar cuántas veces otros usuarios han leído los mismos libros
        usuarios_similares = defaultdict(int)
        for libro in libros_leidos:
            for otro_usuario in self.grafo:
                if otro_usuario != id_usuario and libro in self.grafo[otro_usuario]:
                    usuarios_similares[otro_usuario] += 1
        
        # Obtener libros leídos por usuarios similares
        recomendaciones = defaultdict(int)
        for usuario_similar, peso in usuarios_similares.items():
            for libro in self.grafo[usuario_similar]:
                if libro not in libros_leidos:
                    recomendaciones[libro] += peso
        
        return sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def guardar_grafo(self, archivo='grafo_biblioteca.json'):
        """Guarda el grafo en un archivo JSON"""
        datos = {
            'grafo': dict(self.grafo),
            'usuarios': list(self.usuarios),
            'libros': list(self.libros)
        }
        with open(archivo, 'w') as f:
            json.dump(datos, f)
            
    def cargar_grafo(self, archivo='grafo_biblioteca.json'):
        """Carga el grafo desde un archivo JSON"""
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                datos = json.load(f)
                self.grafo = defaultdict(dict, datos['grafo'])
                self.usuarios = set(datos['usuarios'])
                self.libros = set(datos['libros'])
                
    def mostrar_estadisticas(self):
        """Muestra estadísticas básicas del grafo"""
        print("\n📊 ESTADÍSTICAS DEL GRAFO:")
        print(f"Total de usuarios: {len(self.usuarios)}")
        print(f"Total de libros: {len(self.libros)}")
        
        total_interacciones = sum(len(aristas) for aristas in self.grafo.values())
        print(f"Total de interacciones: {total_interacciones}")
        
        print("\n📚 Libros más populares:")
        for libro_id, peso in self.obtener_libros_populares():
            print(f"Libro ID {libro_id}: {peso} préstamos") 