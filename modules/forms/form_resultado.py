import pygame as pg
import modules.variables as var
import modules.puntajes as puntajes_modulo
from modules.forms import(
    form_base as fbase
)
from utn_fra.pygame_widgets import(
    Button
)

def callback_guardar(dict_form_datos: dict, param=None):
    """Callback para el botón guardar"""
    # Guardar el puntaje cuando se presiona el botón
    guardar_puntaje(dict_form_datos)

def crear_form_resultado(dict_for_data: dict) -> dict:
    """
    Crea el formulario de resultado final del juego

    Args:
        dict_for_data (dict): Datos del formulario

    Returns:
        dict: Diccionario con los datos del formulario
    """

    form = fbase.crear_form_base(dict_for_data)
    
    form["btn_guardar"] = Button(x= var.PANTALLA[0] // 2, y=350,
                            text="GUARDAR PUNTAJE", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=20,
                            color= pg.Color("green"), on_click=callback_guardar,
                            on_click_param=form)
    
    form["btn_jugar_nuevamente"] = Button(x= var.PANTALLA[0] // 2, y=450,
                            text="JUGAR NUEVAMENTE", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=20,
                            color= pg.Color("blue"), on_click=fbase.cambiar_pantalla,
                            on_click_param="app")
    
    form["btn_menu"] = Button(x= var.PANTALLA[0] // 2, y=520,
                            text="MENU PRINCIPAL", screen=form.get("pantalla"),
                            font_path=var.FUENTE, font_size=20,
                            color= pg.Color("red"), on_click=fbase.cambiar_pantalla,
                            on_click_param="menu")

    form["lista_widgets"] = [
        form.get("btn_guardar"),
        form.get("btn_jugar_nuevamente"),
        form.get("btn_menu")
    ]
    
    form["puntaje_final"] = 0
    form["nickname"] = ""
    form["cursor_visible"] = True
    form["tiempo_cursor"] = 0
    form["puntaje_guardado"] = False
    form["eventos"] = []

    var.dict_categorias_forms[form.get("nombre")] = form

    return form


