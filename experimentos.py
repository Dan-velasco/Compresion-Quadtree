
import numpy as np
import pandas as pd
from pathlib import Path
from time import perf_counter

from quadtree import (
    construir_quadtree,
    reconstruir,
    contar_nodos,
    profundidad_maxima
)



CARPETA = Path(__file__).resolve().parent
SALIDA = CARPETA / "resultados"
SALIDA.mkdir(parents=True, exist_ok=True)

TAMANOS = [64, 128, 256]
TOLERANCIAS = [0, 20, 60]
TIPOS = ["uniforme", "regiones", "detalles"]

REPETICIONES = 5
SEMILLA = 42




def generar_imagen(tipo, n):

    imagen = np.zeros((n, n, 3), dtype=np.uint8)

    if tipo == "uniforme":
        imagen[:, :] = [80, 140, 200]

    elif tipo == "regiones":
        mitad = n // 2

        imagen[:mitad, :mitad] = [255, 0, 0]
        imagen[:mitad, mitad:] = [0, 255, 0]
        imagen[mitad:, :mitad] = [0, 0, 255]
        imagen[mitad:, mitad:] = [255, 255, 0]

    elif tipo == "detalles":
        rng = np.random.default_rng(SEMILLA)

        imagen = rng.integers(
            0,
            256,
            size=(n, n, 3),
            dtype=np.uint8
        )

    else:
        raise ValueError(
            f"Tipo de imagen desconocido: {tipo}"
        )

    return imagen




def calcular_metricas(imagen, reconstruida, arbol):

    alto, ancho = imagen.shape[:2]

    nodos, hojas = contar_nodos(arbol)
    profundidad = profundidad_maxima(arbol)

    diferencia = (
        imagen.astype(np.float64)
        - reconstruida.astype(np.float64)
    )

    mse = float(np.mean(diferencia ** 2))

   

    internos = nodos - hojas

    bits_original = ancho * alto * 24

    bits_quadtree = (
        64
        + internos
        + hojas * 25
    )

    bytes_original = bits_original // 8
    bytes_quadtree = (bits_quadtree + 7) // 8

    razon = bytes_original / bytes_quadtree

    ahorro = (
        1 - bytes_quadtree / bytes_original
    ) * 100

    return {
        "nodos_totales": nodos,
        "nodos_hoja": hojas,
        "nodos_internos": internos,
        "profundidad": profundidad,
        "bytes_original": bytes_original,
        "bytes_quadtree": bytes_quadtree,
        "razon_compresion": razon,
        "ahorro_porcentaje": ahorro,
        "mse": mse
    }




def experimentar():

    registros = []

    total_configuraciones = (
        len(TIPOS)
        * len(TAMANOS)
        * len(TOLERANCIAS)
    )

    print("=" * 55)
    print("EXPERIMENTOS DE COMPRESION QUADTREE")
    print("=" * 55)

    print("Configuraciones:", total_configuraciones)
    print("Repeticiones por configuracion:", REPETICIONES)
    print(
        "Total de construcciones:",
        total_configuraciones * REPETICIONES
    )

    contador = 0

    for tipo in TIPOS:

        for n in TAMANOS:

            
            imagen = generar_imagen(tipo, n)

            for tolerancia in TOLERANCIAS:

                contador += 1

                tiempos = []

               
                for repeticion in range(REPETICIONES):

                    inicio = perf_counter()

                    arbol = construir_quadtree(
                        imagen,
                        0,
                        0,
                        n,
                        n,
                        tolerancia
                    )

                    duracion = perf_counter() - inicio

                    tiempos.append(duracion)

               
                tiempo_promedio = float(
                    np.mean(tiempos)
                )

                tiempo_mediana = float(
                    np.median(tiempos)
                )

                desviacion = float(
                    np.std(tiempos, ddof=1)
                )

                
                reconstruida = np.zeros_like(imagen)

                reconstruir(
                    arbol,
                    reconstruida
                )

              
                metricas = calcular_metricas(
                    imagen,
                    reconstruida,
                    arbol
                )

                registro = {
                    "tipo": tipo,
                    "ancho": n,
                    "alto": n,
                    "tolerancia": tolerancia,
                    "repeticiones": REPETICIONES,
                    "tiempo_segundos": tiempo_promedio,
                    "tiempo_mediana": tiempo_mediana,
                    "desviacion_tiempo": desviacion,
                    **metricas
                }

                registros.append(registro)

                
                print(
                    f"[{contador}/{total_configuraciones}] "
                    f"{tipo} | "
                    f"{n}x{n} | "
                    f"T={tolerancia} | "
                    f"Tiempo={tiempo_promedio:.6f}s | "
                    f"Nodos={metricas['nodos_totales']} | "
                    f"MSE={metricas['mse']:.4f} | "
                    f"Compresion="
                    f"{metricas['razon_compresion']:.3f}:1"
                )

   

    tabla = pd.DataFrame(registros)

    archivo_csv = SALIDA / "experimentos.csv"

    tabla.to_csv(
        archivo_csv,
        index=False,
        encoding="utf-8-sig"
    )

   
    print("\n" + "=" * 55)
    print("EXPERIMENTOS TERMINADOS")
    print("=" * 55)

    print("Configuraciones:", len(tabla))

    print(
        "Construcciones realizadas:",
        len(tabla) * REPETICIONES
    )

    print("CSV guardado en:")
    print(archivo_csv)

    print("\nPROCESO COMPLETADO CORRECTAMENTE")




if __name__ == "__main__":
    experimentar()
