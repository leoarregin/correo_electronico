from InterfazMensajeria import InterfazMensajeria
from Usuario import Usuario 
from Mensaje import Mensaje
from GestorBuzon import GestorBuzon
from ColaPrioridadesMensajes import ColaPrioridadesMensajes
from RedServidores import RedServidores
from ServidorCorreo import ServidorCorreo
from Carpeta import Carpeta
import os # Importa el módulo os
from typing import List, Optional, Tuple, Any, Dict # importa de typing los tipos List y Optional para anotaciones de tipo
from datetime import datetime #Importa datetime para manejo de fechas
from abc import ABC, abstractmethod # Importa ABC y abstractmethod para definir clases abstractas
from collections import deque # Importa deque para la red de servidores
import time # Importa time para pausas y animaciones
import sys

def imprimir_estructura_carpetas_simple(carpeta_actual: 'Carpeta', nivel: int = 0):
    if carpeta_actual is None: return
    
    indentacion = '│   ' * nivel
    no_leidos = sum(1 for m in carpeta_actual.mensajes if not m.estado_leido)
    
    info_adicional = f"({len(carpeta_actual.mensajes)} total"
    if no_leidos > 0:
        info_adicional += f", {no_leidos} NO LEÍDOS 🔔"
    info_adicional += ")"
    
    print(f"{indentacion}└── 📁 {carpeta_actual.nombre} {info_adicional}")

    for subcarpeta in carpeta_actual.subcarpetas:
        imprimir_estructura_carpetas_simple(subcarpeta, nivel + 1)

def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# ----------------------------------------------------------------------
# --- ESTADO GLOBAL Y CASOS DE USO (Simulación de Datos)             ---
# ----------------------------------------------------------------------

USUARIO_ACTUAL: Optional['Usuario'] = None
CORREO_SERVER: Optional['ServidorCorreo'] = None
RED_SERVIDORES: Optional['RedServidores'] = None
COLA_MENSAJES_URGENTES = ColaPrioridadesMensajes()

# ------------------------------------ #
# --- FUNCIÓN REFINADA DE INICIALIZACIÓN ---
# ------------------------------------ #
def inicializar_simulacion():
    # Configura la red, el servidor y precarga usuarios/mensajes para demostración. """
    global CORREO_SERVER, RED_SERVIDORES, RED_TOPOLOGIA
    
    # 2. CONFIGURACIÓN DE PRUEBA
    RED_TOPOLOGIA = {
        'S_MADRID': ['S_PARIS', 'S_LISBOA'], 'S_PARIS': ['S_MADRID', 'S_BERLIN', 'S_LONDRES'],
        'S_LISBOA': ['S_MADRID', 'S_NY'], 'S_LONDRES': ['S_PARIS', 'S_NY'],
        'S_BERLIN': ['S_PARIS'], 'S_NY': ['S_LISBOA', 'S_LONDRES', 'S_TOKIO'],
        'S_TOKIO': ['S_NY'], 'S_ISLA': [] # Servidor aislado
    }
    
    RED_SERVIDORES = RedServidores(RED_TOPOLOGIA) 
    CORREO_SERVER = ServidorCorreo(RED_SERVIDORES)
    
    print("Sistema de Correo Inicializado con la red de servidores.")
    
    try:
        CORREO_SERVER.registrar_usuario("alice", "pass1")
        CORREO_SERVER.registrar_usuario("bob", "pass2")
        CORREO_SERVER.registrar_usuario("ceo", "pass3")
    except ValueError:
        pass

    alice_inst = CORREO_SERVER.buscar_usuario("alice")
    
    if alice_inst:
        # Configuración inicial de Alice
        trabajo = alice_inst.buzon_raiz.crear_subcarpeta("Trabajo")
        trabajo.crear_subcarpeta("Proyectos")
        alice_inst.buzon_raiz.crear_subcarpeta("Personal").crear_subcarpeta("Facturas")
        alice_inst.buzon_raiz.crear_subcarpeta("Spam") 
        
        # Filtros pre-existentes
        alice_inst.definir_regla_filtro(nombre_carpeta="Facturas", reglas={"remitente": "bank", "asunto": "factura"})
        alice_inst.definir_regla_filtro(nombre_carpeta="Spam", reglas={"asunto": "oferta"})
        
        # Mensajes pre-cargados
        alice_inst._recibir_mensaje("ceo", "Reporte de Ventas", "Adjunto el archivo.", datetime.now(), False, ["reporte.xlsx"]) 
        alice_inst._recibir_mensaje("visa@bank.com", "Tu factura de tarjeta", "Monto a pagar...", datetime.now(), False) 
        alice_inst._recibir_mensaje("ads@promo.net", "Gran Oferta de Verano", "No te la pierdas.", datetime.now(), False) 
        
        # Mensajes con distintos estados
        msg_rapida = Mensaje("bob", "alice", "Consulta rápida (LEÍDO)", "Hola.", datetime.now(), True)
        alice_inst.recibidos.agregar_mensaje(msg_rapida)
        
        # Mensaje URGENTE (para probar la cola de prioridad si se implementa más adelante)
        msg_urgente = Mensaje("ceo", "alice", "URGENTE: Reunión ahora", "Ven a mi oficina.", datetime.now(), False)
        msg_urgente.es_urgente = True
        alice_inst.recibidos.agregar_mensaje(msg_urgente)

