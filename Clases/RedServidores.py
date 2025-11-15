from collections import deque
# importa de typing los tipos Dict, List y Optional para anotaciones de tipo
from typing import Dict, List, Optional

# Clase RedServidores (Gestiona la topología y búsqueda de rutas, mediante un grafo)
class RedServidores:
    def __init__(self, topologia: Dict[str, List[str]]):
        self.grafo = topologia
    
    def buscar_ruta_envio(self, origen: str, destino: str) -> Optional[List[str]]:
        if origen not in self.grafo or destino not in self.grafo: return None
        if origen == destino: return [origen]
        cola = deque([origen])
        padres: Dict[str, Optional[str]] = {origen: None}
        while cola:
            servidor_actual = cola.popleft()
            for vecino in self.grafo.get(servidor_actual, []):
                if vecino not in padres:
                    padres[vecino] = servidor_actual
                    if vecino == destino:
                        ruta = []
                        nodo = destino
                        while nodo is not None:
                            ruta.append(nodo)
                            nodo = padres.get(nodo)
                        return ruta[::-1]
                    cola.append(vecino)
        return None
