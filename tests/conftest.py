import pytest
import tempfile
import os
import shutil
import sys


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
