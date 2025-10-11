# Importa ABC y abstractmethod para definir clases abstractas
from abc import ABC, abstractmethod
from typing import List

# Clase abstracta para definir la interfaz de mensajería (Contrato de métodos)
class InterfazMensajeria(ABC):
    @abstractmethod
    def _enviar_mensaje(self, destinatario, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = []):
        pass
    @abstractmethod
    def _recibir_mensaje(self, remitente, asunto, contenido, fecha_envio, leido, adjuntos: List[str] = []):
        pass
    @abstractmethod
    def _listar_mensaje(self, carpeta: str) -> List["Mensaje"]:
        pass
