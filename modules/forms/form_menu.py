import pygame as pg
import modules.variables as var
from modules.forms import(
    form_base as fbase,
    form_controlador as fcontrol
)
from utn_fra.pygame_widgets import(
    Button
)

def crear_form_menu(dict_for_data: dict) -> dict:
    """


    Args:
        dict_for_data (dict): _description_

    Returns:
        dict: _description_
    """

    form = fbase.crear_form_base(dict_for_data)
    form["btn_jugar"] = Button(x= var.PANTALLA[0] // 2, y=220,
                            text="JUGAR", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click=fbase.cambiar_pantalla,
                            on_click_param= "app")
    
    form["btn_ranking"] = Button(x= var.PANTALLA[0] // 2, y=320,
                            text="RANKING", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click=fbase.cambiar_pantalla,
                            on_click_param= "ranking")
    
    form["btn_opciones"] = Button(x= var.PANTALLA[0] // 2, y=420,
                            text="OPCIONES", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click=fbase.cambiar_pantalla,
                            on_click_param= "opciones")
    
    form["btn_salir"] = Button(x= var.PANTALLA[0] // 2, y=520,
                            text="SALIR", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click=fcontrol.cerrar_juego,
                            on_click_param=None)

    form["lista_widgets"] = [
        form.get("btn_jugar"),
        form.get("btn_ranking"),
        form.get("btn_opciones"),
        form.get("btn_salir")
    ]

    var.dict_categorias_forms[form.get("nombre")]  = form

    return form



def dibujar(dict_form_datos: dict):
    """_summary_

    Args:
        dict_form_datos (dict): _description_
    """

    fbase.dibujar(dict_form_datos)
    fbase.dibujar_widgets(dict_form_datos)


def actualizar(dict_form_datos: dict):
    """

    Args:
        dict_form_datos (dict): _description_
    """

    fbase.actualizar(dict_form_datos)