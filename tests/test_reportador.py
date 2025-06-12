import os
import pytest
from src.logs.registrador_logs import RegistradorLogs
from src.reporting.reportador import Reportador


def test_reporte_formato_correcto_sin_logs():
    # arrange
    reportador = Reportador()

    # act
    ruta = reportador.generar_reporte_estado()
    with open(ruta, 'r') as contenido:
        lineas = contenido.readlines()

    # assert
    assert lineas[0].strip() == "Reporte de estado del sistema"
    assert "Flake8: no ejecutado" in ''.join(lineas)
    assert "Pytest: no ejecutado" in ''.join(lineas)
    assert "Shellcheck: no ejecutado" in ''.join(lineas)

    # limpiamos
    os.remove("reports/reporte_estado.txt")
    os.rmdir("./reports")


def test_reporte_incluye_contenido_completo_logs():
    # arrange
    registrador = RegistradorLogs()
    registrador.registrar_resultados_flake8("Error en linea 21: unused import")
    registrador.registrar_resultados_pytest(8, 6, 2)
    registrador.registrar_resultados_shellcheck("Warning: variable no usada")

    gestor_archivos = registrador.gestor_archivos
    ruta_flake8 = "logs/flake8.log"
    ruta_pytest = "logs/pytest.log"
    ruta_shellcheck = "logs/shellcheck.log"
    contenido_flake8 = gestor_archivos.leer_archivo(ruta_flake8)
    contenido_pytest = gestor_archivos.leer_archivo(ruta_pytest)
    contenido_shellcheck = gestor_archivos.leer_archivo(ruta_shellcheck)

    # act
    reportador = Reportador()
    ruta = reportador.generar_reporte_estado()

    with open(ruta, 'r') as contenido:
        contenido_reporte = contenido.read()

    # assert
    assert contenido_flake8 in contenido_reporte
    assert contenido_pytest in contenido_reporte
    assert contenido_shellcheck in contenido_reporte

    # limpiamos
    for archivo in [ruta_flake8, ruta_pytest, ruta_shellcheck]:
        os.remove(archivo)

    os.rmdir("./logs")
    os.remove("reports/reporte_estado.txt")
    os.rmdir("./reports")


def test_fallo_archivo_reporte_es_directorio():
    # arrange
    reportador = Reportador()
    os.makedirs("./reports/reporte_estado.txt")

    # act y assert
    with pytest.raises(IsADirectoryError):
        reportador.generar_reporte_estado()

    # limpiamos
    os.rmdir("./reports/reporte_estado.txt")
    os.rmdir("./reports")


def test_fallo_log_es_directorio():
    # arrange
    reportador = Reportador()
    os.makedirs("logs/flake8.log")

    # act y assert
    with pytest.raises(IsADirectoryError):
        reportador.generar_reporte_estado()

    # limpiamos
    os.rmdir("./logs/flake8.log")
    os.rmdir("./logs")
    os.rmdir("./reports")
