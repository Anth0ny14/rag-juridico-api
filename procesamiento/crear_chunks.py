import json
from pathlib import Path
import re
from config import (
    CHUNKS_DIR
)

RUTA_ENTRADA = str(
    CHUNKS_DIR /
    "articulos.json"
)

RUTA_SALIDA = str(
    CHUNKS_DIR /
    "losep_chunks.json"
)

def limpiar_texto_embedding(texto):

    patrones_corte = [

        r"Nota:",
        r"CONCORDANCIAS:",
        r"JURISPRUDENCIA:",
        r"Artículo agregado",
        r"Artículo sustituido",
        r"Artículo reformado",
        r"Disposición",
        r"TÍTULO",
        r"CAPÍTULO"

    ]

    texto_limpio = texto

    for patron in patrones_corte:

        partes = re.split(patron, texto_limpio)

        texto_limpio = partes[0]

    return texto_limpio.strip()

def crear_chunks(
        articulos,
        metadata
):

    chunks = []

    for articulo in articulos:

        numero_articulo = articulo["articulo"].replace("Art. ", "").strip()

        chunk = {
            "chunk_id": (f"{metadata['id']}" f"_ART_{numero_articulo}"),
            "doc_id": metadata["doc_id"],
            "tipo": metadata["tipo"],
            "titulo": metadata["titulo"],
            "nombre_completo": metadata["nombre_completo"],
            "nombre_normalizado": metadata["nombre_normalizado"],
            "articulo": articulo["articulo"],
            "vigente": True,
            "jerarquia": metadata["jerarquia"],
            "texto": articulo["texto"],
            "texto_embedding":limpiar_texto_embedding(
                articulo["texto"]
            )
        }

        chunks.append(chunk)

    return chunks


def guardar_json(datos, ruta):

    Path(ruta).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def procesar_chunks(

    ruta_entrada,

    ruta_salida,
    metadata

):

    with open(

        ruta_entrada,

        "r",

        encoding="utf-8"

    ) as archivo:

        articulos = json.load(archivo)

    chunks = crear_chunks(
        articulos,
        metadata
    )

    guardar_json(
        chunks,
        ruta_salida
    )

    return ruta_salida


if __name__ == "__main__":

    print(
        "Este módulo es invocado desde indexador_automatico.py"
    )