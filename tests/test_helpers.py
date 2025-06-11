import os
import pytest
from src.helpers.gestor_directorios import GestorDirectorios
from src.helpers.gestor_archivos import GestorArchivos


def test_gestor_directorios_crea_directorio():
    # arrange
    gestorDirectorios = GestorDirectorios("./reporting")

    # act
    gestorDirectorios.crear_directorio()

    # assert
    assert os.path.exists("./reporting")

    # limpiamos
    os.rmdir("./reporting")


def test_gestor_directorios_crea_directorio_cadena_vacia():
    # arrange
    gestorDirectorios = GestorDirectorios("")

    # act y assert
    with pytest.raises(FileNotFoundError):
        gestorDirectorios.crear_directorio()


def test_gestor_archivos_escribir_archivo():
    # arrange
    gestorArchivos = GestorArchivos()

    # act
    gestorArchivos.escribir_archivo("texto.txt", "Este es un texto de prueba")
    contenido = gestorArchivos.leer_archivo("texto.txt")

    # assert
    assert contenido == "Este es un texto de prueba"

    # limpiamos
    os.remove("texto.txt")


def test_gestor_archivos_escribir_archivo_ruta_carpeta_vacia():
    # arrange
    gestorArchivos = GestorArchivos()

    # act y assert
    with pytest.raises(FileNotFoundError):
        gestorArchivos.escribir_archivo("", "Este es un texto de prueba")


def test_gestor_archivos_crear_archivo_exitoso():
    # arrange
    gestorArchivos = GestorArchivos()

    # act
    gestorArchivos.crear_archivo("texto.txt")

    # assert
    assert gestorArchivos.existe_archivo("texto.txt")  # True

    # limpiamos
    os.remove("texto.txt")


def test_gestor_archivos_crear_archivo_fallido():
    # arrange
    gestorArchivos = GestorArchivos()
    gestorArchivos.crear_archivo("texto.txt")

    # act y arrange
    with pytest.raises(FileExistsError):
        gestorArchivos.crear_archivo("texto.txt")


def test_gestor_archivos_leer_archivos_exitoso():
    # arrange
    gestorArchivos = GestorArchivos()
    contenido = "hola, este es un contenido de prueba"
    gestorArchivos.escribir_archivo("texto.txt", contenido)

    # act y assert
    assert gestorArchivos.leer_archivo("texto.txt") == contenido

    # limpiamos
    os.remove("texto.txt")


def test_gestor_archivos_leer_archivos_fallido():
    # arrange
    gestorArchivos = GestorArchivos()

    # act y assert
    with pytest.raises(FileNotFoundError):
        gestorArchivos.leer_archivo("texto.txt")


def test_gestor_archivos_existe_archivo_verdadero():
    # arrange
    gestorArchivos = GestorArchivos()
    gestorArchivos.crear_archivo("texto.txt")

    # act y assert
    assert gestorArchivos.existe_archivo("texto.txt")  # True

    # limpiamos
    os.remove("texto.txt")


def test_gestor_archivos_existe_archivo_falso():
    # arrange
    gestorArchivos = GestorArchivos()

    # act y assert
    assert not gestorArchivos.existe_archivo("texto.txt")  # False
