import numpy as np
from quadtree import construir_quadtree, reconstruir
rng = np.random.default_rng(42)
for alto, ancho in [(63,63),(65,67),(127,129),(1,19),(19,1)]:
    img = rng.integers(0,256,size=(alto,ancho,3),dtype=np.uint8)
    arbol = construir_quadtree(img,0,0,ancho,alto,0)
    salida = np.zeros_like(img)
    reconstruir(arbol,salida)
    assert np.array_equal(img,salida),f"Error en {ancho}x{alto}"
    print(f"{ancho}x{alto}: reconstrucción exacta")
print("TODAS LAS PRUEBAS SUPERADAS")
