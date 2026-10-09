from pathlib import Path
import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from quadtree import construir_quadtree, reconstruir, contar_nodos, profundidad_maxima

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Reconstrucción RGB por Quadtree")
parser.add_argument("--imagen",default=str(BASE / "imagenes" / "prueba.jpg"))
parser.add_argument("--tamano",type=int,default=128)
parser.add_argument("--tolerancia",type=float,default=20)
args = parser.parse_args()
if args.tamano < 1 or args.tolerancia < 0:
    parser.error("Tamaño positivo y tolerancia no negativa")
ruta = Path(args.imagen)
if not ruta.is_file():
    parser.error(f"No se encontró {ruta}; añade tu propia imagen o usa --imagen RUTA")
with Image.open(ruta) as img:
    original = np.asarray(img.convert("RGB").resize((args.tamano,args.tamano),Image.Resampling.LANCZOS))
quadtree = construir_quadtree(original,0,0,args.tamano,args.tamano,args.tolerancia)
recon = np.zeros_like(original)
reconstruir(quadtree,recon)
nodos,hojas = contar_nodos(quadtree)
bytes_rgb = args.tamano*args.tamano*3
bytes_tree = (64+(nodos-hojas)+25*hojas+7)//8
mse = np.mean((original.astype(float)-recon.astype(float))**2)
salida = BASE / "resultados" / "reconstruida.png"
salida.parent.mkdir(parents=True,exist_ok=True)
Image.fromarray(recon).save(salida)
print(f"Nodos={nodos}, hojas={hojas}, profundidad={profundidad_maxima(quadtree)}, MSE={mse:.4f}")
print(f"Bytes RGB={bytes_rgb}, estimado Quadtree={bytes_tree}, razón={bytes_rgb/bytes_tree:.3f}:1")
print("Imagen reconstruida:",salida)
fig,axs=plt.subplots(1,2)
for ax,mat,title in zip(axs,[original,recon],["Original","Reconstruida"]):
    ax.imshow(mat)
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()
