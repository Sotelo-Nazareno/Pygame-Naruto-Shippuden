import pygame as pg
import modules.forms.form_controlador as fcontrol
import modules.variables as var
import random as rd
from .variables import(
    PANTALLA, TITULO, FPS, VOL_MUSICA
)


def run_game():
    """
    Ejecuta el juego
    """

    pg.mixer.pre_init(44100, -16, 2, 512)
    pg.init()

    pg.display.set_caption(TITULO)
    pantalla_principal = pg.display.set_mode(PANTALLA, pg.RESIZABLE)


    corriendo = True
    reloj = pg.time.Clock()

    datos_juego = {
        'points': 0,
        'cantidad_vidas': 3,
        'player': {},
        'config_musica':{
            "volumen_musica": VOL_MUSICA,
            "musica_encendida": True,
            "musica_inicializada" : False
        }
    }

    control_form = fcontrol.crear_form_controlador(pantalla_principal, datos_juego)
    


    #pg.time.set_timer(GENERAR_ENEMIGO, 500)
    while corriendo:
        reloj.tick(FPS)
        eventos = pg.event.get()

        for event in eventos:
            if event.type == pg.QUIT:
                corriendo = False
            
            # Capturar evento de redimensionamiento de ventana
            if event.type == pg.VIDEORESIZE:
                pantalla_principal = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                var.PANTALLA = (event.w, event.h)
                control_form["pantalla"] = pantalla_principal
                # Re-escalar los fondos de todos los formularios
                for form in var.dict_categorias_forms.values():
                    form["pantalla"] = pantalla_principal
                    fcontrol.redimensionar_surfaces(form)

            #reajustar_pantalla(control_form, event)

        # Pasar eventos al controlador
        control_form["eventos"] = eventos
        fcontrol.actualizar_forms(control_form)
        pg.display.flip()

    fcontrol.cerrar_juego()
