import pygame as pg
import modules.variables as var
import modules.forms.form_base as fbase
from utn_fra.pygame_widgets import(
    Button
)


def crear_form_inicio(dict_for_data: dict) -> dict:
    """
    Crea el controlador del formulario de inicio

    Args:
        dict_for_data (dict): El diccionario de datos

    Returns:
        dict: Devuelve un controlador de formularios de inicio con los datos ingresados
    """

    form = fbase.crear_form_base(dict_for_data)
    form["btn_start"] = Button(x= var.PANTALLA[0] // 2, y=320,
                            text="START", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click= fbase.cambiar_pantalla,
                            on_click_param= "menu")


    form["lista_widgets"] = [
        form.get("btn_start")
    ]

    var.dict_categorias_forms[form.get("nombre")] = form

    return form


def dibujar(dict_form_datos: dict):
    """
    Dibuja el formulario de menú

    Args:
        dict_form (dict): El diccionario del formulario
    """

    fbase.dibujar(dict_form_datos)
    fbase.dibujar_widgets(dict_form_datos)


def actualizar(dict_form: dict):
    """
    Actualiza el formulario de menú

    Args:
        dict_form (dict): El diccionario del formulario
    """

    fbase.actualizar(dict_form)