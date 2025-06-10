import os
import pytest
from src.helpers.gestor_directorios import GestorDirectorios

def test_gestor_directorios_crea_directorio():
    #arrange
    gestorDirectorios = GestorDirectorios("./reporting")

    #act
    gestorDirectorios.crear_directorio()

    #assert
    assert os.path.exists("./reporting")

    #limpiamos
    os.rmdir("./reporting")

def test_gestor_directorios_crea_directorio_cadena_vacia():
    #arrange
    gestorDirectorios = GestorDirectorios("")

    #act y assert
    with pytest.raises(FileNotFoundError):
        gestorDirectorios.crear_directorio()