def dibujar_campo_nickname(dict_form_datos: dict):
    """
    Dibuja el campo para ingresar el nickname
    
    Args:
        dict_form_datos (dict): Datos del formulario
    """
    try:
        pantalla = dict_form_datos.get("pantalla")
        fuente = pg.font.SysFont("arial", 25)
        
        # Dibujar etiqueta
        texto_label = fuente.render("Nickname:", True, pg.Color("white"))
        pantalla.blit(texto_label, (var.PANTALLA[0] // 2 - 200, 270))
        
        # Dibujar caja del input
        rect_input = pg.Rect(var.PANTALLA[0] // 2 - 50, 265, 300, 40)
        pg.draw.rect(pantalla, pg.Color("white"), rect_input, 2)
        
        # Dibujar el nickname ingresado
        nickname = dict_form_datos.get("nickname", "")
        texto_nick = fuente.render(nickname, True, pg.Color("yellow"))
        pantalla.blit(texto_nick, (var.PANTALLA[0] // 2 - 30, 275))
        
        # Dibujar cursor parpadeante
        if dict_form_datos.get("cursor_visible"):
            cursor_x = var.PANTALLA[0] // 2 - 30 + texto_nick.get_width() + 5
            pg.draw.line(pantalla, pg.Color("yellow"), (cursor_x, 270), (cursor_x, 305), 2)
        
        dict_form_datos["entrada_rect"] = rect_input
    except Exception as e:
        print(f"ERROR en dibujar_campo_nickname: {e}")


def dibujar(dict_form_datos: dict):
    """
    Dibuja el formulario de resultado

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    fbase.dibujar(dict_form_datos)
    
    # Dibujar el puntaje final
    pantalla = dict_form_datos.get("pantalla")
    fuente_grande = pg.font.Font(var.FUENTE, 50)
    fuente_pequenia = pg.font.Font(var.FUENTE, 30)
    
    texto_fin = fuente_grande.render("¡TIEMPO TERMINADO!", True, pg.Color("red"))
    texto_puntaje = fuente_pequenia.render(f"Puntaje Final: {dict_form_datos.get('puntaje_final')}", True, pg.Color("white"))
    
    pantalla.blit(texto_fin, (var.PANTALLA[0] // 2 - texto_fin.get_width() // 2, 100))
    pantalla.blit(texto_puntaje, (var.PANTALLA[0] // 2 - texto_puntaje.get_width() // 2, 180))
    
    # Configurar visibilidad de botones
    if not dict_form_datos.get("puntaje_guardado"):
        # Mostrar botones de guardar y jugar nuevamente
        dict_form_datos["btn_guardar"].visibles = True
        dict_form_datos["btn_jugar_nuevamente"].visibles = True
        dict_form_datos["btn_menu"].visibles = False
    else:
        # Mostrar botones de jugar nuevamente y menu
        dict_form_datos["btn_guardar"].visibles = False
        dict_form_datos["btn_jugar_nuevamente"].visibles = True
        dict_form_datos["btn_menu"].visibles = True
    
    # Dibujar widgets (botones) primero
    fbase.dibujar_widgets(dict_form_datos)
    
    # Dibujar campo de nickname DESPUÉS de los botones para que aparezca encima
    if not dict_form_datos.get("puntaje_guardado"):
        dibujar_campo_nickname(dict_form_datos)
    else:
        # Mostrar mensaje de puntaje guardado
        texto_guardado = fuente_pequenia.render("¡Puntaje guardado!", True, pg.Color("green"))
        pantalla.blit(texto_guardado, (var.PANTALLA[0] // 2 - texto_guardado.get_width() // 2, 300))


def actualizar(dict_form_datos: dict):
    """
    Actualiza el formulario de resultado

    Args:
        dict_form_datos (dict): Datos del formulario
    """

    # Parpadeo del cursor
    dict_form_datos["tiempo_cursor"] += 1
    if dict_form_datos["tiempo_cursor"] >= 30:
        dict_form_datos["cursor_visible"] = not dict_form_datos.get("cursor_visible", True)
        dict_form_datos["tiempo_cursor"] = 0
    
    # Manejar entrada de texto si aún no se ha guardado
    if not dict_form_datos.get("puntaje_guardado"):
        # Obtener eventos del diccionario (pasados desde juego.py)
        eventos = dict_form_datos.get("eventos", [])
        
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    dict_form_datos["nickname"] = dict_form_datos.get("nickname", "")[:-1]
                elif event.key == pg.K_RETURN:
                    # Guardar el puntaje al presionar Enter
                    if dict_form_datos.get("nickname", "").strip():
                        guardar_puntaje(dict_form_datos)
                    else:
                        dict_form_datos["nickname"] = "Jugador"
                        guardar_puntaje(dict_form_datos)
                elif len(dict_form_datos.get("nickname", "")) < 15:
                    if event.unicode and event.unicode.isprintable():
                        dict_form_datos["nickname"] += event.unicode
        
        # Actualizar widgets (botones)
        for widget in dict_form_datos.get("lista_widgets", []):
            if hasattr(widget, "update"):
                widget.update()
    else:
        # Si puntaje fue guardado, procesar widgets normalmente
        fbase.actualizar(dict_form_datos)


def guardar_puntaje(dict_form_datos: dict):
    """
    Guarda el puntaje con el nickname ingresado
    
    Args:
        dict_form_datos (dict): Datos del formulario
    """
    nickname = dict_form_datos.get("nickname", "Jugador")
    if not nickname.strip():
        nickname = "Jugador"
    
    puntaje = dict_form_datos.get("puntaje_final", 0)
    puntajes_modulo.guardar_puntaje(nickname, puntaje)
    
    dict_form_datos["puntaje_guardado"] = True
