# importa de typing los tipos List y Optional para anotaciones de tipo
from typing import List, Optional
# Importa la clase Usuario para gestionar los usuarios del servidor
#from Usuario import Usuario
# Importa la clase Mensaje para manejar los mensajes que se envían y reciben
from Mensaje import Mensaje
# Importa la clase RedServidores para realizar el enrutamiento
from RedServidores import RedServidores

class ServidorCorreo:
    def __init__(self, red_servidores: RedServidores):
        self.usuarios: List['Usuario'] = []
        self.red_servidores = red_servidores
    
    def enrutar_red(self, mensaje: Mensaje, servidor_origen: str, servidor_destino: str) -> bool:
        ruta = self.red_servidores.buscar_ruta_envio(servidor_origen, servidor_destino)
        if not ruta:
            print(f"[Red] Error: No se pudo encontrar ruta de {servidor_origen} a {servidor_destino}.")
            return False
        print(f"[Red] Ruta de envío: {' -> '.join(ruta)}")
        destino_usuario = self.buscar_usuario(mensaje.destinatario)
        if destino_usuario:
            # Llama al método de recepción del usuario destino
            destino_usuario._recibir_mensaje(
                mensaje.remitente, mensaje.asunto, mensaje.contenido,
                mensaje.fecha_envio, mensaje.estado_leido, mensaje.adjuntos
            )
            return True
        else:
            print(f"Error de entrega: Usuario destino '{mensaje.destinatario}' no encontrado.")
            return False

    def registrar_usuario(self, nombre_usuario: str, contrasena: str):
        from Usuario import Usuario  # Importación local para evitar dependencias circulares
        nuevo_usuario = Usuario(nombre_usuario, contrasena, servidor=self) 
        if self.buscar_usuario(nombre_usuario) is None:
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
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                return usuario
        return None

    def cambiar_contrasena_usuario(self, nombre_usuario: str, nueva_contrasena: str) -> bool:
        # Busca al usuario por nombre y actualiza su contraseña.

        # Validación de Longitud (simulación de seguridad)
        if not nueva_contrasena or len(nueva_contrasena) < 4:
            raise ValueError("La nueva contraseña debe tener al menos 4 caracteres.")
        # Búsqueda del Usuario
        usuario = self.buscar_usuario(nombre_usuario)
        if usuario:
            # Actualización de la Credencial
            usuario.contrasena = nueva_contrasena
            return True
        else:
            # Caso límite: Usuario no encontrado
            return False

    def enrutar_mensaje(self, mensaje: Mensaje) -> bool:
        # Simplificación: Usar servidores ficticios del grafo para la simulación
        servidor_origen_fijo = 'S_MADRID' 
        servidor_destino_fijo = 'S_NY' 
        return self.enrutar_red(mensaje, servidor_origen_fijo, servidor_destino_fijo)