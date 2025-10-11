from typing import List

# Clase Mensaje
class Mensaje():
    def __init__(self, remitente, destinatario, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = None):
        self.remitente = remitente
        self.destinatario = destinatario
        self.asunto = asunto
        self.contenido = contenido
        self.fecha_envio = fecha_envio
        self.estado_leido = leido
        self.adjuntos = adjuntos if adjuntos is not None else []

    def __repr__(self):
        return f"Mensaje(Asunto: '{self.asunto}', De: '{self.remitente}')"
    
    def __str__(self):
        adjuntos_str = ', '.join(self.adjuntos)
        return (f"De: {self.remitente}\nPara: {self.destinatario}\nAsunto: {self.asunto}\nFecha: {self.fecha_envio}\nLeído: {self.estado_leido}\nAdjuntos: {adjuntos_str}")