# ------------------------------------ #
# --- FUNCIÓN REFINADA DE CASO DE USO ---
# ------------------------------------ #
def demostrar_uc_red_servidores():
    # Ejecuta los escenarios del Caso de Uso UC-RS-001 (Búsqueda de Ruta Óptima)."""
    
    if RED_SERVIDORES is None: return
    red_servidores = RED_SERVIDORES
    
    print("\n" + "="*70)
    print("CASO DE USO: DEMOSTRACIÓN DE BÚSQUEDA DE RUTA ÓPTIMA (RedServidores)")
    print("="*70)
    
    def ejecutar_prueba(origen, destino):
        ruta = red_servidores.buscar_ruta_envio(origen, destino)
        if ruta:
            print(f"  ✅ Ruta ({origen} -> {destino}): {' -> '.join(ruta)} (Saltos: {len(ruta) - 1})")
        elif ruta is None:
            print(f"  ❌ Ruta ({origen} -> {destino}): RUTA NO ENCONTRADA / SERVIDOR INEXISTENTE.")
        else:
            print(f"  ⚠️ Ruta ({origen} -> {destino}): Error inesperado.")

    print("\n--- 1. FLUJO PRINCIPAL: Ruta Existente (Búsqueda BFS) ---")
    ejecutar_prueba('S_MADRID', 'S_TOKIO') # S_MADRID -> S_LISBOA -> S_NY -> S_TOKIO
    ejecutar_prueba('S_BERLIN', 'S_NY') # S_BERLIN -> S_PARIS -> S_LONDRES -> S_NY
    
    print("\n--- 2. EXCEPCIÓN E1: Servidor Inexistente ---")
    ejecutar_prueba('S_NULO', 'S_NY')
    ejecutar_prueba('S_MADRID', 'S_OTRO')
    
    print("\n--- 3. EXCEPCIÓN E2: No Existe Conexión (Aislado) ---")
    ejecutar_prueba('S_MADRID', 'S_ISLA')
    ejecutar_prueba('S_ISLA', 'S_PARIS')
    
    print("\n--- 4. CASO ESPECIAL: Origen = Destino ---")
    ejecutar_prueba('S_LONDRES', 'S_LONDRES')

# ----------------------------------------------------------------------
# --- FUNCIONES DE PROCESAMIENTO DE LA CLI (Refinadas) ---
# ----------------------------------------------------------------------

def procesar_login():
    global USUARIO_ACTUAL
    nombre = input("\nUsuario: ")
    contrasena = input("Contraseña: ")
    try:
        USUARIO_ACTUAL = CORREO_SERVER.autenticar_usuario(nombre, contrasena)
        print(f"\n✅ ¡Inicio de sesión exitoso como {nombre}!")
        time.sleep(1) # Pausa para ver mensaje
        limpiar_pantalla()
        return True
    except ValueError as e:
        print(f"\n❌ Error de autenticación: {e}")
        input("Presiona Enter para continuar...")
        return False

