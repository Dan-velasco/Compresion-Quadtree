
import numpy as np


class NodoQuadtree:
    def __init__(self, x, y, ancho, alto, color=None, hijos=None):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.hijos = hijos if hijos is not None else []

    def es_hoja(self):
        return len(self.hijos) == 0


def construir_quadtree(imagen, x, y, ancho, alto, tolerancia):
    # Extraemos la region que vamos a analizar
    region = imagen[y:y + alto, x:x + ancho]

    # Calculamos el color promedio de la region
    promedio = np.mean(region, axis=(0, 1))

    # Medimos la mayor diferencia respecto al promedio
    diferencia = np.max(np.abs(region.astype(float) - promedio))

    # Si la region es suficientemente uniforme,
    # se representa con un solo nodo hoja
    if diferencia <= tolerancia or (ancho == 1 and alto == 1):
        color = np.rint(promedio).astype(np.uint8)
        return NodoQuadtree(
            x, y, ancho, alto, color=color
        )

    # Dividir en regiones sin perder pixeles
    mitad_ancho = ancho // 2
    mitad_alto = alto // 2

    rangos_x = [(x, mitad_ancho), (x + mitad_ancho, ancho - mitad_ancho)]
    rangos_y = [(y, mitad_alto), (y + mitad_alto, alto - mitad_alto)]

    hijos = []

    for inicio_y, h in rangos_y:
        for inicio_x, w in rangos_x:
            if w > 0 and h > 0:
                hijo = construir_quadtree(
                    imagen, inicio_x, inicio_y, w, h, tolerancia
                )
                hijos.append(hijo)

    return NodoQuadtree(x, y, ancho, alto, hijos=hijos)


def reconstruir(nodo, imagen):
    if nodo.es_hoja():
        imagen[
            nodo.y:nodo.y + nodo.alto,
            nodo.x:nodo.x + nodo.ancho
        ] = nodo.color
    else:
        for hijo in nodo.hijos:
            reconstruir(hijo, imagen)


def contar_nodos(nodo):
    total = 1
    hojas = 1 if nodo.es_hoja() else 0

    for hijo in nodo.hijos:
        n, h = contar_nodos(hijo)
        total += n
        hojas += h

    return total, hojas


def profundidad_maxima(nodo):
    if nodo.es_hoja():
        return 0

    return 1 + max(profundidad_maxima(h) for h in nodo.hijos)
