import chromadb


cliente = chromadb.PersistentClient(
    path="datos/chroma"
)

coleccion = cliente.get_collection(
    name="normativa_juridica"
)


coleccion.delete(

    where={

        "doc_id": "RGLOSNCP_2025"

    }

)

print(
    "RGLOSNCP eliminado de Chroma."
)