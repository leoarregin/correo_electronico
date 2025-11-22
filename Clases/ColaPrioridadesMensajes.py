from typing import Optional

# Nodo para la Lista Enlazada de Mensajes
class NodoMensaje:
    # Nodo para la Lista Enlazada, contiene un Mensaje y una referencia al siguiente.
    def __init__(self, mensaje: 'Mensaje'):
        self.mensaje = mensaje
        self.siguiente: Optional['NodoMensaje'] = None


# Implementa una cola de prioridades para los mensajes
class ColaPrioridadesMensajes:
    # Gestiona mensajes usando una Lista Enlazada con prioridad: Urgente (FIFO) > Normal (FIFO). Operaciones O(1).
    def __init__(self):
        self.cabeza: Optional[NodoMensaje] = None
        self.cola: Optional[NodoMensaje] = None
        self.fin_urgentes: Optional[NodoMensaje] = None # Puntero al último mensaje urgente

    def esta_vacia(self) -> bool:
        # Verifica si la cola no contiene elementos.
        return self.cabeza is None

    def encolar(self, mensaje: 'Mensaje'):
        # Agrega un mensaje a la cola según su prioridad.
        nuevo_nodo = NodoMensaje(mensaje)
        if self.esta_vacia():
            # Primer elemento de la cola
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
            if mensaje.es_urgente:
                self.fin_urgentes = nuevo_nodo
            return
        if mensaje.es_urgente:
            # --- Inserción de Mensaje Urgente (O(1)) ---
            if self.fin_urgentes:
                # Caso 1: Hay otros mensajes urgentes. Inserta DESPUÉS del último urgente.
                nuevo_nodo.siguiente = self.fin_urgentes.siguiente
                self.fin_urgentes.siguiente = nuevo_nodo
            else:
                # Caso 2: Es el primer urgente (se inserta al principio, antes del primer normal o como cabeza).
                nuevo_nodo.siguiente = self.cabeza
                self.cabeza = nuevo_nodo
            
            # El nuevo nodo es ahora el último urgente
            self.fin_urgentes = nuevo_nodo

        else:
            # --- Inserción de Mensaje Normal (O(1)) ---
            
            # Se inserta al final de la cola (después del último mensaje normal)
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def desencolar(self) -> Optional['Mensaje']:
        # Extrae y retorna el mensaje con la máxima prioridad (la Cabeza).
        if self.esta_vacia():
            return None
        mensaje_extraido = self.cabeza.mensaje
        # Si el nodo extraído era el último urgente, resetear el puntero fin_urgentes
        if self.cabeza == self.fin_urgentes:
            self.fin_urgentes = None
        # Mueve la cabeza al siguiente nodo
        self.cabeza = self.cabeza.siguiente
        # Si la lista queda vacía, resetear también la cola
        if self.cabeza is None:
            self.cola = None
            self.fin_urgentes = None # (redundante, pero asegura estado)
        return mensaje_extraido
