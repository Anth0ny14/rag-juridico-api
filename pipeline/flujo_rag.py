import sys

from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)


from vectorstore.evaluador_retrieval import (
    retrieval_es_confiable
)

from pipeline.extractor_normativa import (
    extraer_normativa
)

from pipeline.verificador_corpus import (
    normativa_existe_localmente
)

from pipeline.descargador_normativa import (
    descargar_normativa
)

def activar_scraping(consulta):

    print("\n[SCRAPING ACTIVADO]")

    normativa = extraer_normativa(
        consulta
    )

    if not normativa:

        print(
            "\nNo se detectó normativa conocida."
        )

        return

    print(
        f"\nNormativa detectada: "
        f"{normativa['nombre_oficial']}"
    )

    existe = normativa_existe_localmente(
        normativa["id"]
    )

    if existe:

        print(
            "\nLa normativa ya existe "
            "localmente."
        )

        return

    print(
        "\nNormativa no encontrada "
        "localmente."
    )

    print(
        "\nDescargando normativa..."
    )

    descarga_ok = descargar_normativa(
        normativa
    )

    if descarga_ok:

        print(
            "\nNormativa descargada "
            "correctamente."
        )

    else:

        print(
            "\nNo fue posible descargar "
            "la normativa."
        )


def flujo_rag(

    consulta,

    distancia,

    texto_resultado

):

    confiable = retrieval_es_confiable(

        consulta,

        distancia,

        texto_resultado

    )

    if confiable:

        print("\n[USANDO CORPUS LOCAL]")

    else:

        activar_scraping(consulta)


if __name__ == "__main__":

    consulta = input("Consulta: ")

    distancia = float(
        input("Distancia: ")
    )

    texto = input("Texto resultado: ")

    flujo_rag(

        consulta,

        distancia,

        texto

    )