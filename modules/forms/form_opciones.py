import pygame as pg
import modules.variables as var
import modules.musica as musica
from modules.forms import(
    form_base as fbase,
)
from utn_fra.pygame_widgets import(
    Button
)

def cambiar_musica_on(param=None):
    """Activa la música"""
    musica.play_music()

def cambiar_musica_off(param=None):
    """Desactiva la música"""
    musica.stop_music()

def crear_form_opciones(dict_for_data: dict) -> dict:
    """
    Crea el formulario de opciones con controles de música y volumen

    Args:
        dict_for_data (dict): Datos del formulario

    Returns:
        dict: Diccionario con los datos del formulario
    """

    form = fbase.crear_form_base(dict_for_data)
    
    form["btn_musica_on"] = Button(x= var.PANTALLA[0] // 2 - 100, y=200,
                            text="MUSIC ON", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=20,
                            color= pg.Color("green"), on_click=cambiar_musica_on,
                            on_click_param=None)
    
    form["btn_musica_off"] = Button(x= var.PANTALLA[0] // 2 + 100, y=200,
                            text="MUSIC OFF", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=20,
                            color= pg.Color("red"), on_click=cambiar_musica_off,
                            on_click_param=None)
    
    form["btn_volver"] = Button(x= var.PANTALLA[0] // 2, y=520,
                            text="VOLVER", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click=fbase.cambiar_pantalla,
                            on_click_param="menu")

    form["lista_widgets"] = [
        form.get("btn_musica_on"),
        form.get("btn_musica_off"),
        form.get("btn_volver")
    ]
    
    # Variables para controlar el volumen
    form["volumen"] = 30  # Volumen inicial en porcentaje (0-100)
    form["barra_volumen_rect"] = pg.Rect(var.PANTALLA[0] // 2 - 150, 320, 300, 20)
    form["barra_volumen_slider_rect"] = pg.Rect(var.PANTALLA[0] // 2 - 150 + (form["volumen"] / 100) * 300 - 10, 315, 20, 30)
    form["arrastrando_slider"] = False

    var.dict_categorias_forms[form.get("nombre")]  = form

    return form


def dibujar_barra_volumen(dict_form_datos: dict):
    """
    Dibuja la barra de volumen y su slider

    Args:
        dict_form_datos (dict): Datos del formulario
    """
    pantalla = dict_form_datos.get("pantalla")
    barra_rect = dict_form_datos.get("barra_volumen_rect")
    slider_rect = dict_form_datos.get("barra_volumen_slider_rect")
    
    # Dibujar fondo de la barra
    pg.draw.rect(pantalla, pg.Color("gray"), barra_rect)
    
    # Dibujar barra de progreso
    volumen_rect = pg.Rect(barra_rect.x, barra_rect.y, (dict_form_datos.get("volumen") / 100) * barra_rect.width, barra_rect.height)
    pg.draw.rect(pantalla, pg.Color("green"), volumen_rect)
    
    # Dibujar slider
    pg.draw.rect(pantalla, pg.Color("white"), slider_rect)
    
    # Dibujar texto del porcentaje
    fuente = pg.font.Font(var.FUENTE, 18)
    texto_volumen = fuente.render(f"{dict_form_datos.get('volumen')}%", True, pg.Color("white"))
    pantalla.blit(texto_volumen, (var.PANTALLA[0] // 2 - 20, 360))


def dibujar(dict_form_datos: dict):
    """
    Dibuja el formulario de opciones

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.dibujar(dict_form_datos)
    fbase.dibujar_widgets(dict_form_datos)
    dibujar_barra_volumen(dict_form_datos)


def actualizar(dict_form_datos: dict):
    """
    Actualiza el formulario de opciones

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.actualizar(dict_form_datos)
    
    # Manejar el slider de volumen
    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()
    
    slider_rect = dict_form_datos.get("barra_volumen_slider_rect")
    barra_rect = dict_form_datos.get("barra_volumen_rect")
    
    # Detectar clic en el slider
    if mouse_pressed[0] and slider_rect.collidepoint(mouse_pos):
        dict_form_datos["arrastrando_slider"] = True
    
    # Soltar el slider
    if not mouse_pressed[0]:
        dict_form_datos["arrastrando_slider"] = False
    
    # Si se está arrastrando, ajustar el volumen
    if dict_form_datos.get("arrastrando_slider"):
        # Calcular la nueva posición del volumen
        volumen_nuevo = int(((mouse_pos[0] - barra_rect.x) / barra_rect.width) * 100)
        volumen_nuevo = max(0, min(100, volumen_nuevo))  # Limitar entre 0 y 100
        
        dict_form_datos["volumen"] = volumen_nuevo
        
        # Actualizar posición del slider
        new_slider_x = barra_rect.x + (volumen_nuevo / 100) * barra_rect.width - 10
        dict_form_datos["barra_volumen_slider_rect"] = pg.Rect(new_slider_x, 315, 20, 30)
        
        # Cambiar volumen de la música
        musica.cambiar_volumen(volumen_nuevo / 100)