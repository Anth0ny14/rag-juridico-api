import re

from sentence_transformers import util

from vectorstore.buscador_semantico import (
    obtener_modelo
)


def obtener_encabezado(texto):

    coincidencia = re.match(

        r"Art\.\s*\d+\.?-?\s*(.*?)(?:\.-|\.|:)",

        texto

    )

    if coincidencia:

        return coincidencia.group(1).strip()

    return texto[:150]


def validar_consistencia(

    tema,

    resultado_articulo,

    resultado_tema

):

    # Si no existe tema no hay nada que comparar
    if not tema:

        return None

    modelo = obtener_modelo()

    embedding_tema = modelo.encode(

        tema,

        convert_to_tensor=True

    )

    encabezado_articulo = obtener_encabezado(

        resultado_articulo["document"]

    )

    embedding_articulo = modelo.encode(

        encabezado_articulo,

        convert_to_tensor=True

    )

    encabezado_tema = obtener_encabezado(

        resultado_tema["document"]

    )

    embedding_resultado_tema = modelo.encode(

        encabezado_tema,

        convert_to_tensor=True

    )

    similitud_articulo = util.cos_sim(

        embedding_tema,

        embedding_articulo

    ).item()

    similitud_tema = util.cos_sim(

        embedding_tema,

        embedding_resultado_tema

    ).item()
    MARGEN = 0.03

    print("\n========== VALIDACIÓN ==========")

    print("\nENCABEZADO ARTÍCULO:")

    print(encabezado_articulo)

    print("\nENCABEZADO TEMA:")

    print(encabezado_tema)

    print(

        "\nSimilitud Tema ↔ Artículo:",

        similitud_articulo

    )

    print(

        "Similitud Tema ↔ Resultado Tema:",

        similitud_tema

    )

    print("===============================\n")
    diferencia = abs(
        similitud_articulo -
        similitud_tema
    )

    print(

        "Diferencia:",

        diferencia
    )

    if diferencia < MARGEN:
        print(
            "\nSIMILITUDES MUY CERCANAS"
        )
        print(
            "Se prioriza el artículo recibido."
        )

        return {

            "ganador": "articulo",

            "resultado": resultado_articulo,

            "similitud": similitud_articulo
        }

    if similitud_articulo > similitud_tema:
       print("\nGANADOR: ARTÍCULO\n")
       return{
           "ganador": "articulo",

            "resultado": resultado_articulo,

            "similitud": similitud_articulo
       } 
    else:
        print("\nGANADOR: TEMA\n")
        return {
            "ganador": "tema",

            "resultado": resultado_tema,

            "similitud": similitud_tema
        }