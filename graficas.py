from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DESTINO = BASE / "resultados" / "graficas"
DESTINO.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(BASE / "resultados" / "experimentos.csv")

configuraciones = [
    ("tiempos.png", "ancho", "tiempo_segundos", "Tamaño (lado en píxeles)", "Tiempo medio (s)", 20, None),
    ("nodos.png", "tolerancia", "nodos_totales", "Tolerancia", "Total de nodos", None, 128),
    ("compresion.png", "tolerancia", "razon_compresion", "Tolerancia", "Razón RGB / Quadtree", None, 128),
    ("mse.png", "tolerancia", "mse", "Tolerancia", "MSE", None, 128)
]

for nombre, eje_x, eje_y, etiqueta_x, etiqueta_y, tol, lado in configuraciones:
    fig, ax = plt.subplots(figsize=(8, 5))
    for tipo in ["uniforme", "regiones", "detalles"]:
        seleccion = df[df["tipo"] == tipo]
        if tol is not None:
            seleccion = seleccion[seleccion["tolerancia"] == tol]
        if lado is not None:
            seleccion = seleccion[seleccion["ancho"] == lado]
        seleccion = seleccion.sort_values(eje_x)
        ax.plot(seleccion[eje_x], seleccion[eje_y], marker="o", label=tipo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    ax.set_title(nombre.replace(".png", "").capitalize())
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(DESTINO / nombre, dpi=200)
    plt.close(fig)
print("Cuatro gráficas guardadas en", DESTINO)
