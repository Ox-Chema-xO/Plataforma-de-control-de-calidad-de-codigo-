import os
from src.logs.registrador_logs import RegistradorLogs


def test_registrador_logs_crea_directorio_logs(workspace):
    # arrange
    directorio_logs = "./logs"
    registrador = RegistradorLogs()

    # act
    registrador.crear_directorio()

    # assert
    assert os.path.exists(directorio_logs)


def test_registrador_logs_guarda_flake8(workspace):
    # arrange
    archivo_log = "logs/flake8.log"
    registrador = RegistradorLogs()
    linea = "src/helpers/gestor_directorios.py:5:1"
    tipo_error = "E302 expected 2 blank lines"
    salida_flake8 = f"{linea}: {tipo_error}"

    # act
    registrador.registrar_resultados_flake8(salida_flake8)

    # assert
    assert os.path.exists(archivo_log)

    # Verificamos contenido
    with open(archivo_log, 'r') as contenido_archivo_log:
        contenido = contenido_archivo_log.read()
        assert "Flake8:" in contenido
        assert salida_flake8 in contenido


def test_registrar_logs_guardar_pytest(workspace):
    registrador = RegistradorLogs()
    registrador.registrar_resultados_pytest(5, 4, 1)

    assert os.path.exists("./logs/pytest.log")

    with open("./logs/pytest.log", 'r') as contenido_pytest:
        contenido = contenido_pytest.read()
        assert "Tests: 5" in contenido
        assert "Aprobadas: 4" in contenido
        assert "Fallidas: 1" in contenido


def test_registrar_logs_guardar_shellcheck(workspace):
    registrador = RegistradorLogs()
    linea = "In script.sh line 1: echo $1"
    tipo_error = "SC2086: Double quote to prevent globbing and word splitting"
    salida_shellcheck = f"{linea}, {tipo_error}"
    registrador.registrar_resultados_shellcheck(f"{salida_shellcheck}")

    assert os.path.exists("./logs/shellcheck.log")

    with open("./logs/shellcheck.log", 'r') as contenido_shellcheck:
        contenido = contenido_shellcheck.read()
        assert "SC2086" in contenido
