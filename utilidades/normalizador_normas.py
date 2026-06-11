import unicodedata


def normalizar_nombre(texto):

    texto = texto.upper().strip()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(

        c

        for c in texto

        if unicodedata.category(c) != "Mn"

    )

    return texto