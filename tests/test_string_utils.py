import pytest
from src.utils.string_utils import (
    extraer_metricas_de_output,
    normalizar_output_comando,
    parsear_ruta_archivo,
    limpiar_nombre_archivo,
    procesar_salida_herramienta
)


class TestExtraerMetricasDeOutput:
    """Tests para extracción de métricas de outputs de herramientas."""
    
    @pytest.mark.parametrize("output,expected", [
        ("===== 15 passed, 2 failed in 3.45 seconds =====", {
            'tests_passed': 15, 
            'tests_failed': 2, 
            'duration': 3.45
        }),
        ("Total coverage: 85.5% coverage", {
            'coverage_percent': 85.5
        }),
        ("Found 7 errors and 12 warnings in your code", {
            'errors': 7,
            'warnings': 12
        }),
        ("Plan: 5 to add, 2 to change, 1 to destroy", {
            'to_add': 5,
            'to_change': 2,
            'to_destroy': 1
        }),
        ("Este texto no contiene métricas numéricas", {}),
        ("Process completed with 100 lines total", {
            'lines_total': 100
        }),
        ("Test duration: 45.8 seconds with 0 errors", {
            'duration': 45.8,
            'errors': 0
        })
    ])
    def test_extrae_metricas_correctamente(self, output, expected):
        """Extrae métricas de diferentes tipos de outputs."""
        resultado = extraer_metricas_de_output(output)
        
        for key, value in expected.items():
            assert resultado[key] == value


class TestNormalizarOutputComando:
    """Tests para normalización de outputs de comandos."""
    
    @pytest.mark.parametrize("input_text,expected", [
        ("\x1b[32mSUCCESS\x1b[0m: All tests passed", "SUCCESS: All tests passed"),
        ("Multiple    spaces\n\nand   \t  tabs", "Multiple spaces and tabs"),
        ("   texto con espacios   ", "texto con espacios"),
        ("", ""),
        ("   \n\t  ", ""),
        ("Normal text without changes", "Normal text without changes"),
        ("\x1b[91mERROR\x1b[0m\n\n   Multiple   issues   ", "ERROR Multiple issues")
    ])
    def test_normaliza_output_correctamente(self, input_text, expected):
        """Normaliza diferentes tipos de outputs correctamente."""
        resultado = normalizar_output_comando(input_text)
        assert resultado == expected
        
        # Verificar que no quedan códigos ANSI
        assert '\x1b' not in resultado


class TestParsearRutaArchivo:
    """Tests para parseo de rutas de archivos."""
    
    @pytest.mark.parametrize("ruta,expected_fields", [
        ("src/utils/string_utils.py", {
            'nombre_archivo': 'string_utils.py',
            'nombre_sin_extension': 'string_utils',
            'extension': '.py',
            'directorio': 'src/utils',
            'es_archivo_python': True,
            'es_archivo_terraform': False,
            'es_archivo_test': False,
            'nivel_profundidad': 3
        }),
        ("iac/main.tf", {
            'nombre_archivo': 'main.tf',
            'extension': '.tf',
            'es_archivo_terraform': True,
            'es_archivo_python': False,
            'es_archivo_test': False
        }),
        ("tests/test_string_utils.py", {
            'es_archivo_test': True,
            'es_archivo_python': True,
            'nombre_sin_extension': 'test_string_utils'
        }),
        ("scripts/setup", {
            'extension': '',
            'nombre_sin_extension': 'setup',
            'nombre_archivo': 'setup'
        }),
        ("src/utils/helpers/modulo.py", {
            'nivel_profundidad': 4,
            'es_archivo_python': True
        })
    ])
    def test_parsea_rutas_correctamente(self, ruta, expected_fields):
        """Parsea diferentes tipos de rutas correctamente."""
        resultado = parsear_ruta_archivo(ruta)
        
        for field, expected_value in expected_fields.items():
            assert resultado[field] == expected_value, f"Campo {field} no coincide"


class TestLimpiarNombreArchivo:
    """Tests para limpieza de nombres de archivos."""
    
    @pytest.mark.parametrize("nombre,expected", [
        ("archivo<con>caracteres:problemáticos", "archivo-con-caracteres-problemáticos"),
        ("archivo con espacios múltiples", "archivo-con-espacios-múltiples"),
        ("---archivo-con-guiones---", "archivo-con-guiones"),
        ("archivo_valido.txt", "archivo_valido.txt"),
        ("file/with\\slashes|and*wildcards", "file-with-slashes-and-wildcards"),
        ("archivo???con???caracteres", "archivo-con-caracteres")
    ])
    def test_limpia_nombres_correctamente(self, nombre, expected):
        """Limpia diferentes tipos de nombres problemáticos."""
        resultado = limpiar_nombre_archivo(nombre)
        assert resultado == expected
        
        # Verificar que no quedan caracteres problemáticos
        caracteres_problematicos = '<>:"/\\|?*'
        assert not any(c in resultado for c in caracteres_problematicos)
    
    def test_limita_longitud_maxima(self):
        """Limita longitud a 100 caracteres."""
        nombre = "a" * 150
        resultado = limpiar_nombre_archivo(nombre)
        
        assert len(resultado) == 100
        assert resultado == "a" * 100


class TestProcesarSalidaHerramienta:
    """Tests para procesamiento de salidas de herramientas."""
    
    @pytest.mark.parametrize("salida,herramienta,expected_estado,expected_metricas", [
        ("===== 10 passed in 2.5 seconds =====", "pytest", "success", {
            'tests_passed': 10, 
            'duration': 2.5
        }),
        ("===== 5 passed, 3 failed =====", "PYTEST", "error", {
            'tests_passed': 5,
            'tests_failed': 3
        }),
        ("Found 5 warnings in your code", "flake8", "warning", {
            'warnings': 5
        }),
        ("Build completed successfully", "docker", "success", {}),
        ("Terraform apply failed with errors", "terraform", "error", {}),
        ("Output sin indicadores claros de estado", "tool", "unknown", {})
    ])
    def test_procesa_diferentes_outputs(self, salida, herramienta, expected_estado, expected_metricas):
        """Procesa outputs de diferentes herramientas correctamente."""
        resultado = procesar_salida_herramienta(salida, herramienta)
        
        assert resultado['herramienta'] == herramienta.lower().strip()
        assert resultado['estado'] == expected_estado
        
        # Verificar métricas específicas
        for key, value in expected_metricas.items():
            assert resultado['metricas'][key] == value
    
    def test_incluye_salida_limpia_ansi(self):
        """Incluye salida limpia sin códigos ANSI."""
        salida = "\x1b[32mSUCCESS\x1b[0m"
        resultado = procesar_salida_herramienta(salida, "tool")
        
        assert resultado['salida_limpia'] == "SUCCESS"
        assert '\x1b' not in resultado['salida_limpia']
    
    def test_estructura_resultado_completa(self):
        """Verifica que el resultado tenga la estructura completa."""
        resultado = procesar_salida_herramienta("test output", "pytest")
        
        required_keys = ['herramienta', 'estado', 'metricas', 'salida_limpia']
        for key in required_keys:
            assert key in resultado, f"Falta la clave {key} en el resultado"
