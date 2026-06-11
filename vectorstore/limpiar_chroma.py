import chromadb


cliente = chromadb.PersistentClient(path="datos/chroma")


cliente.delete_collection("normativa_juridica")


print("Colección eliminada correctamente.")