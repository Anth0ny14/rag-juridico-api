import json
from sentence_transformers import SentenceTransformer


RUTA_CHUNKS = "datos/chunks/losep_chunks.json"


# Modelo de embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")


def cargar_chunks(ruta):

    with open(ruta, "r", encoding="utf-8") as archivo:

        return json.load(archivo)


def generar_embeddings(chunks):

    textos = [chunk["texto"] for chunk in chunks]

    embeddings = modelo.encode(textos)

    return embeddings


if __name__ == "__main__":

    chunks = cargar_chunks(RUTA_CHUNKS)

    embeddings = generar_embeddings(chunks)

    print("Cantidad de chunks:", len(chunks))

    print("Dimensión embedding:", len(embeddings[0]))

    print("Primer embedding generado correctamente.")