class Carpeta():
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.mensajes: List[Mensaje] = []

    def crear_subcarpeta(self, nombre: str):
        self.nombre = nombre
        self.mensajes = []

    def eliminar_subcarpeta(self):
        self.nombre = ""
        self.mensajes = []

    def agregar_mensaje(self, mensaje: Mensaje):
        if isinstance(mensaje, Mensaje):
            self.__mensajes.append(mensaje)
        else:
            raise TypeError("Solamente se agregan objetos de clase Mensaje")
    # uso insistance para asegurar que el mensaje pertenezca a la clase Mensaje
    # y el TypeError para avisar mediante un error que no estamos agregando un objeto de clase Mensaje
         
    def eliminar_mensaje(self, mensaje: Mensaje):
        if mensaje in self.__mensajes:
            self.__mensajes.remove(mensaje)

    def listar_mensaje(self) -> List[Mensaje]:
        return self.mensajes
