# Compresión de imágenes mediante Quadtree

**Universidad Nacional Autónoma de México — Facultad de Estudios Superiores Aragón**  
**Materia:** Diseño y Análisis de Algoritmos  
**Grupo:** 1510 (2027-I)  
**Trabajo:** Examen práctico  
**Profesor:** Víctor Manuel Sánchez Sánchez

## Integrantes

1. Carlos Daniel Balanzar Velasco
2. Giner Ortiz Vicente
3. Lara Hernandez Elias Lemuel
4. Martinez Guillen Martin

## Objetivo

Implementar y analizar, usando Divide y Vencerás, una representación de imágenes RGB mediante un **Quadtree**. Se divide recursivamente una región en hasta cuatro cuadrantes hasta que todos sus píxeles estén suficientemente próximos al color promedio o se alcance un solo píxel. Se reconstruye la imagen coloreando cada región hoja y se evalúan tiempo, nodos, profundidad, calidad y estimación de almacenamiento.

## Requisitos

- Python 3.10 o superior con `pip`.
- Paquetes: NumPy, Pillow, Matplotlib y Pandas.
- Se puede ejecutar desde Visual Studio 2022 con soporte para Python o desde PowerShell.

## Instalación y ejecución en Windows

Abra una terminal en esta carpeta y ejecute:

```powershell
py -m pip install -r requirements.txt
py verificacion.py
py experimentos.py
py graficas.py
py evidencias.py
```

> Si `py` no funciona pero `python` sí, sustituya `py` por `python`.

Para probar una fotografía real, coloque una imagen llamada `prueba.jpg` en la carpeta `imagenes` y ejecute:

```powershell
py main.py --imagen imagenes/prueba.jpg --tamano 128 --tolerancia 20
```

También admite otras rutas con `--imagen` y tolerancias como 0, 20 o 60. Se generará `resultados/reconstruida.png` y aparecerá una comparación visual.

En **Visual Studio 2022**, abra los archivos como proyecto Python, establezca el archivo deseado como archivo de inicio y use **Ctrl+F5**.

## Archivos

| Archivo | Función |
|---|---|
| `quadtree.py` | Nodo, construcción recursiva, reconstrucción y conteos. |
| `main.py` | Prueba interactiva con imagen real proporcionada por el usuario. |
| `experimentos.py` | Genera tres tipos de imágenes y ejecuta las 27 configuraciones con cinco mediciones cada una. |
| `verificacion.py` | Comprueba reconstrucción exacta para dimensiones impares con tolerancia cero. |
| `graficas.py` | Crea cuatro gráficas a partir del CSV. |
| `evidencias.py` | Genera tres comparaciones visuales con métricas. |
| `resultados/experimentos.csv` | Resultados originales registrados por el equipo (27 filas de configuración). |
| `reporte/` | Reporte técnico en PDF. |

## Diseño y métricas

Para cada región, se calcula el promedio de color por canal RGB. Si la máxima diferencia absoluta entre los píxeles y dicho promedio no supera la tolerancia, se representa como hoja con el promedio redondeado. De lo contrario se divide en cuadrantes no vacíos, lo que permite dimensiones impares.

Se registra el **MSE**, el número de nodos y hojas, profundidad y tiempo de construcción medido con `perf_counter`. Para el almacenamiento se emplea una **estimación teórica** de codificación preorden: 64 bits de dimensiones de imagen, 1 bit por nodo interno y 25 bits por hoja (1 bit de tipo más 24 bits RGB), redondeando el total a bytes. Los tamaños se comparan contra la matriz RGB sin comprimir (`ancho × alto × 3` bytes).

**Razón de compresión** = tamaño RGB sin comprimir / tamaño Quadtree teórico. No equivale al tamaño del JPG/PNG ni a un archivo Quadtree comprimido real: la serialización binaria no está implementada.

## Reproducibilidad y limitaciones

Se prueban imágenes **uniformes**, **cuatro regiones de color** y **ruido aleatorio** reproducible con semilla 42; tamaños de 64, 128 y 256 píxeles por lado; tolerancias de 0, 20 y 60. Se obtienen 27 configuraciones y **135 construcciones** (cinco tiempos por configuración). Se guardan promedio, mediana y desviación estándar. Los cinco tiempos individuales no se conservan en el CSV; volver a ejecutar `experimentos.py` lo sobrescribe y los tiempos cambiarán según el equipo.

El método no siempre consigue ahorro, sobre todo para ruido aleatorio. Las pruebas con imágenes sintéticas no permiten generalizar a cualquier fotografía. El peor caso temporal del enfoque actual es `Θ(n² log n)` por revisar todos los píxeles en cada nivel, y el espacial es `O(n²)` para imágenes cuadradas.

## Verificación y entrega

1. Ejecute `py verificacion.py` y compruebe que muestra `TODAS LAS PRUEBAS SUPERADAS`.
2. Ejecute `py experimentos.py` y confirme las 27 configuraciones.
3. Genere gráficas y evidencias.
4. Consulte el PDF para la justificación teórica y las conclusiones.

**Fuentes y bibliotecas:** NumPy, Pillow, Matplotlib y Pandas; referencias teóricas citadas en el reporte.
