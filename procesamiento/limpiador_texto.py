import re
from pathlib import Path
from config import (
    LIMPIO_DIR
)

RUTA_ENTRADA = str(

    LIMPIO_DIR /

    "losncp.txt"

)

RUTA_SALIDA = str(

    LIMPIO_DIR /

    "losncp_limpio.txt"

)


def limpiar_texto(texto):

    # Normalizar saltos de línea
    texto = re.sub(
        r"\n{3,}",
        "\n\n",
        texto
    )

    # Normalizar espacios
    texto = re.sub(
        r"[ \t]+",
        " ",
        texto
    )

    # Eliminar espacios antes de salto
    texto = re.sub(
        r" +\n",
        "\n",
        texto
    )
    
    return texto


def guardar_texto(texto, ruta):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)

def procesar_limpieza(

    ruta_entrada,

    ruta_salida

):

    with open(

        ruta_entrada,

        "r",

        encoding="utf-8"

    ) as archivo:

        texto = archivo.read()

    texto_limpio = limpiar_texto(
        texto
    )

    guardar_texto(

        texto_limpio,

        ruta_salida

    )

    return ruta_salida

if __name__ == "__main__":

    print(

        "Este módulo es invocado desde indexador_automatico.py"

    )