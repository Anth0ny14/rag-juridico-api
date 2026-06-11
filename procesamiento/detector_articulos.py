import re
import json
from pathlib import Path
from config import (
    LIMPIO_DIR,
    CHUNKS_DIR
)

RUTA_ENTRADA = str(

    LIMPIO_DIR /

    "losep_reconstruido.txt"

)

RUTA_SALIDA = str(

    CHUNKS_DIR /

    "articulos.json"

)


def extraer_articulos(texto):

    patron = r"Art\.\s*(\d+(\.\d+)?|\.{3})"

    coincidencias = list(re.finditer(patron, texto))

    articulos = []

    for i in range(len(coincidencias)):

        inicio = coincidencias[i].start()

        if i + 1 < len(coincidencias):
            fin = coincidencias[i + 1].start()
        else:
            fin = len(texto)

        contenido = texto[inicio:fin].strip()

        articulos.append({
            "articulo": coincidencias[i].group(),
            "texto": contenido
        })

    return articulos


def guardar_json(datos, ruta):

    Path(ruta).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def procesar_articulos(

    ruta_entrada,

    ruta_salida

):

    with open(

        ruta_entrada,

        "r",

        encoding="utf-8"

    ) as archivo:

        texto = archivo.read()

    articulos = extraer_articulos(
        texto
    )

    guardar_json(

        articulos,

        ruta_salida

    )

    return ruta_salida

if __name__ == "__main__":

    print(

        "Este módulo es invocado desde indexador_automatico.py"

    )