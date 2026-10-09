import numpy as np
import pandas as pd
from pathlib import Path
from time import perf_counter
from quadtree import construir_quadtree, reconstruir, contar_nodos, profundidad_maxima

BASE = Path(__file__).resolve().parent
RESULTADOS = BASE / "resultados"
TAMANOS = [64, 128, 256]
TOLERANCIAS = [0, 20, 60]
TIPOS = ["uniforme", "regiones", "detalles"]
REPETICIONES = 5
SEMILLA = 42


def generar_imagen(tipo, n):
    imagen = np.zeros((n, n, 3), dtype=np.uint8)
    if tipo == "uniforme":
        imagen[:] = [80, 140, 200]
    elif tipo == "regiones":
        mitad = n // 2
        imagen[:mitad, :mitad] = [255, 0, 0]
        imagen[:mitad, mitad:] = [0, 255, 0]
        imagen[mitad:, :mitad] = [0, 0, 255]
        imagen[mitad:, mitad:] = [255, 255, 0]
    elif tipo == "detalles":
        imagen = np.random.default_rng(SEMILLA).integers(0, 256, size=(n, n, 3), dtype=np.uint8)
    else:
        raise ValueError(f"Tipo no reconocido: {tipo}")
    return imagen


def experimentar():
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    filas = []
    for tipo in TIPOS:
        for n in TAMANOS:
            imagen = generar_imagen(tipo, n)
            for tolerancia in TOLERANCIAS:
                tiempos = []
                for _ in range(REPETICIONES):
                    inicio = perf_counter()
                    arbol = construir_quadtree(imagen, 0, 0, n, n, tolerancia)
                    tiempos.append(perf_counter() - inicio)
                reconstruida = np.zeros_like(imagen)
                reconstruir(arbol, reconstruida)
                nodos, hojas = contar_nodos(arbol)
                internos = nodos - hojas
                bits_arbol = 64 + internos + hojas * 25
                bytes_arbol = (bits_arbol + 7) // 8
                bytes_original = n*n*3
                error = imagen.astype(float) - reconstruida.astype(float)
                filas.append({
                    "tipo":tipo,"ancho":n,"alto":n,"tolerancia":tolerancia,
                    "repeticiones":REPETICIONES,"tiempo_segundos":float(np.mean(tiempos)),
                    "tiempo_mediana":float(np.median(tiempos)),
                    "desviacion_tiempo":float(np.std(tiempos, ddof=1)),
                    "nodos_totales":nodos,"nodos_hoja":hojas,"nodos_internos":internos,
                    "profundidad":profundidad_maxima(arbol),
                    "bytes_original":bytes_original,"bytes_quadtree":bytes_arbol,
                    "razon_compresion":bytes_original/bytes_arbol,
                    "ahorro_porcentaje":100*(1-bytes_arbol/bytes_original),
                    "mse":float(np.mean(error**2))
                })
                print(f"{tipo} {n}x{n} T={tolerancia}: {nodos} nodos")
    salida = RESULTADOS / "experimentos.csv"
    pd.DataFrame(filas).to_csv(salida,index=False,encoding="utf-8-sig")
    print(f"27 configuraciones, 135 construcciones. CSV: {salida}")

if __name__ == "__main__":
    experimentar()
