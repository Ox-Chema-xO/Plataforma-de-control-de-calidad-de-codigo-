import pytest
from src.utils.list_utils import aplanar_lista
from src.utils.list_utils import separar_lista
from src.utils.list_utils import agrupar_por_extension

def test_aplanar_lista_con_none():
    lista = None
    with pytest.raises(TypeError):
        aplanar_lista(lista)

def test_separar_lista_con_none():
    archivos = ["list_utils.py","test_list_utils.py","variables.tf","setup.sh"]
    condicion_invalida = None
    with pytest.raises(TypeError):
        separar_lista(archivos, condicion_invalida)

def test_agrupar_por_extension_con_lista_invalida():
    with pytest.raises(ValueError):
        agrupar_por_extension(["lists.py", 738, None])