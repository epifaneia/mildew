# Mildew · Clasificador de hojas de cerezo, rescatado

*Read this in [English](README.md).*

Una red convolucional que distingue hojas de cerezo sanas de hojas con oídio, tres notebooks que la llevan de la descarga en bruto a la evaluación en el conjunto de test, y una app en Streamlit para probarla con tus propias imágenes.

Fue mi proyecto de Predictive Analytics en Code Institute, en abril de 2024. En octubre de 2026 lo rescaté: la app ya no estaba desplegada, las dependencias ya no instalaban y el notebook de entrenamiento no tenía salidas guardadas, así que nada en el repositorio demostraba su precisión. Al rescatarlo encontré dos vías por las que el test antiguo podía filtrarse al entrenamiento. Esta versión cierra las dos y vuelve a medir.

[Lo que encontró el rescate](#lo-que-encontró-el-rescate) · [Medido](#medido) · [Los notebooks](#los-notebooks) · [Probarlo](#probarlo) · [Limitaciones](#limitaciones)

---

## Lo que encontró el rescate

**1. El dataset se repite.** La descarga de Kaggle tiene 5.779 imágenes, pero 1.393 son copias exactas, byte a byte, de otra (704 sanas y 689 con oídio), al parecer repartidas entre las propias carpetas `train/` y `test/` del dataset. Imágenes únicas: 2.282 sanas y 2.104 con oídio. En 2024 entraron todas en la partición, así que la misma imagen podía estar en entrenamiento y en test.

**2. Las imágenes sintéticas se hacían antes de partir.** Para equilibrar las clases, el notebook de 2024 generaba copias espejadas, giradas o con otro brillo de las hojas con oídio, y solo después lo repartía todo en train, validación y test. Una copia podía caer en test mientras su original estaba en entrenamiento.

**El arreglo, en ese orden:** quitar los duplicados exactos, partir 70/10/20 por clase con una semilla fija, y solo entonces equilibrar el conjunto de **entrenamiento** con imágenes sintéticas. Validación y test tienen solo imágenes originales, en sus proporciones naturales.

## Medido

| | |
|---|---|
| Conjunto de test | 879 imágenes originales (457 sanas, 422 con oídio), nunca vistas en entrenamiento de ninguna forma |
| Acierto en test | **879 / 879 (100 %)**, 0 errores |
| Imágenes de test con un gemelo casi idéntico en entrenamiento | 1 de 879 (hash de diferencias de 64 bits, ≤ 2 bits) |
| Entrenamiento | 3.194 imágenes (1.597 por clase, 125 de ellas sintéticas) · 15 épocas · unos 2 minutos en la CPU de un portátil |
| Cifra de 2024, como referencia | 99,83 %, medida con las dos filtraciones de arriba y no reproducible desde el repositorio |

Una puntuación perfecta es motivo de sospecha antes que de orgullo, así que el notebook 03 la comprueba: los duplicados exactos ya no están, y los casi duplicados (la misma foto recomprimida o algo cambiada) prácticamente no existen. La puntuación no es filtración. **Este dataset es fácil**: una hoja por foto, fondo liso, luz uniforme. Las curvas de aprendizaje muestran que la pérdida de validación sube un poco a partir de la época 8, un sobreajuste leve que las 15 épocas mantienen para poder comparar con 2024.

Todas las cifras de esta tabla salen de `outputs/metrics.json`, que escribe el notebook 03; la página de resultados de la app lee el mismo fichero.

## Los notebooks

El núcleo del proyecto y lo primero que hay que leer. Cada uno empieza con su objetivo, explica cada paso antes del código y está guardado **con sus salidas**: se puede leer todo el proceso en GitHub sin ejecutar nada.

| Notebook | Qué hace | Qué se ve en él |
|---|---|---|
| [01 · Descarga de datos](notebooks/01_Kaggle_Data_Download.ipynb) | Descarga el dataset de Kaggle con tu propio token | Las imágenes por carpeta, tal como se publicaron |
| [02 · Preparación de datos](notebooks/02_Data_preparation.ipynb) | Quita duplicados, parte con semilla, equilibra solo el entrenamiento, redimensiona a 50×50 | Los duplicados encontrados, los tres conjuntos, hojas de muestra |
| [03 · CNN](notebooks/03_CNN.ipynb) | Entrena, evalúa una sola vez en test, busca casi duplicados, guarda el modelo y las métricas | Registro del entrenamiento, curvas, informe de clasificación, matriz de confusión |

La descarga en bruto nunca se modifica: el notebook 02 escribe en `inputs/prepared/` y se puede volver a ejecutar. Los notebooks están en inglés.

## Probarlo

```bash
python -m venv .venv && .venv\Scripts\activate          # en Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py
```

El modelo entrenado está en el repositorio (`outputs/cherry_leaf_cnn.keras`), así que la app funciona sin reentrenar ni descargar el dataset. *Model Interaction* acepta imágenes JPG o PNG, varias a la vez o en un ZIP.

TODO: hojas de muestra para probar la app (`samples/`): pendiente de comprobar la licencia.

Para repetir todo el proceso, de la descarga a la evaluación:

```bash
pip install -r requirements-notebooks.txt
jupyter notebook notebooks/
```

El notebook 01 necesita un token de la API de Kaggle en `~/.kaggle/kaggle.json` (kaggle.com → Settings → API → *Create New Token*). El token nunca entra en el repositorio.

## Limitaciones

- **Un solo dataset, y fácil.** Hojas sueltas sobre fondo liso. Cómo se comporta con fotos hechas en una plantación, con varias hojas, sombras y tierra, está sin medir, y es lo primero que necesitaría datos nuevos.
- **50×50 píxeles**, mantenidos de 2024 para poder comparar. Las manchas tempranas de oídio pueden quedar por debajo de un píxel a ese tamaño.
- **Sin control de imágenes fuera de distribución.** El modelo siempre responde sana u oídio, le enseñes lo que le enseñes, así que su respuesta solo significa algo para una hoja suelta sobre fondo liso, como las del dataset. Una imagen blanca, sin ninguna hoja, recibe una probabilidad de oídio de 0,69; imágenes de un solo color verde, gris o negro reciben de 0,00 a 0,99 según el tono. La app muestra este aviso en *Model Interaction*.
- **Una ejecución, una semilla.** Sin validación cruzada. 0 errores en 879 no es «100 %»: por la regla del tres, la cota superior al 95 % de la tasa de error es de unos 3/879 = 0,34 %, en este tipo de imagen.
- **Licencia del dataset:** no figura en su [página de Kaggle](https://www.kaggle.com/datasets/ahmadhabibhasanzein/cherry-leaves) (comprobado en octubre de 2026). Las imágenes no se redistribuyen aquí; los notebooks las descargan.
- La app es una demo, no una herramienta para decidir en una plantación real.

---

## Estructura

```
notebooks/     01 descarga · 02 preparación · 03 CNN (guardados con sus salidas)
app/           app de Streamlit: app.py y app_pages/ (un módulo por página)
outputs/       cherry_leaf_cnn.keras · metrics.json · figures/ (los escribe el notebook 03)
inputs/        el dataset, descargado por el notebook 01 (fuera de git)
```

Hecho con TensorFlow/Keras 3, scikit-learn, Pillow y Streamlit, en Python 3.13.

Daniel Martín · [epifaneia.dev](https://epifaneia.dev) · Apache-2.0
