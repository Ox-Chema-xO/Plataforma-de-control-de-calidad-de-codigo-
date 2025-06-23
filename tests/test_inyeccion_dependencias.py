from abc import ABC, abstractmethod
from unittest.mock import Mock
from datetime import datetime


class IGestorArchivos(ABC):
    """
    Interfaz abstracta para operaciones de archivos
    """

    @abstractmethod
    def existe_archivo(self, ruta_archivo: str) -> bool:
        pass

    @abstractmethod
    def leer_archivo(self, ruta_archivo: str) -> str:
        pass

    @abstractmethod
    def escribir_archivo(self, ruta_archivo: str, contenido: str) -> None:
        pass


class IGestorDirectorios(ABC):
    """
    Interfaz abstracta para operaciones de directorios
    """

    @abstractmethod
    def crear_directorio(self) -> None:
        pass


class ReportadorConDI:
    """
    Version del Reportador que usa inyeccion de dependencias para ser testeable
    """

    def __init__(self,
                 gestor_archivos: IGestorArchivos,
                 gestor_directorios: IGestorDirectorios,
                 directorio_salida: str = "./reports"):
        self.gestor_archivos = gestor_archivos
        self.gestor_directorios = gestor_directorios
        self.directorio_salida = directorio_salida

    def generar_reporte_estado(self):
        """
        Metodo identico al Reportador original pero con dependencias inyectadas
        """
        self.gestor_directorios.crear_directorio()

        contenido = "Reporte de estado del sistema\n"
        contenido += f"Fecha: {datetime.now()}\n"

        ruta_flake8 = "logs/flake8.log"
        if self.gestor_archivos.existe_archivo(ruta_flake8):
            contenido += "Flake8:\n"
            contenido += self.gestor_archivos.leer_archivo(ruta_flake8)
            contenido += "\n"
        else:
            contenido += "Flake8: no ejecutado\n"

        ruta_pytest = "logs/pytest.log"
        if self.gestor_archivos.existe_archivo(ruta_pytest):
            contenido += "Pytest: ejecutado correctamente\n"
            contenido += self.gestor_archivos.leer_archivo(ruta_pytest)
            contenido += "\n"
        else:
            contenido += "Pytest: no ejecutado\n"

        ruta_shellcheck = "logs/shellcheck.log"
        if self.gestor_archivos.existe_archivo(ruta_shellcheck):
            contenido += "Shellcheck: ejecutado correctamente\n"
            contenido += self.gestor_archivos.leer_archivo(ruta_shellcheck)
            contenido += "\n"
        else:
            contenido += "Shellcheck: no ejecutado\n"

        ruta_reporte = f"{self.directorio_salida}/reporte_estado.txt"
        self.gestor_archivos.escribir_archivo(ruta_reporte, contenido)
        return ruta_reporte


