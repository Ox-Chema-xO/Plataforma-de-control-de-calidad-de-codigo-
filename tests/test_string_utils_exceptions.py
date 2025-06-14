import pytest
import src.utils.string_utils as string_utils


# ===== TESTS DE EXCEPCIONES PARA FUNCIONES DE TRANSFORMACIÓN =====

@pytest.mark.parametrize("valor_invalido", [
    None,
    123,
    ["texto"],
    {"texto": "prueba"},
    45.67,
    True,
])
def test_funciones_transformacion_con_tipos_invalidos(valor_invalido):
    """Testa que las funciones de transformación lancen TypeError con tipos inválidos"""
    with pytest.raises(TypeError):
        string_utils.convertir_a_mayusculas(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.convertir_a_minusculas(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.capitalizar_palabras(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.capitalizar_primera_letra(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.invertir_cadena(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.normalizar_espacios(valor_invalido)

# ===== TESTS DE EXCEPCIONES PARA FUNCIONES DE VALIDACIÓN =====

@pytest.mark.parametrize("valor_invalido", [
    None,
    123,
    ["email@test.com"],
    {"email": "test@example.com"},
    45.67,
])
def test_funciones_validacion_basicas_con_tipos_invalidos(valor_invalido):
    """Testa que las funciones de validación básicas lancen TypeError con tipos inválidos"""
    with pytest.raises(TypeError):
        string_utils.es_email_valido(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.es_numero(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.contiene_solo_letras(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.contiene_solo_letras_espacios(valor_invalido)


@pytest.mark.parametrize("texto_invalido, min_len, max_len, error_esperado", [
    (None, 5, 10, TypeError),
    ("texto", -1, 10, ValueError),
    ("texto", "5", 10, ValueError),
    ("texto", 10, 5, ValueError),
    ("texto", 5, "10", ValueError),
])
def test_cumple_longitud_casos_invalidos(texto_invalido, min_len, max_len, error_esperado):
    """Testa casos inválidos para la función cumple_longitud"""
    with pytest.raises(error_esperado):
        string_utils.cumple_longitud(texto_invalido, min_len, max_len)


# ===== TESTS DE EXCEPCIONES PARA FUNCIONES DE BÚSQUEDA Y REEMPLAZO =====

@pytest.mark.parametrize("texto, patron, reemplazo, error_esperado", [
    (None, r'\d+', 'X', TypeError),
    ("texto", None, 'X', TypeError),
    ("texto", r'\d+', None, TypeError),
    (123, r'\d+', 'X', TypeError),
    ("texto", 456, 'X', TypeError),
    ("texto", r'\d+', 789, TypeError),
])
def test_buscar_reemplazar_patron_tipos_invalidos(texto, patron, reemplazo, error_esperado):
    """Testa que buscar_patron y reemplazar_patron lancen TypeError con tipos inválidos"""
    with pytest.raises(error_esperado):
        string_utils.reemplazar_patron(texto, patron, reemplazo)


@pytest.mark.parametrize("patron_invalido", [
    "[",
    "(?P<",
    "*",
    "(?P<nombre>",
])
def test_buscar_reemplazar_patron_regex_invalido(patron_invalido):
    """Testa que se lance ValueError con patrones regex inválidos"""
    with pytest.raises(ValueError):
        string_utils.buscar_patron("texto", patron_invalido)
    
    with pytest.raises(ValueError):
        string_utils.reemplazar_patron("texto", patron_invalido, "reemplazo")


@pytest.mark.parametrize("valor_invalido", [
    None,
    123,
    ["palabra1", "palabra2"],
    {"numero": 456},
    45.67,
])
def test_extraer_funciones_con_tipos_invalidos(valor_invalido):
    """Testa que las funciones de extracción lancen TypeError con tipos inválidos"""
    with pytest.raises(TypeError):
        string_utils.extraer_numeros(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.extraer_palabras(valor_invalido)


# ===== TESTS DE EXCEPCIONES PARA FUNCIONES DE LIMPIEZA =====

@pytest.mark.parametrize("valor_invalido", [
    None,
    123,
    ["<p>texto</p>"],
    {"html": "<div>contenido</div>"},
    45.67,
])
def test_funciones_limpieza_con_tipos_invalidos(valor_invalido):
    """Testa que las funciones de limpieza lancen TypeError con tipos inválidos"""
    with pytest.raises(TypeError):
        string_utils.eliminar_espacios_extra(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.eliminar_acentos(valor_invalido)
    
    with pytest.raises(TypeError):
        string_utils.limpiar_html(valor_invalido)


@pytest.mark.parametrize("texto_valido, mantener_invalido", [
    ("texto válido", None),
    ("texto válido", 123),
    ("texto válido", [".", "!"]),
    ("texto válido", {"chars": ".,!"}),
])
def test_limpiar_caracteres_especiales_mantener_invalido(texto_valido, mantener_invalido):
    """Testa que limpiar_caracteres_especiales lance TypeError con parámetro mantener inválido"""
    with pytest.raises(TypeError):
        string_utils.limpiar_caracteres_especiales(texto_valido, mantener_invalido)


def test_limpiar_caracteres_especiales_texto_invalido():
    """Testa que limpiar_caracteres_especiales lance TypeError con texto inválido"""
    with pytest.raises(TypeError):
        string_utils.limpiar_caracteres_especiales(None)


# ===== TESTS DE CASOS EDGE =====

def test_buscar_patron_texto_vacio():
    resultado = string_utils.buscar_patron("", r'\d+')
    assert resultado == []


def test_reemplazar_patron_texto_vacio():
    resultado = string_utils.reemplazar_patron("", r'\d+', 'X')
    assert resultado == ""


def test_extraer_numeros_sin_numeros():
    resultado = string_utils.extraer_numeros("solo texto sin números")
    assert resultado == []


def test_extraer_palabras_solo_numeros():
    resultado = string_utils.extraer_palabras("123 456 789")
    assert resultado == []


def test_limpiar_caracteres_especiales_solo_especiales():
    resultado = string_utils.limpiar_caracteres_especiales("!@#$%^&*()")
    assert resultado == ""


def test_eliminar_acentos_sin_acentos():
    texto = "Hola mundo sin acentos"
    resultado = string_utils.eliminar_acentos(texto)
    assert resultado == texto


def test_limpiar_html_sin_html():
    texto = "Texto sin etiquetas HTML"
    resultado = string_utils.limpiar_html(texto)
    assert resultado == texto
