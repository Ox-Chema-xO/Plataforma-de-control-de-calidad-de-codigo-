import pytest
from unittest.mock import patch, Mock
import re
import os
from src.utils.string_utils import (
    extraer_metricas_de_output,
    parsear_ruta_archivo
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
    @patch.object(os, 'sep', '\\')  # windows
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