def procesar_redactar_mejorado(usuario: 'Usuario'):
    limpiar_pantalla()
    print("\n--- REDACTAR MENSAJE ---")
    destinatario = input("Destinatario: ")
    asunto = input("Asunto: ")
    contenido = input("Contenido:\n")
    
    urgente_input = input("Marcar como URGENTE? (s/N): ").lower()
    es_urgente = (urgente_input == 's')
    
    adjuntos_str = input("Adjuntos (separados por coma) [Dejar vacío]: ")
    adjuntos = [a.strip() for a in adjuntos_str.split(',') if a.strip()]
    
    try:
        usuario._enviar_mensaje(destinatario, asunto, contenido, datetime.now(), False, adjuntos, es_urgente=es_urgente)
    except Exception as e:
        print(f"\n❌ Error al enviar: {e}")

def procesar_ver_mensajes_resumen(usuario: 'Usuario'):
    nombre_carpeta = input("\nNombre de la carpeta a listar (ej: Recibidos): ")
    try:
        carpeta_buscada = GestorBuzon.buscar_carpeta_por_nombre(usuario.buzon_raiz, nombre_carpeta)
        if not carpeta_buscada: raise ValueError(f"Carpeta '{nombre_carpeta}' no encontrada.")

        mensajes_ordenados = sorted(carpeta_buscada.mensajes, key=lambda m: (m.estado_leido, m.fecha_envio), reverse=True)
        
        limpiar_pantalla()
        print(f"\n--- MENSAJES EN '{carpeta_buscada.nombre.upper()}' ({len(mensajes_ordenados)}) ---")
        if not mensajes_ordenados: print("Carpeta vacía."); return

        for i, msg in enumerate(mensajes_ordenados):
            leido = "🔔" if not msg.estado_leido else "  "
            urgente = "⚡" if msg.es_urgente else ""
            print(f"[{i + 1:2}] {leido}{urgente} {msg.fecha_envio.strftime('%H:%M')} | {msg.asunto[:40]:40}... (De: {msg.remitente})")
        
        opcion_ver = input("\nNúmero de mensaje para ver detalle / gestionar (o 0 para volver): ")
        if not opcion_ver.isdigit() or not (1 <= int(opcion_ver) <= len(mensajes_ordenados)): return

        mensaje_sel = mensajes_ordenados[int(opcion_ver) - 1]
        procesar_gestion_mensaje_avanzada(usuario, mensaje_sel)

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        
def procesar_gestion_mensaje_avanzada(usuario: 'Usuario', mensaje_sel: 'Mensaje'):
    limpiar_pantalla()
    print("\n" + "="*50)
    print("DETALLE DEL MENSAJE")
    print(mensaje_sel)
    print("="*50)
    
    if not mensaje_sel.estado_leido:
        mensaje_sel.estado_leido = True
        print("\n✅ Mensaje marcado como LEÍDO.")
        
    print("\n--- ACCIONES ---")
    print("1. Mover a otra Carpeta")
    print("2. Eliminar (Mover a Papelera)")
    print("3. Volver")
    
    accion = input("Elige una acción (1-3): ")

    if accion == '1':
        nombre_destino = input("Nombre de la carpeta destino (ej: 'Trabajo'): ")
        if GestorBuzon.mover_mensaje(usuario.buzon_raiz, mensaje_sel, nombre_destino):
             print(f"\n✅ Mensaje movido a '{nombre_destino}'.")
        else:
             print("\n❌ No se pudo mover el mensaje.")
    elif accion == '2':
        if GestorBuzon.mover_mensaje(usuario.buzon_raiz, mensaje_sel, "Papelera"):
            print(f"\n✅ Mensaje movido a 'Papelera'.")
        else:
            print("\n❌ Error al intentar mover el mensaje a Papelera.")

def procesar_busqueda(usuario: 'Usuario'):
    limpiar_pantalla()
    print("\n--- BÚSQUEDA DE MENSAJES ---")
    termino = input("Término de búsqueda: ")
    campo = input("Buscar por (asunto/remitente): ").lower()
    
    if campo not in ["asunto", "remitente"]:
        print("\n❌ Campo de búsqueda inválido. Debe ser 'asunto' o 'remitente'.")
        return

    resultados = GestorBuzon.busqueda_recursiva_mensajes(usuario.buzon_raiz, termino, campo)

    print(f"\n--- RESULTADOS DE BÚSQUEDA para '{termino}' ({len(resultados)}) ---")
    if not resultados:
        print("No se encontraron mensajes.")
        return

    for mensaje, carpeta in resultados:
        leido = "(Leído)" if mensaje.estado_leido else "(NO LEÍDO) 🔔"
        urgente = "⚡" if mensaje.es_urgente else ""
        print(f" [Carpeta: {carpeta}] {urgente}{leido} {mensaje.asunto[:40]}... (De: {mensaje.remitente})")

