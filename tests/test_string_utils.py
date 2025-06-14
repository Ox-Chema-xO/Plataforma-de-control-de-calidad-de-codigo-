import pytest
import src.utils.string_utils as string_utils


# ===== TESTS PARA FUNCIONES DE TRANSFORMACIÓN =====

@pytest.mark.parametrize("entrada, esperado", [
    ("python", "PYTHON"),
    ("hola mundo", "HOLA MUNDO"),
    ("123abc", "123ABC"),
    ("", ""),
    ("áéíóú", "ÁÉÍÓÚ"),
])
def test_convertir_a_mayusculas(entrada, esperado):
    resultado = string_utils.convertir_a_mayusculas(entrada)
    assert resultado == esperado


@pytest.mark.parametrize("entrada, esperado", [
    ("PYTHON", "python"),
    ("HoLa MuNdO", "hola mundo"),
    ("123ABC", "123abc"),
    ("", ""),
    ("ÁÉÍóú", "áéíóú"),
])
def test_convertir_a_minusculas(entrada, esperado):
    resultado = string_utils.convertir_a_minusculas(entrada)
    assert resultado == esperado


def test_capitalizar_palabras():
    texto = "hola mundo python"
    resultado = string_utils.capitalizar_palabras(texto)
    assert resultado == "Hola Mundo Python"


def test_capitalizar_primera_letra():
    texto = "hola MUNDO"
    resultado = string_utils.capitalizar_primera_letra(texto)
    assert resultado == "Hola mundo"


def test_capitalizar_primera_letra_cadena_vacia():
    texto = ""
    resultado = string_utils.capitalizar_primera_letra(texto)
    assert resultado == ""


def test_invertir_cadena():
    texto = "python"
    resultado = string_utils.invertir_cadena(texto)
    assert resultado == "nohtyp"


def test_normalizar_espacios():
    texto = "  hola    mundo   python  "
    resultado = string_utils.normalizar_espacios(texto)
    assert resultado == "hola mundo python"


# ===== TESTS PARA FUNCIONES DE VALIDACIÓN =====

@pytest.mark.parametrize("email, esperado", [
    ("test@ejemplo.com", True),
    ("usuario.123@dominio.org", True),
    ("test+tag@ejemplo.co.uk", True),
    ("invalido@", False),
    ("@ejemplo.com", False),
    ("sin_arroba.com", False),
    ("test@sin_dominio", False),
])
def test_es_email_valido(email, esperado):
    resultado = string_utils.es_email_valido(email)
    assert resultado == esperado


@pytest.mark.parametrize("texto, esperado", [
    ("123", True),
    ("123.45", True),
    ("-123", True),
    ("-123.45", True),
    ("0", True),
    ("abc", False),
    ("123abc", False),
    ("", False),
    ("12.34.56", False),
])
def test_es_numero(texto, esperado):
    resultado = string_utils.es_numero(texto)
    assert resultado == esperado


def test_contiene_solo_letras_verdadero():
    texto = "HolaMundo"
    assert string_utils.contiene_solo_letras(texto) is True


def test_contiene_solo_letras_falso():
    texto = "Hola123"
    assert string_utils.contiene_solo_letras(texto) is False


def test_contiene_solo_letras_espacios_verdadero():
    texto = "Hola Mundo"
    assert string_utils.contiene_solo_letras_espacios(texto) is True


def test_contiene_solo_letras_espacios_con_acentos():
    texto = "Hola Muñdo Niño"
    assert string_utils.contiene_solo_letras_espacios(texto) is True


def test_contiene_solo_letras_espacios_falso():
    texto = "Hola123 Mundo"
    assert string_utils.contiene_solo_letras_espacios(texto) is False


@pytest.mark.parametrize("texto, min_len, max_len, esperado", [
    ("python", 0, 10, True),
    ("python", 6, 6, True),
    ("python", 10, 20, False),
    ("", 0, 5, True),
    ("", 1, 5, False),
    ("test", 2, None, True),
    ("a", 2, None, False),
])
def test_cumple_longitud(texto, min_len, max_len, esperado):
    resultado = string_utils.cumple_longitud(texto, min_len, max_len)
    assert resultado == esperado


# ===== TESTS PARA FUNCIONES DE BÚSQUEDA Y REEMPLAZO =====

def test_buscar_patron_numeros():
    texto = "El año 2023 tiene 365 días"
    patron = r'\d+'
    resultado = string_utils.buscar_patron(texto, patron)
    assert resultado == ['2023', '365']


def test_buscar_patron_emails():
    texto = "Contactos: juan@test.com y maria@ejemplo.org"
    patron = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    resultado = string_utils.buscar_patron(texto, patron)
    assert resultado == ['juan@test.com', 'maria@ejemplo.org']


def test_reemplazar_patron_numeros():
    texto = "Tengo 25 años y mi hermana tiene 30 años"
    patron = r'\d+'
    reemplazo = 'X'
    resultado = string_utils.reemplazar_patron(texto, patron, reemplazo)
    assert resultado == "Tengo X años y mi hermana tiene X años"


def test_extraer_numeros_mixtos():
    texto = "Precio: $123.45, descuento: -10%, cantidad: 5"
    resultado = string_utils.extraer_numeros(texto)
    assert resultado == [123.45, -10, 5]


def test_extraer_palabras():
    texto = "¡Hola123 mundo! ¿Cómo estás?"
    resultado = string_utils.extraer_palabras(texto)
    assert resultado == ['Hola', 'mundo', 'Cómo', 'estás']


# ===== TESTS PARA FUNCIONES DE LIMPIEZA =====

def test_eliminar_espacios_extra():
    texto = "  Hola   mundo  \n\t python  "
    resultado = string_utils.eliminar_espacios_extra(texto)
    assert resultado == "Hola mundo python"


def test_limpiar_caracteres_especiales():
    texto = "¡Hola123, mundo!"
    resultado = string_utils.limpiar_caracteres_especiales(texto)
    assert resultado == "Hola123 mundo"


def test_limpiar_caracteres_especiales_mantener():
    texto = "¡Hola123, mundo!"
    resultado = string_utils.limpiar_caracteres_especiales(texto, ',!')
    assert resultado == "Hola123, mundo!"


def test_eliminar_acentos():
    texto = "Niño áéíóú ÁÉÍÓÚ ñÑ"
    resultado = string_utils.eliminar_acentos(texto)
    assert resultado == "Nino aeiou AEIOU nN"


def test_limpiar_html():
    texto = "<p>Hola <strong>mundo</strong></p>"
    resultado = string_utils.limpiar_html(texto)
    assert resultado == "Hola mundo"


def test_limpiar_html_con_espacios():
    texto = "<div>  <p>Hola</p>   <span>mundo</span>  </div>"
    resultado = string_utils.limpiar_html(texto)
    assert resultado == "Hola mundo"
