import re


def aplanar_lista(lista: list):
    """
    Se aplana una lista para cuando necesitemos
    procesar resultados de terraform de varios modulos,
    para los resultados de los test de acuerdo al tipo
    de prueba, entre otros
    """
    lista_aplanada = []
    for elemento in lista:
        if isinstance(elemento, list):
            lista_aplanada.extend(aplanar_lista(elemento))
        else:
            lista_aplanada.append(elemento)
    return lista_aplanada


def separar_lista(lista: list, condicion):
    """
    Separar en dos una lista para cuando se cumpla una determinada
    condicion y separar nuestros archivos python, terraform,
    categorizar test fallidos y exitosos, entre otros.
    """
    lista_cumplen = []
    lista_no_cumplen = []
    for elemento in lista:
        if condicion(elemento):
            lista_cumplen.append(elemento)
        else:
            lista_no_cumplen.append(elemento)
    return lista_cumplen, lista_no_cumplen


def agrupar_por_extension(lista_archivos: list):
    """
    Agrupar lista de archivos python, terraform,
    por su extension, entre otros
    """
    if (
        not isinstance(lista_archivos, list) or
        not all(isinstance(x, str) for x in lista_archivos)
    ):
        raise ValueError("Se requiere una lista de nombres de archivos(str)")
    grupos = {}
    for archivo in lista_archivos:
        if "." in archivo:
            extension = archivo[archivo.rfind("."):]
        else:
            extension = ""
        if extension not in grupos:
            grupos[extension] = []
        grupos[extension].append(archivo)
    return grupos


def eliminar_duplicados(lista: list):
    """
    Se elimina elementos duplicados preservando el orden cuando
    por error se repite test u archivos, entre otros
    """
    if (
        not isinstance(lista, list)
    ):
        raise ValueError("Se requiere una lista")
    try:
        lista_sin_duplicados = []
        conjunto = set()
        for elemento in lista:
            if elemento not in conjunto:
                conjunto.add(elemento)
                lista_sin_duplicados.append(elemento)
        return lista_sin_duplicados
    except TypeError:
        raise ValueError("Los elementos deben ser hashables")


def filtrar_por_patron(lista: list, patron: str, sensible_mayus: bool = True):
    """
    Filtramos mediante un patron nuestra lista de archivos python,
    terraform, pruebas unitarias de integracion, entre otros
    """
    if (
        not isinstance(lista, list) or
        not all(isinstance(x, str) for x in lista)
    ):
        raise ValueError("Se requiere una lista (str)")
    flag = 0 if sensible_mayus else re.IGNORECASE
    patron_compilado = re.compile(patron, flag)
    lista_filtrada = []
    for elemento in lista:
        if patron_compilado.search(elemento):
            lista_filtrada.append(elemento)
    return lista_filtrada


def ordenar_por_criterio(lista: list, criterio, descendente: bool = False):
    """
    Ordenar mediante un criterio listas de pruebas que tengan
    mayor prioridad o sean necesarios antes que otras pruebas
    u ordenar ciertos archivos, entre otros
    """
    if not isinstance(lista, list):
        raise ValueError("Se requiere una lista")
    lista_ordenada = sorted(lista, key=criterio, reverse=descendente)
    return lista_ordenada
