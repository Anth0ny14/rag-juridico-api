import json
from pathlib import Path


RUTA_CATALOGO = (
    "datos/catalogo_normas.json"
)


def actualizar_catalogo(

    sigla,

    nombre_completo,

    nombre_normalizado

):

    ruta = Path(
        RUTA_CATALOGO
    )

    if ruta.exists():

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:

            catalogo = json.load(
                archivo
            )

    else:

        catalogo = {}

    catalogo[sigla] = {

        "nombre_completo":
        nombre_completo,

        "nombre_normalizado":
        nombre_normalizado

    }

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(

            catalogo,

            archivo,

            ensure_ascii=False,

            indent=4

        )