def procesar_crear_carpeta(usuario: 'Usuario'):
    limpiar_pantalla()
    print("\n--- CREAR NUEVA CARPETA ---")
    nombre_nueva = input("Nombre de la nueva carpeta: ")
    nombre_padre = input("Carpeta padre (ej: 'Bandeja Principal') [Dejar vacío para crear en la raíz]: ").strip()
    
    carpeta_padre = usuario.buzon_raiz
    if nombre_padre:
        carpeta_padre_temp = GestorBuzon.buscar_carpeta_por_nombre(usuario.buzon_raiz, nombre_padre)
        if carpeta_padre_temp: carpeta_padre = carpeta_padre_temp
        else: print(f"\n⚠️ Advertencia: Carpeta padre '{nombre_padre}' no encontrada. Creando en la raíz.")
    
    if any(sub.nombre.lower() == nombre_nueva.lower() for sub in carpeta_padre.subcarpetas):
        print(f"\n❌ Error: Ya existe una carpeta llamada '{nombre_nueva}' en '{carpeta_padre.nombre}'."); return
        
    try:
        carpeta_padre.crear_subcarpeta(nombre_nueva)
        print(f"\n✅ Carpeta '{nombre_nueva}' creada exitosamente bajo '{carpeta_padre.nombre}'.")
    except Exception as e:
        print(f"\n❌ Error al crear carpeta: {e}")

def procesar_gestion_carpetas(usuario: 'Usuario'):
    while True:
        limpiar_pantalla()
        print("\n--- GESTIÓN AVANZADA DE CARPETAS ---")
        print("\n[Estructura Actual del Buzón]")
        imprimir_estructura_carpetas_simple(usuario.buzon_raiz) 
        print("\n" + "="*50)
        print("1. Crear Nueva Carpeta")
        print("2. Definir Regla de Filtro")
        print("3. Eliminar Carpeta (Debe estar vacía)")
        print("4. Volver al Menú Principal")
        print("="*50)
        
        opcion = input("Elige una opción de gestión (1-4): ")

        if opcion == '1': procesar_crear_carpeta(usuario)
        elif opcion == '2': procesar_definir_filtro(usuario)
        elif opcion == '3': procesar_eliminar_carpeta(usuario)
        elif opcion == '4': print("Volviendo al menú principal."); break
        else: print("\n❌ Opción no válida.")
        
        input("\nPresiona Enter para continuar...")

def procesar_eliminar_carpeta(usuario: 'Usuario'):
    # Permite al usuario eliminar una carpeta existente, siempre que esté vacía.
    
    limpiar_pantalla()
    print("--- 🗑️ Eliminar Carpeta ---")
    
    # Mostrar la estructura actual para referencia
    print("\nEstructura de Carpetas Actual:")
    GestorBuzon.imprimir_estructura_arbol(usuario.raiz_buzon)
    
    nombre_eliminar = input("\nIngresa el nombre exacto de la carpeta a eliminar: ").strip()

    if nombre_eliminar.upper() in USUARIO_CARPETAS_RESERVADAS:
        print("\n❌ Error: No se pueden eliminar carpetas reservadas (Bandeja Principal, Enviados, etc.).")
        input("Presiona Enter para continuar...")
        return
        
    # El método eliminar_carpeta debe estar implementado en GestorBuzon o Usuario
    # Asumimos que la lógica de eliminar está en el objeto Usuario, que llama a GestorBuzon.
    try:
        if usuario.eliminar_carpeta(nombre_eliminar): 
            print(f"\n✅ Carpeta '{nombre_eliminar}' eliminada con éxito.")
        else:
            print(f"\n⚠️ Error: La carpeta '{nombre_eliminar}' no existe, no está vacía, o es una carpeta raíz reservada.")
    except Exception as e:
        print(f"\n❌ Ocurrió un error inesperado al intentar eliminar: {e}")

    input("\nPresiona Enter para continuar...")
    limpiar_pantalla()

