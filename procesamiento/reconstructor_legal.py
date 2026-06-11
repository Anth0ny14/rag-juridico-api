from pathlib import Path
from config import (
    LIMPIO_DIR
)

RUTA_ENTRADA = str(

    LIMPIO_DIR /

    "losep.txt"

)

RUTA_SALIDA = str(

    LIMPIO_DIR /

    "losep_reconstruido.txt"

)

def unir_lineas_partidas(texto):

    lineas = texto.split("\n")

    resultado = []

    bloque_actual = ""

    i = 0

    while i < len(lineas):

        linea = lineas[i].strip()

        if not linea:

            i += 1
            continue

        # =========================
        # NUEVO ARTÍCULO
        # =========================

        if linea.startswith("Art."):

            if bloque_actual:

                resultado.append(
                    bloque_actual.strip()
                )

            bloque_actual = linea

        # =========================
        # CONCORDANCIAS
        # =========================

        elif linea.startswith(
            "CONCORDANCIAS"
        ):

            bloque_actual += "\n" + linea

        # =========================
        # NOTAS
        # =========================

        elif linea.startswith("Nota:"):

            i += 1

            while (

                i < len(lineas)

                and not lineas[i].startswith("Art.")

                and not lineas[i].startswith("CAPITULO")

                and not lineas[i].startswith("TITULO")

            ):

                i += 1

            continue

        # =========================
        # CAPÍTULOS / TÍTULOS
        # =========================

        elif linea.startswith(

            ("CAPITULO", "TITULO")

        ):

            if bloque_actual:

                resultado.append(
                    bloque_actual.strip()
                )

            bloque_actual = linea

        # =========================
        # CONTENIDO NORMAL
        # =========================

        else:

            bloque_actual += " " + linea

        i += 1

    if bloque_actual:

        resultado.append(
            bloque_actual.strip()
        )

    return "\n\n".join(resultado)

def reconstruir_texto(texto):

    lineas = texto.split("\n")

    nuevas_lineas = []

    i = 0

    while i < len(lineas):

        actual = lineas[i].strip()

        siguiente = ""

        if i + 1 < len(lineas):
            siguiente = lineas[i + 1].strip()

        # Caso:
        # .- Principios.-
        # Art. 1
        if actual.startswith(".-") and siguiente.startswith("Art."):

            linea_reconstruida = f"{siguiente} {actual}"

            nuevas_lineas.append(linea_reconstruida)

            i += 2
            continue

        nuevas_lineas.append(actual)

        i += 1

    return "\n".join(nuevas_lineas)


def guardar_texto(texto, ruta):

    Path(ruta).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)

def procesar_reconstruccion(

    ruta_entrada,

    ruta_salida

):

    with open(

        ruta_entrada,

        "r",

        encoding="utf-8"

    ) as archivo:

        texto = archivo.read()

    texto_reconstruido = reconstruir_texto(
        texto
    )

    texto_reconstruido = unir_lineas_partidas(
        texto_reconstruido
    )

    texto_reconstruido = (
        texto_reconstruido.replace(
            " .-",
            ".-"
        )
    )

    guardar_texto(

        texto_reconstruido,

        ruta_salida

    )

    return ruta_salida


if __name__ == "__main__":

    print(

        "Este módulo es invocado desde indexador_automatico.py"

    )