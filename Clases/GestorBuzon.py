from Carpeta import Carpeta
from Mensaje import Mensaje
from typing import Optional, List, Dict

# Clase estática que agrupa las operaciones recursivas sobre el árbol de carpetas del buzón.    
class GestorBuzon:
    @staticmethod
    def buscar_carpeta_por_nombre(carpeta_actual: 'Carpeta', nombre_buscado: str) -> Optional['Carpeta']:
        # Busca recursivamente una carpeta por nombre, retornando la instancia o None.
        if carpeta_actual is None: return None
        if carpeta_actual.nombre == nombre_buscado: return carpeta_actual
        for subcarpeta in carpeta_actual.subcarpetas:
            resultado = GestorBuzon.buscar_carpeta_por_nombre(subcarpeta, nombre_buscado)
            if resultado: return resultado
        return None

    @staticmethod
    def busqueda_recursiva_mensajes(carpeta_actual: 'Carpeta', termino: str, campo: str) -> List[tuple['Mensaje', str]]:
        # Realiza una búsqueda recursiva por 'asunto' o 'remitente'.
        resultados = []
        for mensaje in carpeta_actual.mensajes:
            valor = getattr(mensaje, campo, None)
            if valor and termino.lower() in str(valor).lower():
                resultados.append((mensaje, carpeta_actual.nombre))

        for subcarpeta in carpeta_actual.subcarpetas:
            resultados.extend(GestorBuzon.busqueda_recursiva_mensajes(subcarpeta, termino, campo))
        return resultados

    @staticmethod
    def _buscar_y_eliminar_origen_recursivo(c: 'Carpeta', mensaje: 'Mensaje') -> bool:
        # Helper privado que retorna True si el mensaje fue encontrado y eliminado.
        if c is None: return False
        if mensaje in c.mensajes:
            c.eliminar_mensaje(mensaje)
            return True
            
        for sub in c.subcarpetas:
            if GestorBuzon._buscar_y_eliminar_origen_recursivo(sub, mensaje):
                return True
        return False

    @staticmethod
    def mover_mensaje(raiz: 'Carpeta', mensaje: 'Mensaje', nombre_destino: str) -> bool:
        # Mueve un mensaje (objeto) de su carpeta actual a la carpeta destino.
        carpeta_destino = GestorBuzon.buscar_carpeta_por_nombre(raiz, nombre_destino)
        if not carpeta_destino:
            print(f"Error: Carpeta destino '{nombre_destino}' no encontrada.")
            return False
        # 1. Eliminar el mensaje de su origen (recursivamente)
        origen_encontrado = GestorBuzon._buscar_y_eliminar_origen_recursivo(raiz, mensaje)
        if not origen_encontrado:
            print("Error: Mensaje no encontrado en ninguna carpeta para mover.")
            return False
        # 2. Agregar mensaje a la carpeta destino
        carpeta_destino.agregar_mensaje(mensaje)
        return True
