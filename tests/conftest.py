import pytest
import tempfile
import os
import shutil
import sys
import random


@pytest.fixture(scope="session")
def entorno_temporal():
    """
    Fixture global que crea un entorno temporal donde
    realizar pruebas que requieran trabajar con un entorno limpio
    para gestionar archivos, configuraciones, entre otros
    """
    directorio_proyecto = os.getcwd()
    directorio_temporal = tempfile.mkdtemp(prefix="tests_qa_")
    print(f"\nRuta proyecto: {directorio_proyecto}")
    print(f"\nEntorno temporal: {directorio_temporal}")

    if directorio_proyecto not in sys.path:
        sys.path.insert(0, directorio_proyecto)
    try:
        yield directorio_temporal, directorio_proyecto
    finally:
        print("\nLimpiando entorno temporal")
        shutil.rmtree(directorio_temporal, ignore_errors=True)


@pytest.fixture(scope="function")
def workspace(entorno_temporal):
    """
    Fixture que se encarga de que cada test use el entorno temporal
    """
    directorio_temporal, directorio_proyecto = entorno_temporal
    try:
        os.chdir(directorio_temporal)
        yield directorio_temporal
    finally:
        os.chdir(directorio_proyecto)


@pytest.fixture(scope="module")
def datos_compartidos_modulo():
    """
    Datos compartidos para todos los tests en un modulo
    """
    datos = {
        "cadenas_prueba": ["hola", "mundo", "python", "testing"],
        "numeros_prueba": [1, 2, 3, 4, 5]
    }
    yield datos


@pytest.fixture(scope="function")
def datos_inicializados():
    """
    Datos inicializados para cada test individual
    """
    datos = {
        "elementos": [],
        "contador": 0,
        "estado": "listo"
    }
    yield datos


@pytest.fixture
def archivo_factory():
    """
    Se encarga de generar nombre de archivos aleatorios
    """
    def _crear_archivo(extension=".py", prefijo="test", es_test=None):
        numero = random.randint(1000, 10000)
        if es_test is None:
            es_test = random.choice([True, False])
        if es_test:
            nombre_archivo = f"{prefijo}_archivo_{numero}{extension}"
        else:
            nombre_archivo = f"archivo_{numero}{extension}"
        return nombre_archivo
    return _crear_archivo


@pytest.fixture
def metricas_factory():
    """
    Se encarga de simular outputs de herramientas
    como pytest, flake8, terraform, coverage
    """
    def _crear_metricas(herramienta="pytest", estado="normal"):
        base_metricas = {
            "pytest": {
                "tests_passed": random.randint(10, 100),
                "tests_failed": random.randint(0, 5),
                "duration": round(random.uniform(6.0, 120.0), 2)
            },
            "flake8": {
                "errors": random.randint(0, 10),
                "warnings": random.randint(5, 20),
                "lines_total": random.randint(400, 4000)
            },
            "terraform": {
                "to_add": random.randint(0, 7),
                "to_change": random.randint(0, 5),
                "to_destroy": random.randint(0, 3)
            },
            "coverage": {
                "coverage_percent": round(random.uniform(70.0, 95.0), 1),
                "lines_total": random.randint(1000, 10000)
            }
        }
        metricas = base_metricas.get(herramienta, {})
        if estado == "error" and herramienta == "pytest":
            metricas["tests_failed"] = max(1, metricas["tests_failed"])
        elif estado == "error" and herramienta == "flake8":
            metricas["errors"] = max(1, metricas["errors"])
        return metricas
    return _crear_metricas
