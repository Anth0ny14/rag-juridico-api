TIPOS_DOCUMENTO = [
    "constitucion",
    "ley",
    "reglamento",
    "acuerdo",
    "resolucion"
]
JERARQUIA_NORMATIVA = {
    "constitucion": 1,
    "ley": 2,
    "reglamento": 3,
    "acuerdo": 4,
    "resolucion": 5
}
CHUNK_SCHEMA = {
    "chunk_id": "",
    "doc_id": "",
    "tipo": "",
    "titulo": "",
    "articulo": "",
    "texto": "",
    "vigente": True
}