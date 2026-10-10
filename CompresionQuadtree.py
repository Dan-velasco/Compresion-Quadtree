
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
from time import perf_counter

from quadtree import (
    construir_quadtree,
    reconstruir,
    contar_nodos,
    profundidad_maxima
)

TAMANO = 128
TOLERANCIA = 20

CARPETA = Path(__file__).resolve().parent
RUTA = CARPETA / "imagenes" / "prueba.jpg"

if not RUTA.exists():
    raise FileNotFoundError(
        f"No se encontro la imagen: {RUTA}"
    )

original = Image.open(RUTA).convert("RGB")
original = original.resize(
    (TAMANO, TAMANO),
    Image.Resampling.LANCZOS
)

imagen = np.array(original)

inicio = perf_counter()

arbol = construir_quadtree(
    imagen, 0, 0, TAMANO, TAMANO, TOLERANCIA
)

tiempo = perf_counter() - inicio

resultado = np.zeros_like(imagen)
reconstruir(arbol, resultado)


nodos, hojas = contar_nodos(arbol)
profundidad = profundidad_maxima(arbol)

mse = np.mean(
    (imagen.astype(float) - resultado.astype(float)) ** 2
)

print("\nRESULTADOS DEL QUADTREE")
print("--------------------------------")
print("Imagen:", RUTA.name)
print("Tamano:", TAMANO, "x", TAMANO)
print("Tolerancia:", TOLERANCIA)
print("Tiempo:", round(tiempo, 6), "segundos")
print("Nodos totales:", nodos)
print("Nodos hoja:", hojas)
print("Profundidad maxima:", profundidad)
print("Error MSE:", round(mse, 4))

# CALCULAR ALMACENAMIENTO

# Una imagen RGB utiliza 24 bits por pixel
bits_original = TAMANO * TAMANO * 24

# Nodos internos
internos = nodos - hojas

# Formato teorico:
# 64 bits para dimensiones
# 1 bit por nodo interno
# 25 bits por nodo hoja (marca + RGB)
bits_arbol = 64 + internos + (hojas * 25)

# Redondear a bytes completos
bytes_original = bits_original // 8
bytes_arbol = (bits_arbol + 7) // 8

razon_compresion = bytes_original / bytes_arbol

ahorro = (1 - bytes_arbol / bytes_original) * 100

print("\nANALISIS DE COMPRESION")
print("--------------------------------")
print("Tamano original:", bytes_original, "bytes")
print("Tamano Quadtree:", bytes_arbol, "bytes")
print("Razon de compresion:", round(razon_compresion, 3))
print("Ahorro de almacenamiento:", round(ahorro, 2), "%")

SALIDA = CARPETA / "reconstruida.png"
Image.fromarray(resultado).save(SALIDA)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(imagen)
plt.title("Imagen original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(resultado)
plt.title(f"Quadtree - Tolerancia {TOLERANCIA}")
plt.axis("off")

plt.tight_layout()
plt.show()
