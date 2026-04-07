import pygame as pg
from modules import variables as var
import modules.musica as ms

def crear_form_base(dict_for_data: dict) -> dict:
    """
    Crea la base de un formulario

    Args:
        dict_for_data (dict): El diccionario de datos

    Returns:
        dict: Devuelve una base de formularios con los datos ingresados
    """

    form = {}
    form["nombre"] = dict_for_data.get("nombre")
    form["pantalla"] = dict_for_data.get("pantalla")
    form["activo"] = dict_for_data.get("activo")
    form["x_coord"] = dict_for_data.get("x_coord")
    form["y_coord"] = dict_for_data.get("y_coord")
    form["ruta_musica"] = dict_for_data.get("ruta_musica")
    # Guardar imagen original para poder re-escalarla
    form["imagen_original"] = pg.image.load(dict_for_data.get("fondo_pantalla")).convert_alpha()
    form["superficie"] = pg.transform.scale(form.get("imagen_original"), var.PANTALLA)
    form["rect"] = form.get("superficie").get_rect()
    form["rect"].x = dict_for_data.get("coords")[0]
    form["rect"].y = dict_for_data.get("coords")[1]
    form["config_musica"] = dict_for_data.get("config_musica")

    return form

def encender_musica(dict_form_datos: dict):
    """

    Args:
        dict_form_dict (dict): _description_
    """

    if dict_form_datos.get("config_musica").get("musica_encendida"):
        ruta_music = dict_form_datos.get("ruta_musica")
        ms.configurar_ruta_music(ruta_music)
        ms.play_music()


def apagar_musica(dict_form_datos: dict):
    """_summary_

    Args:
        dict_form_datos (dict): _description_
    """

    if not dict_form_datos.get("config_musica").get("musica_encendida"):
        ms.stop_music()

def activar_form(nombre: str):
    """
    Activa el formulario

    Args:
        nombre (str): _description_
    """
    for form in var.dict_categorias_forms.values():
        form["activo"] = False

    form_actual = var.dict_categorias_forms[nombre]
    form_actual["activo"] = True

    apagar_musica(form_actual)
    encender_musica(form_actual)

def cambiar_pantalla(form_name: str):
    """
    Cambia la pantalla actual

    Args:
        form_name (str): Nombre del formulario a activar
    """
    activar_form(form_name)
    
    # Resetear estado de form_resultado si es necesario
    if form_name == "resultado":
        resultado_form = var.dict_categorias_forms.get("resultado")
        if resultado_form:
            resultado_form["nickname"] = ""
            resultado_form["puntaje_guardado"] = False
            resultado_form["guardar_presionado"] = False
            resultado_form["cursor_visible"] = True
            resultado_form["tiempo_cursor"] = 0
    
    # Resetear cronometro de juego al volver a jugar
    if form_name == "app":
        app_form = var.dict_categorias_forms.get("app")
        if app_form:
            app_form["cronometro_iniciado"] = False
            app_form["juego_terminado"] = False


def dibujar_widgets(form_datos: dict):
    """
    Dibuja los widgets en la pantalla

    Args:
        form_datos (dict): Diccionario con los datos del formulario
    """
    for widget in form_datos.get("lista_widgets"):
        widget.draw()



def actualizar_widgets(form_datos: dict):
    """
    Actualiza los widgets en la pantalla

    Args:
        form_datos (dict): Diccionario con los datos del formulario
    """
    for widget in form_datos.get("lista_widgets"):
        widget.update()


def actualizar(form_datos: dict):
    """
    Actualiza el formulario

    Args:
        form_datos (dict): Diccionario con los datos del formulario
    """
    actualizar_widgets(form_datos)


def dibujar(form_datos: dict):
    """
    Dibuja el formulario

    Args:
        form_datos (dict): Diccionario con los datos del formulario
    """
    form_datos["pantalla"].blit(form_datos.get("superficie"), form_datos.get("rect"))


def redimensionar_superficie(form_datos: dict):
    """
    Re-escala la superficie cuando se redimensiona la ventana

    Args:
        form_datos (dict): Diccionario con los datos del formulario
    """
    if "imagen_original" in form_datos:
        form_datos["superficie"] = pg.transform.scale(form_datos.get("imagen_original"), var.PANTALLA)
        form_datos["rect"] = form_datos.get("superficie").get_rect()
        form_datos["rect"].x = 0
        form_datos["rect"].y = 0