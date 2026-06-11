import json
import chromadb

from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_DIR,
    CHUNKS_DIR
)

RUTA_CHUNKS = str(
    CHUNKS_DIR /
    "losep_chunks.json"
)


# Modelo embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")


# Cliente Chroma
cliente = chromadb.PersistentClient(path=str(CHROMA_DIR))


# Crear colección
coleccion = cliente.get_or_create_collection(
    name="normativa_juridica"
)


def cargar_chunks(ruta):

    with open(ruta, "r", encoding="utf-8") as archivo:

        return json.load(archivo)


def indexar_chunks(chunks):

    for chunk in chunks:

        embedding = modelo.encode(chunk["texto_embedding"]).tolist()

        coleccion.upsert(

            ids=[chunk["chunk_id"]],

            embeddings=[embedding],

            documents=[chunk["texto"]],

            metadatas=[

                {
                    "doc_id": chunk["doc_id"],
                    "tipo": chunk["tipo"],
                    "articulo": chunk["articulo"],
                    "titulo": chunk["titulo"]
                }

            ]
        )


def procesar_indexacion(

    ruta_chunks

):

    chunks = cargar_chunks(
        ruta_chunks
    )

    indexar_chunks(
        chunks
    )

    return True

if __name__ == "__main__":

    chunks = cargar_chunks(RUTA_CHUNKS)

    indexar_chunks(chunks)

    print("Chunks indexados correctamente en ChromaDB.")