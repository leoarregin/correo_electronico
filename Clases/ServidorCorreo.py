# importa de typing los tipos List y Optional para anotaciones de tipo
from typing import List, Optional
# Importa la clase Usuario para gestionar los usuarios del servidor
from Usuario import Usuario
# Importa la clase Mensaje para manejar los mensajes que se envían y reciben
from Mensaje import Mensaje

# Clase ServidorCorreo (Gestiona usuarios y maneja el enrutamiento de mensajes)
class ServidorCorreo():
    def __init__(self):
        self.usuarios: List['Usuario'] = [] # Almacena todas las instancias de Usuario

    def registrar_usuario(self, nombre_usuario: str, contrasena: str):
        # Asegura que el usuario se inicialice con una referencia al servidor
        nuevo_usuario = Usuario(nombre_usuario, contrasena, servidor=self) 
        if nuevo_usuario not in self.usuarios:
            self.usuarios.append(nuevo_usuario)
            return True
        else:
            raise ValueError ("El nombre de usuario está en uso.")

    def autenticar_usuario(self, nombre_usuario: str, contrasena: str) -> 'Usuario':
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena:
                return usuario
        raise ValueError("Nombre de usuario o contraseña incorrectos.")
    
    def buscar_usuario(self, nombre_usuario: str) -> Optional['Usuario']:
        # Busca y retorna un usuario por su nombre.
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                return usuario
        return None

    def enrutar_mensaje(self, mensaje: Mensaje) -> bool:
        # Simula la entrega del mensaje al buzón del destinatario.
        destino_usuario = self.buscar_usuario(mensaje.destinatario)
        
        if destino_usuario:
            # Llama al método de recepción del usuario destino
            destino_usuario._recibir_mensaje(
                mensaje.remitente,
                mensaje.asunto,
                mensaje.contenido,
                mensaje.fecha_envio,
                mensaje.estado_leido,
                mensaje.adjuntos
            )
            return True
        else:
            print(f"Error de enrutamiento: Usuario destino '{mensaje.destinatario}' no encontrado.")
            return False
