def buscar_carpeta_por_nombre(carpeta_actual: Carpeta, nombre_buscado: str) -> Optional[Carpeta]:
    # Busca recursivamente una carpeta por nombre en el árbol de carpetas.
    # Caso base: Si la carpeta actual es None, retorna None
    if carpeta_actual is None:
        return None
    # Caso base: Si la carpeta actual coincide con el nombre buscado, retorna la carpeta
    if carpeta_actual.nombre == nombre_buscado:
        return carpeta_actual
   
    # Llamada recursiva a cada subcarpeta
    # O(N) en el peor caso, donde N es el número total de carpetas
    for subcarpeta in carpeta_actual.subcarpetas:
        resultado = buscar_carpeta_por_nombre(subcarpeta, nombre_buscado)
        if resultado:
            return resultado


def mover_mensaje(raiz: Carpeta, mensaje: Mensaje, nombre_destino: str) -> bool:
    # Mueve un mensaje (objeto) a la carpeta destino.
    # Localiza y elimina el mensaje de su origen.
   
    # Busca la carpeta destino (O(N)), donde N es el número de carpetas
    carpeta_destino = buscar_carpeta_por_nombre(raiz, nombre_destino)
   
    # Si no se encuentra la carpeta destino, retorna False
    if not carpeta_destino:
        print(f"Error: Carpeta destino '{nombre_destino}' no encontrada.")
        return False


    # Se usa una variable no local para indicar si se encontró el mensaje
    origen_encontrado = False
   
    # Función interna para búsqueda y eliminación del mensaje, usando recursión
    # O(N * M_i) en el peor caso donde N es el número de carpetas y M_i es el número de mensajes en cada carpeta
    def buscar_y_eliminar_origen(c: Carpeta):
        nonlocal origen_encontrado
        # Caso base: Si la carpeta es None, retorna
        if c is None or origen_encontrado:
            return
        # Si el mensaje está en la carpeta actual, lo elimina y marca que encontró el origen
        if mensaje in c.mensajes:
            c.eliminar_mensaje(mensaje)
            origen_encontrado = True
            return
        # Llamada recursiva a las subcarpetas, si no se ha encontrado aún
        for sub in c.subcarpetas:
            buscar_y_eliminar_origen(sub)
            if origen_encontrado:
                return
    # Busca y elimina el mensaje de su carpeta origen
    buscar_y_eliminar_origen(raiz)
    # Si no se encontró el mensaje en ninguna carpeta, retorna False
    if not origen_encontrado:
        print("Error: Mensaje no encontrado en ninguna carpeta para mover.")
        return False


    #Agrega mensaje a la carpeta destino, con tiempo O(1), ya que es una inserción al final de la lista
    carpeta_destino.agregar_mensaje(mensaje)
    return True


def busqueda_recursiva_mensajes(carpeta_actual: Carpeta, termino: str, campo: str) -> List[tuple[Mensaje, str]]:
    # Realiza una búsqueda recursiva por 'asunto' o 'remitente' y devuelve una lista de tuplas (Mensaje, nombre_carpeta).
    # Args:
    #    carpeta_actual (Carpeta): La carpeta actual que se está procesando (inicialmente la raíz).
    resultados = []
   
    # Busca mensaje en la carpeta actual, con tiempo tiempo O(M), donde M es el número de mensajes en la carpeta actual
    for mensaje in carpeta_actual.mensajes:
        valor = getattr(mensaje, campo, None) # Obtiene el valor de 'asunto' o 'remitente'
        # Si el valor existe y contiene el término de búsqueda, usando lower() para no distinguir mayúsculas/minúsculas
        if valor and termino.lower() in valor.lower():
            resultados.append((mensaje, carpeta_actual.nombre))


    # Llama recursivamente a las subcarpetas, con tiempo O(N), donde N es el número de subcarpetas
    # Retorna la lista acumulada de resultados
    for subcarpeta in carpeta_actual.subcarpetas:
        resultados.extend(busqueda_recursiva_mensajes(subcarpeta, termino, campo))
    return resultados