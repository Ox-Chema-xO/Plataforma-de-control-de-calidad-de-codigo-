import hcl2
import pytest

from src.utils.list_utils import aplanar_lista
from src.helpers.gestor_archivos import GestorArchivos


"""Tests para validar las variables definidas en iac/variables.tf"""


@pytest.fixture(scope="function")
def variables_dict():
    """Setup para cada test - inicializar gestor de archivos"""
    ruta_variables = "iac/variables.tf"
    gestor_archivos = GestorArchivos()
    # Verificar que el archivo de variables existe
    assert gestor_archivos.existe_archivo(ruta_variables)
    with open(ruta_variables, 'r') as file:
        terraform_config = hcl2.load(file)
    # Verificar que la configuración de Terraform se cargó correctamente
    assert "variable" in terraform_config
    # Aplanar la lista de variables para facilitar el acceso
    variables_dict = {}
    variables_aplanadas = aplanar_lista(terraform_config["variable"])
    for var_item in variables_aplanadas:
        if isinstance(var_item, dict):
            for var_name, var_config in var_item.items():
                variables_dict[var_name] = var_config
    return variables_dict


@pytest.fixture(scope="function")
def required_vars():
    """Variables requeridas para los tests"""
    return ["environment", "project_name", "enable_debug"]


def test_variables_exist(variables_dict, required_vars):
    """Verifica que existan las variables requeridas en variables.tf"""
    # Verificar que existan las variables específicas
    for var_name in required_vars:
        assert var_name in variables_dict


def test_variables_types(variables_dict):
    """Verifica que las variables tengan los tipos correctos"""
    # Verificar tipos de variables
    expected_types = {
        "environment": "string",
        "project_name": "string",
        "enable_debug": "bool"
    }
    for var_name, expected_type in expected_types.items():
        assert var_name in variables_dict
        assert "type" in variables_dict[var_name]
        actual_type = variables_dict[var_name]["type"]
        assert actual_type == expected_type


def test_variables_defaults(variables_dict, required_vars):
    """Verifica que las variables tengan valores predeterminados"""
    for var_name in required_vars:
        assert var_name in variables_dict
        assert "default" in variables_dict[var_name]
        default_value = variables_dict[var_name]["default"]
        assert default_value or isinstance(default_value, bool)


def test_variables_descriptions(variables_dict, required_vars):
    """Verifica que todas las variables tengan descripciones"""
    for var_name in required_vars:
        assert var_name in variables_dict
        assert "description" in variables_dict[var_name]
        description = variables_dict[var_name]["description"]
        assert description.strip()
