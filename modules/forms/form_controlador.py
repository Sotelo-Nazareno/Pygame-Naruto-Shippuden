import pygame as pg
import modules.variables as var
import sys
from modules.forms import(
    form_inicio as finicio,
    form_menu as fmenu,
    form_aplicacion as fapp,
    form_ranking as franking,
    form_opciones as fopciones,
    form_pausa as fpausa,
    form_resultado as fresultado,
    form_base as fbase
)

def crear_form_controlador(screen: pg.Surface, datos_juego: dict) -> dict:
    """
    Crea el controlador de un formulario

    Args:
        dict_for_data (dict): El diccionario de datos

    Returns:
        dict: Devuelve un controlador de formularios con los datos ingresados
    """

    controlador = {}

    controlador["pantalla_principal"] = screen
    controlador["juego_iniciado"] = False
    controlador["enemigo"] = None
    controlador["jugador"] = datos_juego.get("jugador")
    controlador["config_musica"] = datos_juego.get("config_musica")
    controlador["img_cursor"] = pg.image.load(var.RUTA_POINTER).convert_alpha()
    controlador["img_cursor"] = pg.transform.scale(controlador["img_cursor"], (40, 40))

    # Ocultar el cursor del sistema para usar el personalizado
    pg.mouse.set_visible(False)

    controlador["lista_forms"] = [
        finicio.crear_form_inicio(
            {
                "nombre": "inicio",
                "pantalla": controlador.get("pantalla_principal"),
                "activo": True,
                "coords": (0, 0),
                "fondo_pantalla": var.PANTALLA_INICIO,
                "dimensiones": var.PANTALLA,
            }
        ),
        fmenu.crear_form_menu(
            {
                "nombre": "menu",
                "pantalla": controlador.get("pantalla_principal"),
                "activo": False,
                "coords": (0, 0),
                "fondo_pantalla": var.PANTALLA_MENU,
                "dimensiones": var.PANTALLA,
                "ruta_musica" : var.MUSICA_MENU,
                "config_musica" : controlador.get("config_musica")
            }
        ),
        fapp.crear_form_app(
            {
                "nombre": "app",
                "pantalla": controlador.get("pantalla_principal"),
                "activo": False,
                "coords": (0, 0),
                "fondo_pantalla": var.PANTALLA_JUEGO,
                "dimensiones": var.PANTALLA,
                "ruta_musica" : var.MUSICA_JUEGO,
                "config_musica" : controlador.get("config_musica")
            }
        ),
        franking.crear_form_ranking(
            {
                "nombre": "ranking",
                "pantalla": controlador.get("pantalla_principal"),
                "activo": False,
                "coords": (0, 0),
                "fondo_pantalla": var.PANTALLA_RANKING,
                "dimensiones": var.PANTALLA,
                "ruta_musica" : var.MUSICA_RANKING,
                "config_musica" : controlador.get("config_musica")
            }
        ),
        fopciones.crear_form_opciones(
            {
                "nombre": "opciones",
                "pantalla": controlador.get("pantalla_principal"),
                "activo": False,
                "coords": (0, 0),
                "fondo_pantalla": var.PANTALLA_OPCIONES,
                "dimensiones": var.PANTALLA,
                "ruta_musica" : var.MUSICA_OPCIONES,
                "config_musica" : controlador.get("config_musica")
            }
        ),
        fpausa.crear_form_pausa(
            {
                "nombre": "pausa",
                "pantalla": controlador.get("pantalla_principal"),
                "activo": False,
                "coords": (0, 0),
                "fondo_pantalla": var.PANTALLA_JUEGO,  # Usar el mismo fondo que el juego
                "dimensiones": var.PANTALLA,
                "ruta_musica" : var.MUSICA_JUEGO,
                "config_musica" : controlador.get("config_musica")
            }
        ),
        fresultado.crear_form_resultado(
            {
                "nombre": "resultado",
                "pantalla": controlador.get("pantalla_principal"),
                "activo": False,
                "coords": (0, 0),
                "fondo_pantalla": var.PANTALLA_JUEGO,
                "dimensiones": var.PANTALLA,
                "ruta_musica" : var.MUSICA_JUEGO,
                "config_musica" : controlador.get("config_musica")
            }
        )
    ]
    
    # Inicializar eventos vacío
    controlador["eventos"] = []

    return controlador


def actualizar_forms(form_controlador: dict):
    """
    Actualiza el controlador de formularios

    Args:
        controller_form (dict): Diccionario con los datos del controlador de formularios
    """

    lista_formularios = form_controlador.get("lista_forms")
    
    # Pasar eventos a todos los formularios
    eventos = form_controlador.get("eventos", [])
    for form in lista_formularios:
        form["eventos"] = eventos

    if lista_formularios[0].get("activo"):
        finicio.actualizar(lista_formularios[0])
        finicio.dibujar(lista_formularios[0])
    elif lista_formularios[1].get("activo"):
        fmenu.actualizar(lista_formularios[1])
        fmenu.dibujar(lista_formularios[1])
    elif lista_formularios[2].get("activo"):
        fapp.actualizar(lista_formularios[2])
        fapp.dibujar(lista_formularios[2])
    elif lista_formularios[3].get("activo"):
        franking.actualizar(lista_formularios[3])
        franking.dibujar(lista_formularios[3])
    elif lista_formularios[4].get("activo"):
        fopciones.actualizar(lista_formularios[4])
        fopciones.dibujar(lista_formularios[4])
    elif lista_formularios[5].get("activo"):
        fpausa.actualizar(lista_formularios[5])
        fpausa.dibujar(lista_formularios[5])
    elif lista_formularios[6].get("activo"):
        fresultado.actualizar(lista_formularios[6])
        fresultado.dibujar(lista_formularios[6])

    # Dibujar el cursor personalizado centrado en la posición del mouse
    pos = pg.mouse.get_pos()
    cursor_pos = (pos[0] - 40 // 2, pos[1] - 40 // 2)
    form_controlador["pantalla_principal"].blit(form_controlador["img_cursor"], cursor_pos)




def actualizar(form_controlador: dict):
    """
    Actualiza el controlador de formularios

    Args:
        controller_form (dict): Diccionario con los datos del controlador de formularios
    """

    actualizar_forms(form_controlador)


def cerrar_juego(param=None):
    """
    Cierra el juego
    """
    
    print("Cerrando el juego..")
    pg.quit()
    sys.exit()


def redimensionar_surfaces(form):
    """
    Re-escala la superficie de un formulario cuando se redimensiona la ventana

    Args:
        form (dict): Diccionario con los datos del formulario
    """
    fbase.redimensionar_superficie(form)