def procesar_cambio_contrasena(usuario: 'Usuario'):
    # Permite al usuario cambiar su contraseña después de validación.
    limpiar_pantalla()
    print("--- 🔒 Cambio de Contraseña ---")
    
    contrasena_actual = input("Ingresa tu contraseña actual: ")
    
    # La validación depende de cómo se almacena y verifica la contraseña en Usuario
    if usuario.contrasena == contrasena_actual: 
        nueva_contrasena = input("Ingresa la nueva contraseña: ")
        confirmar_contrasena = input("Confirma la nueva contraseña: ")
        
        if nueva_contrasena and nueva_contrasena == confirmar_contrasena:
            usuario.contrasena = nueva_contrasena
            print("\n✅ Contraseña cambiada con éxito.")
        else:
            print("\n❌ Error: Las contraseñas nuevas no coinciden o están vacías.")
    else:
        print("\n❌ Error: Contraseña actual incorrecta.")
        
    input("\nPresiona Enter para continuar...")
    limpiar_pantalla()

def procesar_definir_filtro(usuario: 'Usuario'):
    """
    Permite al usuario definir reglas para que los mensajes entrantes sean 
    marcados como urgentes en su ColaPrioridadesMensajes (por receptor).
    """
    limpiar_pantalla()
    print("--- ⚙️ Definir Filtro de Prioridad de Buzón ---")
    print(f"Usuario: {usuario.correo}")

    # 1. Filtro por Palabra Clave
    palabra_actual = usuario.filtro_palabra_clave if usuario.filtro_palabra_clave else "NINGUNA"
    print(f"\n> Filtro de Palabra Clave Actual: '{palabra_actual}'")
    nueva_palabra = input("Ingresa una palabra clave para marcar como urgente (o presiona Enter para eliminar): ").strip()

    if nueva_palabra:
        usuario.filtro_palabra_clave = nueva_palabra.upper()
        print(f"✅ Palabra clave de filtro establecida a: '{usuario.filtro_palabra_clave}'")
    elif nueva_palabra == "" and usuario.filtro_palabra_clave:
        usuario.filtro_palabra_clave = ""
        print("✅ Filtro de palabra clave eliminado.")
    
    # 2. Filtro por Remitente VIP
    remitente_actual = usuario.filtro_remitente_vip if usuario.filtro_remitente_vip else "NINGUNO"
    print(f"\n> Filtro de Remitente VIP Actual: '{remitente_actual}'")
    nuevo_remitente = input("Ingresa un correo remitente VIP para marcar como urgente (o presiona Enter para eliminar): ").strip()
    
    if nuevo_remitente:
        # Se asume validación básica de formato o se utiliza sin ella
        usuario.filtro_remitente_vip = nuevo_remitente.lower()
        print(f"✅ Remitente VIP establecido a: '{usuario.filtro_remitente_vip}'")
    elif nuevo_remitente == "" and usuario.filtro_remitente_vip:
        usuario.filtro_remitente_vip = ""
        print("✅ Filtro de remitente VIP eliminado.")
        
    input("\nPresiona Enter para continuar...")
    limpiar_pantalla()

# ----------------------------------------------------------------------
# --- MENÚS Y BUCLE PRINCIPAL DE LA CLI ---
# ----------------------------------------------------------------------

# --- FUNCIÓN REFINADA DE ANIMACIÓN ---
def iniciar_botme_animado(palabra: str = "BOTME", velocidad: float = 0.05):
    limpiar_pantalla()
    print("Iniciando Botmed Message (botme)...\n")
    time.sleep(0.5)
    patrones: Dict[str, List[str]] = {
        "B": ["BBBBBBB","B     B","BBBBBBB","B     B","BBBBBBB"],
        "O": [" OOOOO ","O     O","O     O","O     O"," OOOOO "],
        "T": ["TTTTTTT","   T   ","   T   ","   T   ","   T   "],
        "M": ["M     M","MM   MM","M M M M","M  M  M","M     M"],
        "E": ["EEEEEEE","E      ","EEEEE  ","E      ","EEEEEEE"]
    }
    palabra_mayus = palabra.upper()
    
    for i in range(len(patrones['B'])):
        linea_completa = ""
        for letra in palabra_mayus:
            if letra in patrones:
                linea_completa += patrones[letra][i] + "   "
            else:
                linea_completa += "       " + "   "
        
        print(linea_completa)
        sys.stdout.flush() # Forzar la impresión inmediatamente
        time.sleep(velocidad)

    print("\n")
    print("¡Sistema botme operativo! \nBienvenido.")
    input("Presiona Enter para continuar...")

