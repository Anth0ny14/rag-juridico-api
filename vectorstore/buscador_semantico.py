import chromadb
import re 
import os

from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_DIR
)


# Modelo embeddings
modelo = None

def obtener_modelo():

    global modelo

    if modelo is None:

        print("CARGANDO MODELO...")

        modelo = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return modelo

print("CHROMA DIR:")
print(CHROMA_DIR)

def obtener_coleccion():

    cliente = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    coleccion = cliente.get_collection(
        "normativa_juridica"
    )

    print(
        "TOTAL DOCUMENTOS:",
        coleccion.count()
    )

    return coleccion

def buscar_por_tema(

    tema,

    documento,

    top_k=5

):
    coleccion = obtener_coleccion()

    modelo = obtener_modelo()

    embedding_query = modelo.encode(
        tema
    ).tolist()

    resultados = coleccion.query(

        query_embeddings=[
            embedding_query
        ],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documentos_filtrados = []

    metadatas_filtradas = []

    distancias_filtradas = []

    for i in range(

        len(
            resultados["documents"][0]
        )

    ):

        metadata = (
            resultados["metadatas"][0][i]
        )

        if metadata["titulo"] == documento:

            documentos_filtrados.append(

                resultados["documents"][0][i]

            )

            metadatas_filtradas.append(
                metadata
            )

            distancias_filtradas.append(

                resultados["distances"][0][i]

            )

    return {

        "documents":
        documentos_filtrados,

        "metadatas":
        metadatas_filtradas,

        "distances":
        distancias_filtradas

    }

def buscar_fundamento_juridico(

    tema,

    articulo,

    documento

):
    coleccion = obtener_coleccion()

    resultados_tema = (
        buscar_por_tema(

            tema,

            documento

        )
    )

    if resultados_tema["documents"]:

        distancia = (
            resultados_tema[
                "distances"
            ][0]
        )

        if distancia < 0.80:

            return {

                "tipo":
                "tema",

                "resultado":
                {

                    "document":
                    resultados_tema[
                        "documents"
                    ][0],

                    "metadata":
                    resultados_tema[
                        "metadatas"
                    ][0]

                }

            }

    resultados_articulo = (
        buscar_articulo_exacto(

            coleccion,

            articulo,

            documento

        )
    )

    if resultados_articulo["documents"]:

        return {

            "tipo":
            "articulo",

            "resultado":
            {

                "document":
                resultados_articulo[
                    "documents"
                ][0],

                "metadata":
                resultados_articulo[
                    "metadatas"
                ][0]

            }

        }

    return None

def buscar(query, top_k=2):

    coleccion = obtener_coleccion()

    modelo = obtener_modelo()

    print("BUSCAR() TOTAL:", coleccion.count())

    embedding_query = modelo.encode(
        query
    ).tolist()

    resultados = coleccion.query(

        query_embeddings=[
            embedding_query
        ],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )

    print("\nRESULTADOS CRUDOS:")

    print(resultados)

    return resultados


def buscar_articulo_exacto(

    coleccion,

    articulo,

    documento

):

    return coleccion.get(

        where={

            "$and": [

                {
                    "articulo": articulo
                },

                {
                    "titulo": documento
                }

            ]
        }

    )


if __name__ == "__main__":

    consulta = input(
        "Tema jurídico: "
    )

    resultados = buscar(
        consulta,
        top_k=5
    )

    documentos = resultados["documents"][0]

    metadatas = resultados["metadatas"][0]

    distancias = resultados["distances"][0]

    for i in range(len(documentos)):

        print("\n" + "=" * 80)

        print("ARTÍCULO:")
        print(metadatas[i]["articulo"])

        print("\nDOCUMENTO:")
        print(metadatas[i]["titulo"])

        print("\nDISTANCIA:")
        print(distancias[i])

        print("\nTEXTO:")
        print(documentos[i][:500])
