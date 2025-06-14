import re
import unicodedata


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


# ===== FUNCIONES DE BÚSQUEDA Y REEMPLAZO =====

def buscar_patron(texto: str, patron: str) -> list:
    """
    Busca todas las ocurrencias de un patrón regex en una cadena
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    if not isinstance(patron, str):
        raise TypeError("Se requiere un patrón de búsqueda válido")
    
    try:
        return re.findall(patron, texto)
    except re.error as e:
        raise ValueError(f"Patrón regex inválido: {e}")


def reemplazar_patron(texto: str, patron: str, reemplazo: str) -> str:
    """
    Reemplaza todas las ocurrencias de un patrón con el texto de reemplazo
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    if not isinstance(patron, str):
        raise TypeError("Se requiere un patrón de búsqueda válido")
    if not isinstance(reemplazo, str):
        raise TypeError("Se requiere un texto de reemplazo válido")
    
    try:
        return re.sub(patron, reemplazo, texto)
    except re.error as e:
        raise ValueError(f"Patrón regex inválido: {e}")


def extraer_numeros(texto: str) -> list:
    """
    Extrae todos los números (enteros y decimales) de una cadena
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    patron_numeros = r'-?\d+\.?\d*'
    numeros_str = re.findall(patron_numeros, texto)
    numeros = []
    
    for num_str in numeros_str:
        if '.' in num_str:
            try:
                numeros.append(float(num_str))
            except ValueError:
                continue
        else:
            try:
                numeros.append(int(num_str))
            except ValueError:
                continue
    
    return numeros


def extraer_palabras(texto: str) -> list:
    """
    Extrae todas las palabras de una cadena (solo letras)
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    patron_palabras = r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+'
    return re.findall(patron_palabras, texto)


# ===== FUNCIONES DE LIMPIEZA =====

def eliminar_espacios_extra(texto: str) -> str:
    """
    Elimina espacios en blanco extra, al inicio, final y múltiples espacios
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    return re.sub(r'\s+', ' ', texto).strip()


def limpiar_caracteres_especiales(texto: str, mantener: str = '') -> str:
    """
    Elimina caracteres especiales, manteniendo solo letras, números y espacios
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    if not isinstance(mantener, str):
        raise TypeError("Los caracteres a mantener deben ser una cadena")
    
    # Patrón base: letras, números, espacios
    patron_base = r'[^a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑ'
    
    # Escapar caracteres especiales en mantener
    mantener_escapado = re.escape(mantener)
    patron_completo = patron_base + mantener_escapado + ']'
    
    return re.sub(patron_completo, '', texto)


def eliminar_acentos(texto: str) -> str:
    """
    Elimina acentos y diacríticos de una cadena
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    # Normalizar a NFD (decomposed form)
    texto_normalizado = unicodedata.normalize('NFD', texto)
    
    # Filtrar caracteres de marcas diacríticas
    texto_sin_acentos = ''.join(
        char for char in texto_normalizado
        if unicodedata.category(char) != 'Mn'
    )
    
    return texto_sin_acentos


def limpiar_html(texto: str) -> str:
    """
    Elimina etiquetas HTML básicas de una cadena
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    # Eliminar etiquetas HTML
    patron_html = r'<[^>]+>'
    texto_limpio = re.sub(patron_html, '', texto)
    
    # Limpiar espacios extra resultantes
    return eliminar_espacios_extra(texto_limpio)
