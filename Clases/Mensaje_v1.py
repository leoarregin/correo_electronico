class Mensaje():
    def __init__(self, remitente, destinatario, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = []):
        self.remitente = remitente
        self.destinatario = destinatario
        self.asunto = asunto
        self.contenido = contenido
        self.fecha_envio = fecha_envio
        self.leido = Estado = leido
        self.adjuntos = adjuntos

    def remitente(self):
        return self.remitente
    
    def destinatario(self):
        return self.destinatario

    def asunto(self):
        return self.asunto
    
    def contenido(self):
        return self.contenido
    
    def fecha_envio(self):
        return datetime.now()

    def adjuntos(self):
        return self.adjuntos

    def Estado(self):
        self.estado = bool
    
    def __str__(self):
        return (f"De: {self.remitente}\nPara: {self.destinatario} Asunto: {self.asunto}\nFecha: {self.fecha_envio}\nLeído: {self.leido}\nAdjuntos: {', '.join(self.adjuntos)}")
