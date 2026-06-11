import sys

from pathlib import Path

from config import (

    RAW_DIR,

    LIMPIO_DIR,

    CHUNKS_DIR

)

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from utilidades.normalizador_normas import (
    normalizar_nombre
)

from utilidades.catalogo_normas import (
    actualizar_catalogo
)

from ingestion.extractor_pdf import (
    procesar_pdf
)

from procesamiento.reconstructor_legal import (
    procesar_reconstruccion
)

from procesamiento.crear_chunks import (
    procesar_chunks
)

from vectorstore.indexador_chroma import (
    procesar_indexacion
)

from procesamiento.detector_articulos import (
    procesar_articulos
)

from procesamiento.limpiador_texto import (
    procesar_limpieza
)

def indexar_normativa(

    normativa_id,
    nombre_completo

):

    normativa_lower = normativa_id.lower()

    metadata = {
        "id": normativa_id,

        "doc_id": f"{normativa_id}_2025",

        "tipo": "ley",

        "titulo": normativa_id,

        "nombre_completo": nombre_completo,

        "nombre_normalizado": normalizar_nombre(nombre_completo),

        "jerarquia": 2
    }
    actualizar_catalogo(
        normativa_id,
        nombre_completo,
        normalizar_nombre(
            nombre_completo
        )
    )

    # Rutas

    ruta_pdf = str(
        RAW_DIR /
        f"{normativa_id}.pdf"
    )

    ruta_txt = str(
        LIMPIO_DIR /
        f"{normativa_lower}.txt"
    )

    ruta_limpio = str(
        LIMPIO_DIR /
        f"{normativa_lower}_limpio.txt"
    )

    ruta_reconstruido = str(
        LIMPIO_DIR /
        f"{normativa_lower}_reconstruido.txt"
    )

    ruta_chunks = str(
        CHUNKS_DIR /
        f"{normativa_lower}_chunks.json"
    )

    print(
        "\n[1/6] Extrayendo PDF..."
    )

    procesar_pdf(

        ruta_pdf,

        ruta_txt

    )

    print(
        "\n[2/6] Limpiando texto..."
    )
    procesar_limpieza(
        ruta_txt,
        ruta_limpio
    )

    print(
        "\n[3/6] Reconstruyendo texto..."
    )
    procesar_reconstruccion(

        ruta_limpio,

        ruta_reconstruido

    )

    ruta_articulos = (
        CHUNKS_DIR /
        f"{normativa_lower}_articulos.json"
    )

    print(
        "\n[4/6] Detectando Articulos..."
    )

    procesar_articulos(
        ruta_reconstruido,
        ruta_articulos
    )

    print(
    "\n[5/6] Creando chunks..."
    )

    procesar_chunks(
        ruta_articulos,
        ruta_chunks,
        metadata
    )

    print(
        "\n[6/6] Indexando en Chroma..."
    )

    procesar_indexacion(
        ruta_chunks
    )

    print(
        "\nNormativa indexada "
        "correctamente."
    )


if __name__ == "__main__":

    normativa = input(
        "Normativa ID: "
    )

    nombre_completo = input(
        "Nombre completo: "
    )

    indexar_normativa(

        normativa,

        nombre_completo

    )