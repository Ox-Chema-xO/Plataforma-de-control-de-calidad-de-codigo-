import pytest
from unittest.mock import patch, Mock, create_autospec
import re
import os
from src.utils.string_utils import (
    extraer_metricas_de_output,
    parsear_ruta_archivo,
    normalizar_output_comando,
    procesar_salida_herramienta
)


class TestExtraerMetricasConMock:

    @patch.object(re, 'search')
    def test_extraer_metricas_patron_especifico(self, mock_search):
        mock_match = Mock()
        mock_match.group.return_value = "15"
        mock_search.return_value = mock_match
        metricas = extraer_metricas_de_output("15 passed tests")
        assert metricas['tests_passed'] == 15
        assert mock_search.call_count >= 1
        calls = mock_search.call_args_list
        patron_calls = [call[0][0] for call in calls]
        assert any('passed' in patron for patron in patron_calls)


class TestParsearRutaConMock:

    @patch.object(os.path, 'normpath')
    @patch.object(os.path, 'basename')
    @patch.object(os.path, 'dirname')
    @patch.object(os.path, 'splitext')
    def test_parsear_ruta_windows(self, mock_splitext, mock_dirname,
                                  mock_basename, mock_normpath):
        mock_normpath.return_value = "src\\utils\\string_utils.py"
        mock_basename.return_value = "string_utils.py"
        mock_dirname.return_value = "src\\utils"
        mock_splitext.side_effect = [
            ("string_utils", ".py"),
            ("src\\utils\\string_utils", ".py")
        ]
        resultado = parsear_ruta_archivo("src/utils/string_utils.py")
        # verificamos llamadas al os
        mock_normpath.assert_called_once_with("src/utils/string_utils.py")
        mock_basename.assert_called_once()
        mock_dirname.assert_called_once()
        assert resultado['ruta_completa'] == "src\\utils\\string_utils.py"
        assert resultado['nombre_archivo'] == "string_utils.py"
        assert resultado['directorio'] == "src\\utils"

    @patch.object(os.path, 'normpath')
    def test_parsear_ruta_normpath_falla(self, mock_normpath):
        mock_normpath.side_effect = OSError("Fallo parseo de ruta")
        with pytest.raises(OSError):
            parsear_ruta_archivo("/ruta/erronea")
        mock_normpath.assert_called_once()


class TestProcesarSalidaHerramientaConMock:
    def test_procesar_salida_con_autospec(self):
        mock_extraer = create_autospec(extraer_metricas_de_output)
        mock_extraer.return_value = {'warnings': 5}
        mock_normalizar = create_autospec(normalizar_output_comando)
        mock_normalizar.return_value = "clean output"
        with patch('src.utils.string_utils.extraer_metricas_de_output',
                   new=mock_extraer):
            with patch('src.utils.string_utils.normalizar_output_comando',
                       new=mock_normalizar):
                resultado = procesar_salida_herramienta("5 warnings found",
                                                        "flake8")
                assert resultado['herramienta'] == 'flake8'
                assert resultado['estado'] == 'warning'
                assert resultado['metricas'] == {'warnings': 5}
                assert resultado['salida_limpia'] == "clean output"


class TestConSkip:

    @pytest.mark.skip(reason="Aun no se extrae metricas en formato xml")
    def test_extraer_metricas_formato_xml(self):
        xml_output = "<package name=utils line-rate=0.9709>"
        resultado = extraer_metricas_de_output(xml_output)
        assert resultado['coverage_percent'] == "97.09%"

    @pytest.mark.skipif(
        os.getenv('CI_ENVIRONMENT') != 'production',
        reason="Solo se ejecuta en entorno de produccion"
    )
    def test_procesar_logs_produccion(self):
        log_prod = "700 requests processed, 3 errors, 41.2 seconds"
        resultado = extraer_metricas_de_output(log_prod)
        assert resultado['errors'] == 3
        assert resultado['duration'] == 41.2


class TestConXFail:
    @pytest.mark.xfail(reason="Aun no se parsean multiples rutas agrupadas")
    def test_parsear_multiples_rutas_agrupadas(self):
        rutas_proyecto = [
            "src/utils/string_utils.py",
            "src/utils/list_utils.py",
            "tests/test_string_utils.py",
            "tests/test_list_utils.py",
            "iac/main.tf",
            "iac/variables.tf"
        ]
        resultado = parsear_ruta_archivo(
            rutas_proyecto,
            criterios=['directorio_raiz', 'tipo_archivo', 'es_test']
        )
        assert 'src' in resultado
        assert 'python' in resultado['src']
        assert 'no_test' in resultado['src']['python']
        assert len(resultado['src']['python']['no_test']) == 2
