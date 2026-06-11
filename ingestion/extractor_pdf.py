import fitz  # PyMuPDF
from pathlib import Path

from config import (
    RAW_DIR,
    LIMPIO_DIR
)

RUTA_PDF = str(

    RAW_DIR /

    "LOSNCP.pdf"

)

RUTA_SALIDA = str(

    LIMPIO_DIR /

    "losncp.txt"

)


def extraer_texto_pdf(ruta_pdf):

    texto_completo = ""

    documento = fitz.open(ruta_pdf)

    for pagina in documento:

        bloques = pagina.get_text("blocks")

        bloques_ordenados = sorted(
            bloques,
            key=lambda b: (b[1], b[0])
        )

        for bloque in bloques_ordenados:

            texto_bloque = bloque[4]

            texto_completo += texto_bloque + "\n"

    return texto_completo


def guardar_texto(texto, ruta_salida):

    Path(ruta_salida).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(ruta_salida, "w", encoding="utf-8") as archivo:

        archivo.write(texto)

def procesar_pdf(

    ruta_pdf,

    ruta_salida

):

    texto = extraer_texto_pdf(
        ruta_pdf
    )

    guardar_texto(
        texto,
        ruta_salida
    )

    return ruta_salida

if __name__ == "__main__":

    texto = extraer_texto_pdf(RUTA_PDF)

    guardar_texto(texto, RUTA_SALIDA)

    print("Texto extraído correctamente.")