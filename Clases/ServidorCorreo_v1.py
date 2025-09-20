class ServidorCorreo():
    def __init__(self):
        self.usuarios: List[Usuario] = []

    def registrar_usuario(self, nombre_usuario: str, contrasena: str):
        nuevo_usuario = Usuario(nombre_usuario, contrasena)
        self.usuarios.append(nuevo_usuario)
        return True

    def autenticar_usuario(self, nombre_usuario: str, contrasena: str) -> Usuario:
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena:
                return usuario
        raise ValueError("Nombre de usuario o contraseña incorrectos.")
