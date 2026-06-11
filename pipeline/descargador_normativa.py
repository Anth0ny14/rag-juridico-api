import requests

from pathlib import Path


CARPETA_DESTINO = "datos/raw"


HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

}


def descargar_normativa(normativa):

    normativa_id = normativa["id"]

    fuentes = normativa["fuentes"]

    if not fuentes:

        print(
            "\nNo existen fuentes disponibles."
        )

        return False

    fuente = fuentes[0]

    url = fuente["url"]

    try:

        respuesta = requests.get(

            url,

            headers=HEADERS,

            timeout=30

        )

        if respuesta.status_code == 200:

            Path(CARPETA_DESTINO).mkdir(

                parents=True,

                exist_ok=True

            )

            ruta_archivo = (
                f"{CARPETA_DESTINO}/{normativa_id}.pdf"
            )

            with open(

                ruta_archivo,

                "wb"

            ) as archivo:

                archivo.write(
                    respuesta.content
                )

            print(
                f"\n{normativa_id} descargada correctamente."
            )

            return True

        else:

            print(
                f"\nError HTTP {respuesta.status_code}"
            )

            return False

    except Exception as e:

        print(
            f"\nError descargando normativa: {e}"
        )

        return False