import pygame.mixer as mx

config_musica = {
    "ruta_musica": ""
}

def configurar_ruta_music(ruta_musica: str):
    """_summary_

    Args:
        ruta_musica (str): _description_
    """

    config_musica["ruta_musica"] = ruta_musica


def play_music():
    """_summary_
    """
    if config_musica.get("ruta_musica"):
        mx.music.load(config_musica.get("ruta_musica"))
        mx.music.set_volume(0.3)
        mx.music.play(-1,0,2500)


def stop_music():
    """_summary_
    """

    if config_musica.get("ruta_musica"):
        mx.music.stop()


def cambiar_volumen(volumen: float):
    """
    Cambia el volumen de la música
    
    Args:
        volumen (float): Volumen entre 0.0 y 1.0
    """
    mx.music.set_volume(volumen)