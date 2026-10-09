from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from experimentos import generar_imagen
from quadtree import construir_quadtree, reconstruir, contar_nodos, profundidad_maxima

DESTINO = Path(__file__).resolve().parent / "resultados" / "evidencias"
DESTINO.mkdir(parents=True, exist_ok=True)
for tipo, n, tolerancia in [("uniforme",128,0),("regiones",128,20),("detalles",128,60)]:
    original = generar_imagen(tipo,n)
    arbol = construir_quadtree(original,0,0,n,n,tolerancia)
    restaurada = np.zeros_like(original)
    reconstruir(arbol,restaurada)
    nodos, hojas = contar_nodos(arbol)
    internos = nodos-hojas
    bytes_quadtree = (64 + internos + hojas*25 + 7)//8
    razon = (n*n*3)/bytes_quadtree
    mse = float(np.mean((original.astype(float)-restaurada.astype(float))**2))
    fig, axs = plt.subplots(1,2,figsize=(9,5))
    for ax, image, label in zip(axs,[original,restaurada],["Original","Reconstruida"]):
        ax.imshow(image)
        ax.set_title(label)
        ax.axis("off")
    fig.suptitle(f"{tipo} | {n}x{n} | T={tolerancia} | Nodos={nodos} | Hojas={hojas} | Prof={profundidad_maxima(arbol)}\nMSE={mse:.4f} | Compresión teórica={razon:.3f}:1")
    fig.tight_layout(rect=(0,0,1,.88))
    fig.savefig(DESTINO/f"{tipo}_T{tolerancia}.png",dpi=160)
    plt.close(fig)
print("Tres evidencias en",DESTINO)
