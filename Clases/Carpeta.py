# importa de typing los tipos List y Optional para anotaciones de tipo
from typing import List, Optional
# Importa la clase Mensaje para gestionar los mensajes dentro de las carpetas
from Mensaje import Mensaje

# Clase Carpeta con soporte para subcarpetas (estructura de árbol).
# Cada carpeta puede tener múltiples subcarpetas (hijos) y mensajes.
# La carpeta raíz no tiene padre (padre=None).
# Se implementan métodos para gestión básica y funciones globales para operaciones complejas.
class Carpeta:
    def __init__(self, nombre: str, padre: Optional['Carpeta'] = None):
        self.nombre = nombre
        # Lista de mensajes en la carpeta actual
        self.mensajes: List[Mensaje] = []
        # Lista de subcarpetas como instancias de Carpeta, se inicializa vacía
        self.subcarpetas: List['Carpeta'] = [] 
        self.padre = padre

    # Métodos de Gestión Básica de Carpetas y Mensajes (Operan en el nivel actual)
    
    def crear_subcarpeta(self, nombre_sub: str) -> 'Carpeta':
        # Crea una nueva subcarpeta bajo la carpeta actual. 
        nueva_carpeta = Carpeta(nombre_sub, padre=self)
        self.subcarpetas.append(nueva_carpeta)
        # Retorna la nueva subcarpeta creada
        return nueva_carpeta

    def eliminar_subcarpeta(self, nombre_sub: str) -> bool:
        # Elimina una subcarpeta por nombre si existe, recorriendo la lista de subcarpetas.
        # Retorna True si se eliminó, False si no se encontró.
        for i, sub in enumerate(self.subcarpetas):
            if sub.nombre == nombre_sub:
                del self.subcarpetas[i] 
                return True
        return False
    
    def agregar_mensaje(self, mensaje: Mensaje):
        # Agrega un mensaje con validación de tipo.
        if isinstance(mensaje, Mensaje):
            self.mensajes.append(mensaje)
        else:
            raise TypeError("Solamente se agregan objetos de clase Mensaje") # De no ser un objeto Mensaje, lanza un error.

    def eliminar_mensaje(self, mensaje: Mensaje):
        # Elimina un mensaje si existe en la carpeta actual.
        # Usa un bloque try-except para manejar el caso donde el mensaje no se encuentra.
        try:
            self.mensajes.remove(mensaje)
        except ValueError:
            print(f"Error: Mensaje no encontrado en la carpeta '{self.nombre}'") # Mensaje no encontrado.

    def listar_mensajes(self) -> List[Mensaje]:
        # Devuelve la lista de mensajes de la carpeta actual.
        return self.mensajes
    
    def __repr__(self):
        return f"Carpeta('{self.nombre}', Subcarpetas: {len(self.subcarpetas)}, Mensajes: {len(self.mensajes)})"