import pygame as pg
import modules.variables as var
import modules.puntajes as puntajes_modulo
from modules.forms import(
    form_base as fbase,
)
from utn_fra.pygame_widgets import(
    Button
)

def crear_form_ranking(dict_for_data: dict) -> dict:
    """
    Crea el formulario de ranking

    Args:
        dict_for_data (dict): Datos del formulario

    Returns:
        dict: Diccionario con los datos del formulario
    """

    form = fbase.crear_form_base(dict_for_data)
    form["btn_volver"] = Button(x= var.PANTALLA[0] // 2, y=520,
                            text="VOLVER", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=25,
                            color= pg.Color("blue"), on_click=fbase.cambiar_pantalla,
                            on_click_param="menu")

    form["lista_widgets"] = [
        form.get("btn_volver")
    ]

    var.dict_categorias_forms[form.get("nombre")]  = form

    return form


def dibujar(dict_form_datos: dict):
    """
    Dibuja el formulario de ranking

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.dibujar(dict_form_datos)
    
    pantalla = dict_form_datos.get("pantalla")
    
    # Cargar y mostrar los puntajes
    puntajes = puntajes_modulo.cargar_puntajes()
    
    # Dibujar título
    fuente_titulo = pg.font.Font(var.FUENTE, 40)
    texto_titulo = fuente_titulo.render("RANKING", True, pg.Color("yellow"))
    pantalla.blit(texto_titulo, (var.PANTALLA[0] // 2 - texto_titulo.get_width() // 2, 20))
    
    # Dibujar encabezados
    fuente_header = pg.font.Font(var.FUENTE, 20)
    texto_pos = fuente_header.render("POS", True, pg.Color("white"))
    texto_nick = fuente_header.render("NICKNAME", True, pg.Color("white"))
    texto_pts = fuente_header.render("PUNTOS", True, pg.Color("white"))
    
    pantalla.blit(texto_pos, (50, 80))
    pantalla.blit(texto_nick, (150, 80))
    pantalla.blit(texto_pts, (500, 80))
    
    # Dibujar puntajes
    fuente_puntajes = pg.font.Font(var.FUENTE, 18)
    y_pos = 120
    
    if puntajes:
        for i, p in enumerate(puntajes[:10], 1):  # Mostrar top 10
            nickname = p.get("nickname", "Jugador")
            puntaje = p.get("puntaje", 0)
            
            texto_pos = fuente_puntajes.render(f"{i}", True, pg.Color("white"))
            texto_nick = fuente_puntajes.render(nickname, True, pg.Color("cyan"))
            texto_pts = fuente_puntajes.render(str(puntaje), True, pg.Color("lime"))
            
            pantalla.blit(texto_pos, (70, y_pos))
            pantalla.blit(texto_nick, (150, y_pos))
            pantalla.blit(texto_pts, (500, y_pos))
            
            y_pos += 35
    else:
        # Mensaje cuando no hay puntajes
        fuente_vacio = pg.font.Font(var.FUENTE, 25)
        texto_vacio = fuente_vacio.render("No hay puntajes aún", True, pg.Color("white"))
        pantalla.blit(texto_vacio, (var.PANTALLA[0] // 2 - texto_vacio.get_width() // 2, 250))
    
    fbase.dibujar_widgets(dict_form_datos)


def actualizar(dict_form_datos: dict):
    """
    Actualiza el formulario de ranking

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.actualizar(dict_form_datos)