# importa de typing los tipos List y Optional para anotaciones de tipo
from typing import List, Optional
# Importa la clase Carpeta para gestionar el buzón del usuario
from Carpeta import Carpeta
# Importa la clase Mensaje para crear y manejar mensajes
from Mensaje import Mensaje
# Importa la interfaz de mensajería para asegurar que Usuario implemente los métodos necesarios
from InterfazMensajeria import InterfazMensajeria
# Importa la clase ServidorCorreo para enrutar mensajes a otros usuarios
from ServidorCorreo import ServidorCorreo

# Clase Usuario (Interactúa con el Servidor para enviar mensajes)
class Usuario(InterfazMensajeria):
    # Se añade 'servidor' como argumento para que el usuario sepa dónde enrutar sus mensajes
    def __init__(self, nombre_usuario: str, contrasena: str, servidor: ServidorCorreo): 
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.servidor = servidor # Referencia al Servidor para la funcionalidad de envío
        
        # La raíz del árbol de carpetas es un objeto Carpeta.
        self.buzon_raiz = Carpeta("Bandeja Principal")
        
        # Referencias a carpetas clave creadas en el árbol
        self.enviados = self.buzon_raiz.crear_subcarpeta("Enviados")
        self.recibidos = self.buzon_raiz.crear_subcarpeta("Recibidos")
        self.papelera = self.buzon_raiz.crear_subcarpeta("Papelera")
        
    def _enviar_mensaje(self, destinatario, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = []):
        mensaje = Mensaje(self.nombre_usuario, destinatario, asunto, contenido, fecha_envio, leido, adjuntos)
        
        # Intenta enrutar el mensaje a través del Servidor
        if self.servidor.enrutar_mensaje(mensaje):
            print(f"Mensaje enrutado a {destinatario}.")
            # Guarda una copia en la carpeta 'Enviados'
            self.enviados.agregar_mensaje(mensaje)
            print(f"Copia guardada en 'Enviados'.")
            return mensaje
        else:
            print(f"Fallo al enviar el mensaje a {destinatario}.")
            return None # Retorna None si el envío falla

    def _recibir_mensaje(self, remitente, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = []):
        # NOTA: Este método es llamado por el Servidor
        mensaje = Mensaje(remitente, self.nombre_usuario, asunto, contenido, fecha_envio, leido, adjuntos)
        # Se guarda en la subcarpeta 'Recibidos'
        self.recibidos.agregar_mensaje(mensaje)
        print(f"[BUZÓN {self.nombre_usuario}] Nuevo mensaje de {remitente} recibido.")
        return mensaje

    def _listar_mensaje(self, nombre_carpeta: str) -> List[Mensaje]:
        # Busca la carpeta por nombre en todo el árbol y lista sus mensajes.
        # Usa la función global para buscar la carpeta en el árbol (O(N))
        carpeta_buscada = buscar_carpeta_por_nombre(self.buzon_raiz, nombre_carpeta)
        
        if carpeta_buscada:
            # Retorna la lista de mensajes de la Carpeta encontrada
            return carpeta_buscada.listar_mensajes()
        else:
            # Si no se encuentra la carpeta en el árbol, lanza la excepción
            raise ValueError(f"Error: Carpeta '{nombre_carpeta}' no reconocida o no existe en el buzón.")
