from pathlib import Path


CARPETA_RAW = "datos/raw"


def normativa_existe_localmente(

    normativa_id

):

    ruta_pdf = Path(

        CARPETA_RAW
    ) / f"{normativa_id}.pdf"

    return ruta_pdf.exists()


if __name__ == "__main__":

    normativa = input(
        "ID normativa: "
    )

    existe = normativa_existe_localmente(
        normativa
    )

    print("\n¿EXISTE LOCALMENTE?\n")

    print(existe)