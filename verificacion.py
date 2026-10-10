
import numpy as np

from quadtree import (
    construir_quadtree,
    reconstruir,
    contar_nodos
)

dimensiones = [
    (63, 63),
    (65, 67),
    (127, 129),
    (1, 19),
    (19, 1)
]

rng = np.random.default_rng(42)

for alto, ancho in dimensiones:
    imagen = rng.integers(
        0, 256,
        size=(alto, ancho, 3),
        dtype=np.uint8
    )

    arbol = construir_quadtree(
        imagen, 0, 0, ancho, alto, 0
    )

    resultado = np.zeros_like(imagen)
    reconstruir(arbol, resultado)

    nodos, hojas = contar_nodos(arbol)

    correcta = np.array_equal(
        imagen, resultado
    )

    print(
        f"{ancho}x{alto} | "
        f"Nodos: {nodos} | "
        f"Hojas: {hojas} | "
        f"Reconstruccion exacta: {correcta}"
    )

    assert correcta, "ERROR EN LA RECONSTRUCCION"

print("\nTODAS LAS PRUEBAS SUPERADAS")
