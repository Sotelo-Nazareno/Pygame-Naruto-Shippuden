import pygame as pg
import modules.variables as var
from modules.forms import(
    form_base as fbase
)
from utn_fra.pygame_widgets import(
    Button
)

def crear_form_pausa(dict_for_data: dict) -> dict:
    """
    Crea el formulario de pausa

    Args:
        dict_for_data (dict): Datos del formulario

    Returns:
        dict: Diccionario con los datos del formulario
    """

    form = fbase.crear_form_base(dict_for_data)
    form["btn_reanudar"] = Button(x= var.PANTALLA[0] // 2, y=300,
                            text="REANUDAR", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("green"), on_click=fbase.cambiar_pantalla,
                            on_click_param="app")
    
    form["btn_menu"] = Button(x= var.PANTALLA[0] // 2, y=400,
                            text="MENU PRINCIPAL", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click=fbase.cambiar_pantalla,
                            on_click_param="menu")

    form["lista_widgets"] = [
        form.get("btn_reanudar"),
        form.get("btn_menu")
    ]
    
    form["eventos"] = []

    var.dict_categorias_forms[form.get("nombre")] = form

    return form


def dibujar(dict_form_datos: dict):
    """
    Dibuja el formulario de pausa

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.dibujar(dict_form_datos)
    fbase.dibujar_widgets(dict_form_datos)


def actualizar(dict_form_datos: dict):
    """
    Actualiza el formulario de pausa

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.actualizar(dict_form_datos)