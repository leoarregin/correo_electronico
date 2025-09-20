class Usuario(InterfazMensajeria):
    def __init__(self, nombre_usuario: str, contrasena: str):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.recibidos: List[Mensaje] = []
        self.enviados: List[Mensaje] = []
        self.borradores: List[Mensaje] = []
        self.papelera: List[Mensaje] = []

    def _enviar_mensaje(self, destinatario, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = []):
        mensaje = Mensaje(self.nombre_usuario, destinatario, asunto, contenido,fecha_envio, leido, adjuntos)
        self.enviados.append(mensaje)
        print(f"Mensaje enviado a {destinatario}")

    def _recibir_mensaje(self, remitente, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = []):
        mensaje = Mensaje(remitente, self.nombre_usuario, asunto, contenido, fecha_envio, leido, adjuntos)
        self.recibidos.append(mensaje)
        print(f"Nuevo mensaje de {remitente}")

    def _listar_mensaje(self, carpeta: str) -> List["Mensaje"]:
        if carpeta == "recibidos":
            return self.recibidos
        elif carpeta == "enviados":
            return self.enviados
        elif carpeta == "borradores":
            return self.borradores
        elif carpeta == "papelera":
            return self.papelera
        else:
            raise ValueError("Carpeta no reconocida")
