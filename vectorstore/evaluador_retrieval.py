def contiene_terminos_clave(
    consulta,
    texto
):

    palabras = consulta.lower().split()

    texto = texto.lower()

    coincidencias = 0

    for palabra in palabras:

        if palabra in texto:

            coincidencias += 1

    return coincidencias


def retrieval_es_confiable(

    consulta,

    distancia,

    texto_resultado,

    threshold_distancia=1.2,

    min_coincidencias=2

):

    # Validar distancia
    if distancia > threshold_distancia:

        return False

    # Validar coincidencias semánticas simples
    coincidencias = contiene_terminos_clave(

        consulta,

        texto_resultado

    )

    if coincidencias < min_coincidencias:

        return False

    return True