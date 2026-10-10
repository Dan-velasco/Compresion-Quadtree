
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
RESULTADOS = CARPETA / "resultados"

# Leer los experimentos realizados
datos = pd.read_csv(RESULTADOS / "experimentos.csv")

# Crear carpeta para las graficas
CARPETA_GRAFICAS = RESULTADOS / "graficas"
CARPETA_GRAFICAS.mkdir(exist_ok=True)

tipos = ["uniforme", "regiones", "detalles"]
tolerancias = [0, 20, 60]

# GRAFICA 1: TIEMPO DE CONSTRUCCION
plt.figure(figsize=(9, 5))

for tipo in tipos:
    filtro = datos[
        (datos["tipo"] == tipo) &
        (datos["tolerancia"] == 20)
    ].sort_values("ancho")

    plt.plot(
        filtro["ancho"],
        filtro["tiempo_segundos"],
        marker="o",
        label=tipo
    )

plt.title("Tiempo de construccion del Quadtree")
plt.xlabel("Tamano de imagen (N x N)")
plt.ylabel("Tiempo (segundos)")
plt.xticks([64, 128, 256])
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(CARPETA_GRAFICAS / "tiempos.png", dpi=200)
plt.close()

# GRAFICA 2: NUMERO DE NODOS
plt.figure(figsize=(9, 5))

for tipo in tipos:
    filtro = datos[
        (datos["tipo"] == tipo) &
        (datos["ancho"] == 128)
    ].sort_values("tolerancia")

    plt.plot(
        filtro["tolerancia"],
        filtro["nodos_totales"],
        marker="o",
        label=tipo
    )

plt.title("Tolerancia vs numero de nodos")
plt.xlabel("Tolerancia")
plt.ylabel("Nodos totales")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(CARPETA_GRAFICAS / "nodos.png", dpi=200)
plt.close()

# GRAFICA 3: RAZON DE COMPRESION
plt.figure(figsize=(9, 5))

for tipo in tipos:
    filtro = datos[
        (datos["tipo"] == tipo) &
        (datos["ancho"] == 128)
    ].sort_values("tolerancia")

    plt.plot(
        filtro["tolerancia"],
        filtro["razon_compresion"],
        marker="o",
        label=tipo
    )

plt.title("Tolerancia vs razon de compresion")
plt.xlabel("Tolerancia")
plt.ylabel("Razon de compresion")
plt.axhline(1, linestyle="--", label="Sin ahorro")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(CARPETA_GRAFICAS / "compresion.png", dpi=200)
plt.close()

# GRAFICA 4: ERROR DE RECONSTRUCCION
plt.figure(figsize=(9, 5))

for tipo in tipos:
    filtro = datos[
        (datos["tipo"] == tipo) &
        (datos["ancho"] == 128)
    ].sort_values("tolerancia")

    plt.plot(
        filtro["tolerancia"],
        filtro["mse"],
        marker="o",
        label=tipo
    )

plt.title("Tolerancia vs error MSE")
plt.xlabel("Tolerancia")
plt.ylabel("Error cuadratico medio")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(CARPETA_GRAFICAS / "mse.png", dpi=200)
plt.close()

print("GRAFICAS GENERADAS CORRECTAMENTE")
print("Ubicacion:", CARPETA_GRAFICAS)
