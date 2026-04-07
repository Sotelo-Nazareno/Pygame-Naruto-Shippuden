import pygame as pg
import modules.variables as var
import random
from modules.forms import(
    form_base as fbase
)

class Enemigo:
    """Clase que representa un enemigo en el juego"""
    def __init__(self, imagen, x, y, puntos=10):
        self.imagen = imagen
        self.rect = imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.puntos = puntos

def crear_form_app(dict_for_data: dict) -> dict:
    """
    Crea el formulario de aplicación (juego principal)

    Args:
        dict_for_data (dict): Datos del formulario

    Returns:
        dict: Diccionario con los datos del formulario
    """

    form = fbase.crear_form_base(dict_for_data)

    # Variables del juego
    form["puntaje"] = 0
    form["tiempo_total"] = 60000  # 1 minuto en milisegundos
    form["tiempo_inicio"] = pg.time.get_ticks()
    form["tiempo_pausado"] = 0  # Tiempo acumulado en pausa
    form["pausa_presionada"] = False
    form["juego_terminado"] = False
    form["estaba_en_pausa"] = False
    form["cronometro_iniciado"] = False
    
    # Cargar imágenes de enemigos
    rutas_enemigos = [
        "assets/img/enemigos/enemy1.png",
        "assets/img/enemigos/enemy2.png",
        "assets/img/enemigos/enemy3.png",
        "assets/img/enemigos/enemy4.png"
    ]
    
    form["imagenes_enemigos"] = []
    for ruta in rutas_enemigos:
        try:
            img = pg.image.load(ruta).convert_alpha()
            img = pg.transform.scale(img, (120, 120))
            form["imagenes_enemigos"].append(img)
        except:
            pass
    
    form["enemigos"] = []
    form["contador_spawn"] = 0
    form["frecuencia_spawn"] = 60  # Cada 60 frames aparece un nuevo enemigo
    
    # Cargar sonido de golpe
    try:
        form["sonido_golpe"] = pg.mixer.Sound(var.GOLPES)
    except:
        form["sonido_golpe"] = None
    
    form["lista_widgets"] = []
    form["eventos"] = []
    
    var.dict_categorias_forms[form.get("nombre")] = form

    return form


def crear_enemigo_aleatorio(form):
    """Crea un enemigo en posición aleatoria"""
    if form["imagenes_enemigos"]:
        img = random.choice(form["imagenes_enemigos"])
        x = random.randint(50, var.PANTALLA[0] - 170)
        y = random.randint(80, var.PANTALLA[1] - 180)
        enemigo = Enemigo(img, x, y, puntos=10)
        form["enemigos"].append(enemigo)


def obtener_tiempo_restante(form):
    """Calcula el tiempo restante del juego en milisegundos"""
    tiempo_actual = pg.time.get_ticks()
    tiempo_transcurrido = tiempo_actual - form["tiempo_inicio"]
    tiempo_restante = max(0, form["tiempo_total"] - tiempo_transcurrido)
    return tiempo_restante


def convertir_ms_a_mm_ss(milisegundos):
    """Convierte milisegundos a formato MM:SS"""
    segundos = milisegundos // 1000
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02d}:{segundos:02d}"


def dibujar(dict_form_datos: dict):
    """
    Dibuja el formulario del juego

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.dibujar(dict_form_datos)
    
    pantalla = dict_form_datos.get("pantalla")
    
    # Dibujar enemigos
    for enemigo in dict_form_datos.get("enemigos", []):
        pantalla.blit(enemigo.imagen, (enemigo.rect.x, enemigo.rect.y))
    
    # Dibujar timer en la parte superior izquierda
    tiempo_restante = obtener_tiempo_restante(dict_form_datos)
    tiempo_texto = convertir_ms_a_mm_ss(tiempo_restante)
    
    fuente_timer = pg.font.Font(var.FUENTE, 40)
    texto_timer = fuente_timer.render(tiempo_texto, True, pg.Color("yellow"))
    pantalla.blit(texto_timer, (20, 20))
    
    # Dibujar puntaje en la parte inferior izquierda
    fuente_puntaje = pg.font.Font(var.FUENTE, 30)
    texto_puntaje = fuente_puntaje.render(f"Puntos: {dict_form_datos.get('puntaje')}", True, pg.Color("white"))
    pantalla.blit(texto_puntaje, (20, var.PANTALLA[1] - 50))


def actualizar(dict_form_datos: dict):
    """
    Actualiza el formulario del juego

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    # Resetear el juego si fue reiniciado
    if dict_form_datos.get("juego_terminado"):
        dict_form_datos["puntaje"] = 0
        dict_form_datos["tiempo_inicio"] = pg.time.get_ticks()
        dict_form_datos["juego_terminado"] = False
        dict_form_datos["enemigos"] = []
        dict_form_datos["contador_spawn"] = 0
    
    # Iniciar cronómetro si aún no ha sido inicializado en esta sesión
    if not dict_form_datos.get("cronometro_iniciado"):
        dict_form_datos["tiempo_inicio"] = pg.time.get_ticks()
        dict_form_datos["cronometro_iniciado"] = True
    
    fbase.actualizar(dict_form_datos)
    
    # Verificar si el juego ha terminado
    tiempo_restante = obtener_tiempo_restante(dict_form_datos)
    
    if tiempo_restante <= 0 and not dict_form_datos.get("juego_terminado"):
        dict_form_datos["juego_terminado"] = True
        # Pasar el puntaje al formulario de resultado y cambiara a él
        lista_forms = var.dict_categorias_forms.get("resultado")
        if lista_forms:
            lista_forms["puntaje_final"] = dict_form_datos.get("puntaje")
        fbase.cambiar_pantalla("resultado")
        return
    
    # Generar enemigos de forma aleatoria
    dict_form_datos["contador_spawn"] += 1
    if dict_form_datos["contador_spawn"] >= dict_form_datos["frecuencia_spawn"]:
        crear_enemigo_aleatorio(dict_form_datos)
        dict_form_datos["contador_spawn"] = 0
    
    # Manejar clics en enemigos
    mouse_pressed = pg.mouse.get_pressed()
    if mouse_pressed[0]:  # Clic izquierdo
        mouse_pos = pg.mouse.get_pos()
        enemigos_para_eliminar = []
        
        for enemigo in dict_form_datos.get("enemigos", []):
            if enemigo.rect.collidepoint(mouse_pos):
                dict_form_datos["puntaje"] += enemigo.puntos
                enemigos_para_eliminar.append(enemigo)
                # Reproducir sonido de golpe
                sonido = dict_form_datos.get("sonido_golpe")
                if sonido:
                    sonido.play()
        
        # Eliminar enemigos clickeados
        for enemigo in enemigos_para_eliminar:
            dict_form_datos["enemigos"].remove(enemigo)
    
    # Manejar tecla ESC para pausar
    eventos = dict_form_datos.get("eventos", [])
    for event in eventos:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            if not dict_form_datos.get("pausa_presionada"):
                fbase.cambiar_pantalla("pausa")
                dict_form_datos["pausa_presionada"] = True
            break
    
    # Reset pausa cuando se suelta la tecla
    keys = pg.key.get_pressed()
    if not keys[pg.K_ESCAPE]:
        dict_form_datos["pausa_presionada"] = False