def menu_principal():
    print("\n================================")
    print(" 📧 SIMULADOR DE CORREO (CLI)")
    print("================================")
    print("1. Iniciar Sesión (Ej: alice/pass1)")
    print("2. Registrar nuevo usuario")
    print("3. Salir")
    return input("Elige una opción: ")

def menu_usuario(usuario: 'Usuario'):
    print(f"\n=============================================")
    print(f"  BIENVENIDO, {usuario.nombre_usuario} | Buzón")
    print(f"=============================================")
    print("1. Ver Buzón Completo (Estructura) 📁")
    print("2. Redactar Mensaje (Urgente/Normal) ✍️")
    print("3. Ver/Gestionar Mensajes de Carpeta 📥")
    print("4. Buscar Mensajes (Asunto/Remitente) 🔎")
    print("5. Gestionar Carpetas y Filtros ⚙️")
    print("6. Cambiar Contraseña 🔐")
    print("7. Cerrar Sesión")
    return input("Elige una opción: ")

def main_cli():
    global USUARIO_ACTUAL
    limpiar_pantalla()

    while True:
        if USUARIO_ACTUAL is None:
            opcion = menu_principal()
            
            if opcion == '1':
                procesar_login()
            elif opcion == '2':
                # Registro se mantiene igual
                print("\n--- REGISTRO DE NUEVO USUARIO ---")
                nuevo_usuario = input("Elige un nombre de usuario: ")
                password = input("Elige una contraseña: ")
                try:
                    CORREO_SERVER.registrar_usuario(nuevo_usuario, password)
                    print(f"\n✅ Usuario '{nuevo_usuario}' registrado exitosamente. Ahora puedes iniciar sesión.")
                except ValueError as e:
                    print(f"\n❌ Error al registrar: {e}")
            elif opcion == '3':
                print("\nSaliendo del simulador. ¡Hasta luego! 👋"); break
            else:
                print("\nOpción no válida.")
                input("\nPresiona Enter para continuar...")
        else:
            opcion = menu_usuario(USUARIO_ACTUAL)
            
            if opcion == '1':
                limpiar_pantalla()
                print("\n--- ESTRUCTURA COMPLETA DEL BUZÓN ---")
                imprimir_estructura_carpetas_simple(USUARIO_ACTUAL.buzon_raiz)
            elif opcion == '2':
                procesar_redactar_mejorado(USUARIO_ACTUAL)
            elif opcion == '3':
                procesar_ver_mensajes_resumen(USUARIO_ACTUAL)
            elif opcion == '4':
                procesar_busqueda(USUARIO_ACTUAL)
            elif opcion == '5':
                procesar_gestion_carpetas(USUARIO_ACTUAL)
            elif opcion == '6':
                procesar_cambio_contrasena(USUARIO_ACTUAL)
            elif opcion == '7':
                print(f"\nAdiós, {USUARIO_ACTUAL.nombre_usuario}. Cerrando sesión.")
                USUARIO_ACTUAL = None
            else:
                print("\nOpción no válida.")
        
        # Pausa y limpieza (excepto si se está en el menú de gestión o se salió)
        if opcion not in ['5', '6', '7', '3'] and USUARIO_ACTUAL is not None:
             input("\nPresiona Enter para continuar...")
             limpiar_pantalla()
        elif opcion in ['7']:
             limpiar_pantalla()
        elif USUARIO_ACTUAL is None and opcion in ['2']:
             input("\nPresiona Enter para continuar...")
             limpiar_pantalla()

# ----------------------------------------------------------------------
# --- EJECUCIÓN DEL PROGRAMA (Secuencia Limpia) ---
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # 1. Animación de Inicio y Limpieza
    iniciar_botme_animado()
    limpiar_pantalla()

    # 2. Inicialización del sistema
    inicializar_simulacion()

    # 3. Demostración del Caso de Uso (RedServidores)
    demostrar_uc_red_servidores()
    
    input("\nPresiona Enter para continuar a la Interfaz de Mensajería...")

    # 4. Ejecución de la Interfaz CLI
    main_cli()
    main_cli()
