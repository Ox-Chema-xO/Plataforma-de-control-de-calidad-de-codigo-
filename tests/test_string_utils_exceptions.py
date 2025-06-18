import pytest
from src.utils.string_utils import (
    extraer_metricas_de_output,
    normalizar_output_comando,
    parsear_ruta_archivo,
    limpiar_nombre_archivo,
    procesar_salida_herramienta
)


class TestExcepcionesExtraerMetricas:
    """Tests de excepciones para extraer_metricas_de_output."""
    @pytest.mark.parametrize("invalid_input", [
        None,
        123,
        [],
        {},
        set(),
        True,
        42.5
    ])
    def test_tipo_invalido_lanza_excepcion(self, invalid_input):
        """Lanza TypeError con tipos de entrada inválidos."""
        with pytest.raises(TypeError, match="Se requiere una cadena de texto"):
            extraer_metricas_de_output(invalid_input)


class TestExcepcionesNormalizarOutput:
    """Tests de excepciones para normalizar_output_comando."""
    @pytest.mark.parametrize("invalid_input", [
        None,
        456,
        [],
        {},
        tuple(),
        False
    ])
    def test_tipo_invalido_lanza_excepcion(self, invalid_input):
        """Lanza TypeError con tipos de entrada inválidos."""
        with pytest.raises(TypeError, match="Se requiere una cadena de texto"):
            normalizar_output_comando(invalid_input)


class TestExcepcionesParsearRuta:
    """Tests de excepciones para parsear_ruta_archivo."""
    @pytest.mark.parametrize("invalid_input", [
        None,
        789,
        [],
        {},
        set(),
        True
    ])
    def test_tipo_invalido_lanza_excepcion(self, invalid_input):
        """Lanza TypeError con tipos de entrada inválidos."""
        with pytest.raises(TypeError, match="Se requiere una cadena de texto"):
            parsear_ruta_archivo(invalid_input)


class TestExcepcionesLimpiarNombre:
    """Tests de excepciones para limpiar_nombre_archivo."""
    @pytest.mark.parametrize("invalid_input", [
        None,
        101,
        [],
        {},
        tuple(),
        False
    ])
    def test_tipo_invalido_lanza_excepcion(self, invalid_input):
        """Lanza TypeError con tipos de entrada inválidos."""
        with pytest.raises(TypeError, match="Se requiere una cadena de texto"):
            limpiar_nombre_archivo(invalid_input)


class TestExcepcionesProcesarSalida:
    """Tests de excepciones para procesar_salida_herramienta."""
    @pytest.mark.parametrize("salida,herramienta", [
        # Salida inválida, herramienta válida
        (None, "pytest"),
        (123, "flake8"),
        ([], "terraform"),
        ({}, "tool"),
        (True, "docker"),
        # Salida válida, herramienta inválida
        ("output valido", None),
        ("test output", 456),
        ("resultado", []),
        ("salida", {}),
        ("texto", False),
        # Ambos parámetros inválidos
        (None, None),
        (123, 456),
        ([], {}),
        (True, False)
    ])
    def test_parametros_invalidos_lanzan_excepcion(self, salida, herramienta):
        """Lanza TypeError con cualquier combinación inválida de parámetros."""
        with pytest.raises(TypeError, match="Se requieren cadenas de texto"):
            procesar_salida_herramienta(salida, herramienta)


class TestComportamientosEspeciales:
    """Tests de comportamientos especiales y casos límite."""
    def test_extraer_metricas_con_string_muy_largo(self):
        """Maneja strings extremadamente largos sin problemas."""
        texto_largo = "test " * 10000 + "5 passed"
        resultado = extraer_metricas_de_output(texto_largo)
        assert resultado['tests_passed'] == 5

    def test_parsear_ruta_con_caracteres_especiales(self):
        """Maneja rutas con caracteres especiales."""
        ruta_especial = "src/módulo_ñ/archivo-ñ.py"
        resultado = parsear_ruta_archivo(ruta_especial)
        assert resultado['nombre_archivo'] == "archivo-ñ.py"
        assert resultado['extension'] == ".py"

    def test_limpiar_nombre_solo_caracteres_problematicos(self):
        """Maneja nombres que son solo caracteres problemáticos."""
        nombre_problematico = "<>:\"/\\|?*"
        resultado = limpiar_nombre_archivo(nombre_problematico)
        # No debería quedar algo válido después de la limpieza
        assert len(resultado) == 0
        assert not any(c in resultado for c in '<>:"/\\|?*')

    @pytest.mark.parametrize("string_vacio", ["", "   ", "\t\n"])
    def test_strings_vacios_o_solo_espacios(self, string_vacio):
        """Maneja strings vacíos o solo espacios correctamente."""
        # extraer_metricas_de_output
        metricas = extraer_metricas_de_output(string_vacio)
        assert metricas == {}
        # normalizar_output_comando
        normalizado = normalizar_output_comando(string_vacio)
        assert normalizado == ""
        # parsear_ruta_archivo
        ruta_info = parsear_ruta_archivo(string_vacio.strip() or ".")
        assert isinstance(ruta_info, dict)
        # limpiar_nombre_archivo
        nombre_limpio = limpiar_nombre_archivo(string_vacio)
        assert isinstance(nombre_limpio, str)
        # procesar_salida_herramienta
        resultado = procesar_salida_herramienta(string_vacio, "tool")
        assert resultado['estado'] == 'unknown'

    def test_numeros_muy_grandes_en_metricas(self):
        """Maneja números muy grandes en métricas."""
        texto_grandes = "9999999999 passed, 8888888888 failed"
        metricas = extraer_metricas_de_output(texto_grandes)
        assert metricas['tests_passed'] == 9999999999
        assert metricas['tests_failed'] == 8888888888

    def test_multiples_patrones_en_mismo_texto(self):
        """Extrae múltiples patrones del mismo texto correctamente."""
        texto_complejo = """
        Test suite completed: 50 passed, 5 failed in 120.5 seconds
        Coverage: 85.5% coverage
        Found 3 errors and 7 warnings
        """
        metricas = extraer_metricas_de_output(texto_complejo)
        assert metricas['tests_passed'] == 50
        assert metricas['tests_failed'] == 5
        assert metricas['duration'] == 120.5
        assert metricas['coverage_percent'] == 85.5
        assert metricas['errors'] == 3
        assert metricas['warnings'] == 7
