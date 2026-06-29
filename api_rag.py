import os
print("PID API:", os.getpid())


from fastapi import (

    FastAPI,

    UploadFile,

    File,

    Form

)
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import shutil
import time

from pipeline.indexador_automatico import (
    indexar_normativa
)

from config import CHROMA_DIR

from vectorstore.buscador_semantico import (

    buscar,

    buscar_articulo_exacto,

    buscar_fundamento_juridico,

    obtener_coleccion

)

from utilidades.resolver_norma import (
    resolver_norma
)

from vectorstore.evaluador_retrieval import (
    retrieval_es_confiable
)
from vectorstore.validador_consistencia import (
    validar_consistencia
)

inicio = time.time()

print("INICIANDO API...")
app = FastAPI()
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)
print("FASTAPI CREADO")



@app.get("/")
def root():
    return {
        "status": "ok"
    }
print("TIEMPO TOTAL:", time.time() - inicio)

@app.get("/consulta_articulo")
def consulta_articulo(

    articulo: str,

    documento: str

):
    coleccion = obtener_coleccion()

    resultados = buscar_articulo_exacto(

        coleccion,

        articulo,

        documento

    )

    documentos = resultados.get(
        "documents",
        []
    )

    metadatas = resultados.get(
        "metadatas",
        []
    )

    if not documentos:

        return {

            "ok": False,

            "mensaje": (
                "Artículo no encontrado"
            )
        }

    return {

        "ok": True,

        "articulo":
        metadatas[0]["articulo"],

        "documento":
        metadatas[0]["titulo"],

        "texto":
        documentos[0]
    }

@app.get("/fundamento_juridico")
def fundamento_juridico(

    tema: str = None,

    articulo: str = None,

    documento: str = None,

    nombre_completo: str = None

):

    documento_resuelto = resolver_norma(

        sigla=documento,

        nombre_completo=nombre_completo

    )

    if documento_resuelto is None:

        return {

            "ok": False,

            "norma_disponible": False,

            "mensaje":
            "La normativa solicitada no se encuentra en la base documental."

        }

    # =====================================
    # RECUPERACIÓN DE CANDIDATOS
    # =====================================

    resultado = buscar_fundamento_juridico(

        tema,

        articulo,

        documento_resuelto

    )

    resultado_articulo = resultado["articulo"]

    resultado_tema = resultado["tema"]

    # =====================================
    # NO SE ENCONTRÓ NADA
    # =====================================

    if resultado_articulo is None and resultado_tema is None:

        return {

            "ok": False,

            "mensaje":

            "Fundamento jurídico no encontrado"

        }

    # =====================================
    # SOLO EXISTE ARTÍCULO
    # =====================================

    if resultado_articulo is not None and resultado_tema is None:

        resultado_final = resultado_articulo

    # =====================================
    # SOLO EXISTE TEMA
    # =====================================

    elif resultado_articulo is None and resultado_tema is not None:

        resultado_final = resultado_tema

    # =====================================
    # EXISTEN LOS DOS
    # =====================================

    else:

        articulo_articulo = (

            resultado_articulo["metadata"]["articulo"]

        )

        articulo_tema = (

            resultado_tema["metadata"]["articulo"]

        )

        # Ambos apuntan al mismo artículo

        if articulo_articulo == articulo_tema:

            print("\nARTÍCULO Y TEMA COINCIDEN")

            resultado_final = resultado_articulo

        # Existe conflicto

        else:

            print("\nCONFLICTO DETECTADO")

            decision = validar_consistencia(

                tema,

                resultado_articulo,

                resultado_tema
            )
            print( "\nDECISIÓN FINAL:", decision["ganador"] )

            resultado_final = decision["resultado"]

    # =====================================
    # RESPUESTA FINAL
    # =====================================

    metadata = resultado_final["metadata"]

    texto = resultado_final["document"]

    return {

        "ok": True,

        "tipo_recuperacion":

        resultado_final["tipo"],

        "articulo":

        metadata["articulo"],

        "documento":

        metadata["titulo"],

        "texto":

        texto

    }
    


@app.get("/consulta")

def consultar(

    query: str

):

    # ==================================
    # BÚSQUEDA SEMÁNTICA
    # ==================================

    resultados = buscar(query)

    documentos = resultados["documents"][0]

    metadatas = resultados["metadatas"][0]

    distancias = resultados["distances"][0]

    respuesta = []

    for i in range(len(documentos)):

        confiable = retrieval_es_confiable(

            query,

            distancias[i],

            documentos[i]

        )

        respuesta.append(

            {

                "articulo":
                metadatas[i]["articulo"],

                "documento":
                metadatas[i]["titulo"],

                "texto":
                documentos[i],

                "distancia":
                distancias[i],

                "retrieval_confiable":
                confiable
            }
        )

    return {

        "tipo_busqueda": "semantica",

        "query": query,

        "resultados": respuesta
    }

@app.post("/normativas")
def cargar_normativa(

    archivo: UploadFile = File(...),

    sigla: str = Form(...),

    nombre_completo: str = Form(...)

):

    try:

        sigla = sigla.upper().strip()

        from config import (
            RAW_DIR
        )
        RAW_DIR.mkdir(
            parents=True,

            exist_ok=True

        )

        ruta_pdf = (
            RAW_DIR /
            f"{sigla}.pdf"
        )

        with open(

            ruta_pdf,

            "wb"

        ) as buffer:

            shutil.copyfileobj(

                archivo.file,

                buffer

            )

        indexar_normativa(

            sigla,

            nombre_completo

        )

        return {

            "ok": True,

            "mensaje":

            "Normativa incorporada correctamente"

        }

    except Exception as e:

        return {

            "ok": False,

            "mensaje":

            str(e)

        }
    
@app.get("/debug")
def debug():

    return {

        "existe_chroma":
        CHROMA_DIR.exists(),

        "chroma_dir":
        str(CHROMA_DIR),

        "contenido_chroma":
        [
            x.name
            for x in CHROMA_DIR.iterdir()
        ]
        if CHROMA_DIR.exists()
        else []

    }

@app.get("/debug_chroma")
def debug_chroma():
    import chromadb

    cliente = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    coleccion = cliente.get_collection(
        "normativa_juridica"
    )

    return {
        "path": str(CHROMA_DIR),
        "collections": [c.name for c in cliente.list_collections()],
        "count": coleccion.count(),
        "peek": coleccion.peek()
    }