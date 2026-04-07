import json
import os

ARCHIVO_PUNTAJES = "puntajes.json"

def cargar_puntajes():
    """
    Carga los puntajes desde el archivo JSON
    
    Returns:
        list: Lista de puntajes ordenada descendentemente
    """
    if os.path.exists(ARCHIVO_PUNTAJES):
        try:
            with open(ARCHIVO_PUNTAJES, 'r') as archivo:
                puntajes = json.load(archivo)
                # Ordenar por puntaje descendente
                puntajes.sort(key=lambda x: x.get("puntaje", 0), reverse=True)
                return puntajes
        except:
            return []
    return []

def guardar_puntaje(nickname: str, puntaje: int):
    """
    Guarda un puntaje con su nickname
    
    Args:
        nickname (str): Nombre del jugador
        puntaje (int): Puntaje obtenido
    """
    puntajes = cargar_puntajes()
    
    # Agregar el nuevo puntaje
    puntajes.append({
        "nickname": nickname,
        "puntaje": puntaje
    })
    
    # Ordenar descendentemente por puntaje
    puntajes.sort(key=lambda x: x.get("puntaje", 0), reverse=True)
    
    # Guardar en el archivo
    with open(ARCHIVO_PUNTAJES, 'w') as archivo:
        json.dump(puntajes, archivo, indent=2)

def obtener_top_puntajes(limite: int = 10):
    """
    Obtiene los mejores puntajes
    
    Args:
        limite (int): Cantidad de puntajes a retornar
    
    Returns:
        list: Lista de los mejores puntajes
    """
    puntajes = cargar_puntajes()
    return puntajes[:limite]
