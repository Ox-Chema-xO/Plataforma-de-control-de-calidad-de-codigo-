import pytest
import src.utils.list_utils as list_utils
from unittest.mock import patch
import re


def test_aplanar_lista_con_none():
    lista = None
    with pytest.raises(TypeError):
        list_utils.aplanar_lista(lista)


def test_separar_lista_con_none():
    archivos = ["list_utils.py", "test_list_utils.py",
                "variables.tf", "setup.sh"]
    condicion_invalida = None
    with pytest.raises(TypeError):
        list_utils.separar_lista(archivos, condicion_invalida)


def test_agrupar_por_extension_con_lista_invalida():
    with pytest.raises(ValueError):
        list_utils.agrupar_por_extension(["lists.py", 738, None])


def test_eliminar_duplicados_con_lista_archivos_anidados():
    with pytest.raises(ValueError):
        list_utils.eliminar_duplicados(["module/compute/main.tf",
                                        ["module/dev/main.tf"]])


def test_filtrar_por_patron_con_lista_invalida():
    with pytest.raises(ValueError):
        list_utils.filtrar_por_patron(["main.tf", 738, None], r"\.tf$")


def test_ordenar_por_criterio_lista_invalida():
    with pytest.raises(ValueError):
        list_utils.ordenar_por_criterio("test_unit", "test_integration",
                                        lambda t: t)


def test_filtrar_por_patron_invalido():
    with patch.object(re, 'compile') as mock_re_compile:
        mock_re_compile.side_effect = re.error("Patron invalido")
        archivos = ["main.tf", "variables.tf", "setup.sh"]
        with pytest.raises(re.error):
            list_utils.filtrar_por_patron(archivos, r"m[in")
