
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from experimentos import generar_imagen
from quadtree import (
    construir_quadtree,
    reconstruir,
    contar_nodos,
    profundidad_maxima
)

CARPETA = Path(__file__).resolve().parent
SALIDA = CARPETA / "resultados" / "evidencias"
SALIDA.mkdir(parents=True, exist_ok=True)

# Tres ejemplos representativos
CASOS = [
    ("uniforme", 128, 0),
    ("regiones", 128, 20),
    ("detalles", 128, 60)
]

for tipo, n, tolerancia in CASOS:

    original = generar_imagen(tipo, n)

    arbol = construir_quadtree(
        original, 0, 0, n, n, tolerancia
    )

    reconstruida = np.zeros_like(original)
    reconstruir(arbol, reconstruida)

    nodos, hojas = contar_nodos(arbol)
    profundidad = profundidad_maxima(arbol)

    mse = np.mean(
        (original.astype(float) -
         reconstruida.astype(float)) ** 2
    )

    internos = nodos - hojas
    bytes_original = n * n * 3
    bits_arbol = 64 + internos + hojas * 25
    bytes_arbol = (bits_arbol + 7) // 8
    razon = bytes_original / bytes_arbol

    fig, ejes = plt.subplots(1, 2, figsize=(10, 5))

    ejes[0].imshow(original)
    ejes[0].set_title("Original")
    ejes[0].axis("off")

    ejes[1].imshow(reconstruida)
    ejes[1].set_title("Reconstruida")
    ejes[1].axis("off")

    fig.suptitle(
        f"Tipo: {tipo} | Tamano: {n}x{n} | "
        f"Tolerancia: {tolerancia}\n"
        f"Nodos: {nodos} | Hojas: {hojas} | "
        f"Profundidad: {profundidad}\n"
        f"MSE: {mse:.4f} | "
        f"Compresion: {razon:.3f}:1"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.83])

    archivo = SALIDA / f"{tipo}_T{tolerancia}.png"
    fig.savefig(archivo, dpi=200)
    plt.close(fig)

    print("Evidencia generada:", archivo.name)

print("\nLAS 3 EVIDENCIAS SE GENERARON CORRECTAMENTE")
