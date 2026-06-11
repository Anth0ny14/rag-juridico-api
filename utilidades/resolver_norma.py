import json

from utilidades.normalizador_normas import (
    normalizar_nombre
)


from config import (
    CATALOGO_PATH
)


def resolver_norma(

    sigla=None,

    nombre_completo=None

):

    with open(

        CATALOGO_PATH,

        "r",

        encoding="utf-8"

    ) as archivo:

        catalogo = json.load(
            archivo
        )

    # PRIORIDAD 1
    if sigla:

        sigla = sigla.strip().upper()

        if sigla in catalogo:

            return sigla

    # PRIORIDAD 2
    if nombre_completo:

        nombre_normalizado = normalizar_nombre(

            nombre_completo

        )

        for sigla_catalogo, datos in (

            catalogo.items()

        ):

            if (

                datos["nombre_normalizado"]

                == nombre_normalizado

            ):

                return sigla_catalogo

    return None

if __name__ == "__main__":

    print(
        resolver_norma(
            sigla="rglosncp"
        )

    )