class TestFlujoReportadorConDI:
    """
    Tests que prueban el flujo del Reportador usando inyeccion de dependencias
    """

    def test_generar_reporte_con_todos_los_logs(self):
        """
        Prueba el flujo cuando existen todos los logs
        flake8, pytest, shellcheck)
        """
        # Arrange
        # Crear mocks de las interfaces
        mock_gestor_archivos = Mock(spec=IGestorArchivos)
        mock_gestor_directorios = Mock(spec=IGestorDirectorios)

        # Simular que todos los logs existen
        mock_gestor_archivos.existe_archivo.return_value = True

        # Simular contenido de cada log
        ruta_flake8 = "logs/flake8.log"
        ruta_pytest = "logs/pytest.log"
        ruta_shellcheck = "logs/shellcheck.log"

        def mock_leer_archivo(ruta):
            if ruta == ruta_flake8:
                return "src/main.py:10:1: E302 expected 2 blank lines"
            elif ruta == ruta_pytest:
                return "(2024-06-22) Tests: 8, Aprobadas: 6, Fallidas: 2"
            elif ruta == ruta_shellcheck:
                return "scripts/deploy.sh:5:1: SC2086 warning"
            return ""

        mock_gestor_archivos.leer_archivo.side_effect = mock_leer_archivo

        # Crear reportador con dependencias inyectadas
        reportador = ReportadorConDI(
            gestor_archivos=mock_gestor_archivos,
            gestor_directorios=mock_gestor_directorios,
            directorio_salida="./reports"
        )

        # Act
        # Ejecutar el metodo principal
        ruta_reporte = reportador.generar_reporte_estado()

        # Assert
        # Verificar flujo completo
        assert ruta_reporte == "./reports/reporte_estado.txt"

        # Verificar que se creo el directorio
        mock_gestor_directorios.crear_directorio.assert_called_once()

        # Verificar que se verifico la existencia de todos los logs
        mock_gestor_archivos.existe_archivo.assert_any_call(ruta_flake8)
        mock_gestor_archivos.existe_archivo.assert_any_call(ruta_pytest)
        mock_gestor_archivos.existe_archivo.assert_any_call(ruta_shellcheck)

        # Verificar que se leyeron todos los logs
        mock_gestor_archivos.leer_archivo.assert_any_call(ruta_flake8)
        mock_gestor_archivos.leer_archivo.assert_any_call(ruta_pytest)
        mock_gestor_archivos.leer_archivo.assert_any_call(ruta_shellcheck)

        # Verificar que se escribio el reporte
        mock_gestor_archivos.escribir_archivo.assert_called_once()
        args = mock_gestor_archivos.escribir_archivo.call_args
        ruta_escrita = args[0][0]
        contenido_reporte = args[0][1]

        assert ruta_escrita == "./reports/reporte_estado.txt"

        # Verificar contenido exacto del reporte
        assert "Reporte de estado del sistema" in contenido_reporte
        assert "Flake8:" in contenido_reporte
        assert "E302 expected 2 blank lines" in contenido_reporte
        assert "Pytest: ejecutado correctamente" in contenido_reporte
        assert "Tests: 8, Aprobadas: 6, Fallidas: 2" in contenido_reporte
        assert "Shellcheck: ejecutado correctamente" in contenido_reporte
        assert "SC2086 warning" in contenido_reporte

    def test_generar_reporte_sin_logs(self):
        """
        Prueba el flujo cuando no existen logs
        """
        # Arrange
        mock_gestor_archivos = Mock(spec=IGestorArchivos)
        mock_gestor_directorios = Mock(spec=IGestorDirectorios)
        mock_gestor_archivos.existe_archivo.return_value = False

        reportador = ReportadorConDI(
            gestor_archivos=mock_gestor_archivos,
            gestor_directorios=mock_gestor_directorios,
            directorio_salida="./reports"
        )

        # Act
        ruta_reporte = reportador.generar_reporte_estado()

        # Assert
        assert ruta_reporte == "./reports/reporte_estado.txt"
        # No debe intentar leer archivos que no existen
        mock_gestor_archivos.leer_archivo.assert_not_called()

        # Verificar contenido del reporte
        args = mock_gestor_archivos.escribir_archivo.call_args
        contenido = args[0][1]

        assert "Flake8: no ejecutado" in contenido
        assert "Pytest: no ejecutado" in contenido
        assert "Shellcheck: no ejecutado" in contenido

    def test_generar_reporte_solo_flake8(self):
        """
        Prueba el flujo cuando solo existe el log de flake8
        """
        # Arrange
        mock_gestor_archivos = Mock(spec=IGestorArchivos)
        mock_gestor_directorios = Mock(spec=IGestorDirectorios)

        ruta_flake8 = "logs/flake8.log"

        def mock_existe_archivo(ruta):
            if ruta == ruta_flake8:
                return True

        mock_gestor_archivos.existe_archivo.side_effect = mock_existe_archivo
        mensaje_error = "E302 expected 2 blank lines"
        mock_gestor_archivos.leer_archivo.return_value = mensaje_error

        reportador = ReportadorConDI(
            gestor_archivos=mock_gestor_archivos,
            gestor_directorios=mock_gestor_directorios,
            directorio_salida="./reports"
        )

        # Act
        ruta_reporte = reportador.generar_reporte_estado()

        # Assert
        assert ruta_reporte == "./reports/reporte_estado.txt"
        # Solo debe leer el archivo que existe
        mock_gestor_archivos.leer_archivo.assert_called_once_with(ruta_flake8)

        args = mock_gestor_archivos.escribir_archivo.call_args
        contenido = args[0][1]

        assert "Flake8:" in contenido
        assert "E302 expected 2 blank lines" in contenido
        assert "Pytest: no ejecutado" in contenido
        assert "Shellcheck: no ejecutado" in contenido

    def test_generar_reporte_solo_pytest_y_shellcheck(self):
        """
        Prueba el flujo cuando existen solo pytest y shellcheck
        """
        # Arrange
        mock_gestor_archivos = Mock(spec=IGestorArchivos)
        mock_gestor_directorios = Mock(spec=IGestorDirectorios)

        ruta_pytest = "logs/pytest.log"
        ruta_shellcheck = "logs/shellcheck.log"

        def mock_existe_archivo(ruta):
            if ruta == ruta_pytest:
                return True
            if ruta == ruta_shellcheck:
                return True

        def mock_leer_archivo(ruta):
            if ruta == ruta_pytest:
                return "(2024-06-22) Tests: 15, Aprobadas: 15, Fallidas: 0"
            elif ruta == ruta_shellcheck:
                return "scripts/deploy.sh:5:1: SC2086 warning"
            return ""

        mock_gestor_archivos.existe_archivo.side_effect = mock_existe_archivo
        mock_gestor_archivos.leer_archivo.side_effect = mock_leer_archivo

        reportador = ReportadorConDI(
            gestor_archivos=mock_gestor_archivos,
            gestor_directorios=mock_gestor_directorios,
            directorio_salida="./reports"
        )

        # Act
        ruta_reporte = reportador.generar_reporte_estado()

        # Assert
        assert ruta_reporte == "./reports/reporte_estado.txt"
        # Debe leer solo los archivos que existen
        mock_gestor_archivos.leer_archivo.assert_any_call(ruta_pytest)
        mock_gestor_archivos.leer_archivo.assert_any_call(ruta_shellcheck)

        args = mock_gestor_archivos.escribir_archivo.call_args
        contenido = args[0][1]

        assert "Flake8: no ejecutado" in contenido
        assert "Pytest: ejecutado correctamente" in contenido
        assert "Tests: 15, Aprobadas: 15, Fallidas: 0" in contenido
        assert "Shellcheck: ejecutado correctamente" in contenido
        assert "scripts/deploy.sh:5:1: SC2086 warning" in contenido
