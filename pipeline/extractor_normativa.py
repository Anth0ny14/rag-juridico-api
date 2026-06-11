import json
import re


RUTA_NORMATIVAS = (
    "conocimiento/normativas.json"
)

import re


def extraer_articulo(consulta):

    patron = r"art\.?\s*(\d+)"

    match = re.search(

        patron,

        consulta,

        re.IGNORECASE

    )

    if match:

        return f"Art. {match.group(1)}"

    return None


def cargar_normativas():

    with open(

        RUTA_NORMATIVAS,

        "r",

        encoding="utf-8"

    ) as archivo:

        return json.load(archivo)


def extraer_normativa(consulta):

    consulta_lower = consulta.lower()

    normativas = cargar_normativas()

    for normativa in normativas:

        for alias in normativa["aliases"]:

            if alias.lower() in consulta_lower:

                return normativa

    return None


if __name__ == "__main__":

    consulta = input(
        "Consulta jurídica: "
    )

    normativa = extraer_normativa(
        consulta
    )

    print("\nNORMATIVA DETECTADA:\n")

    print(normativa)