import re


# ===== FUNCIONES DE TRANSFORMACIÓN =====

def convertir_a_mayusculas(texto: str) -> str:
    """
    Convierte una cadena de texto a mayúsculas
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    return texto.upper()


def convertir_a_minusculas(texto: str) -> str:
    """
    Convierte una cadena de texto a minúsculas
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    return texto.lower()


def capitalizar_palabras(texto: str) -> str:
    """
    Capitaliza la primera letra de cada palabra en una cadena
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    return texto.title()


def capitalizar_primera_letra(texto: str) -> str:
    """
    Capitaliza solo la primera letra de la cadena
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    if not texto:
        return texto
    return texto[0].upper() + texto[1:].lower()


def invertir_cadena(texto: str) -> str:
    """
    Invierte el orden de los caracteres en una cadena
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    return texto[::-1]


def normalizar_espacios(texto: str) -> str:
    """
    Normaliza los espacios en blanco, eliminando espacios extra
    y dejando solo un espacio entre palabras
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    return " ".join(texto.split())


# ===== FUNCIONES DE VALIDACIÓN =====

def es_email_valido(email: str) -> bool:
    """
    Valida si una cadena tiene formato de email válido
    """
    if not isinstance(email, str):
        raise TypeError("Se requiere una cadena de texto")
    
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron_email, email))


def es_numero(texto: str) -> bool:
    """
    Valida si una cadena representa un número (entero o decimal)
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    try:
        float(texto)
        return True
    except ValueError:
        return False


def contiene_solo_letras(texto: str) -> bool:
    """
    Valida si una cadena contiene únicamente letras (sin espacios ni números)
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    return texto.isalpha()


def contiene_solo_letras_espacios(texto: str) -> bool:
    """
    Valida si una cadena contiene únicamente letras y espacios
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
    return bool(re.match(patron, texto))


def cumple_longitud(texto: str, min_len: int = 0, max_len: int = None) -> bool:
    """
    Valida si una cadena cumple con los requisitos de longitud mínima y máxima
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    if not isinstance(min_len, int) or min_len < 0:
        raise ValueError("La longitud mínima debe ser un entero no negativo")
    if max_len is not None and (not isinstance(max_len, int) or max_len < min_len):
        raise ValueError("La longitud máxima debe ser un entero mayor o igual a la mínima")
    
    longitud = len(texto)
    if max_len is None:
        return longitud >= min_len
    return min_len <= longitud <= max_len
