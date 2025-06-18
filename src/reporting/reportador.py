from datetime import datetime
from src.helpers.gestor_directorios import GestorDirectorios
from src.helpers.gestor_archivos import GestorArchivos


class Reportador(GestorDirectorios):
    """
    Genera reportes leyendo los logs
    """

    def __init__(self):
        """
        Inicializa el reportador en ./reports/
        """
        super().__init__(directorio_salida="./reports")
        self.gestor_archivos = GestorArchivos()

    def generar_reporte_estado(self):
        """
        Crea reporte leyendo los logs disponibles
        """
        self.crear_directorio()

        contenido = "Reporte de estado del sistema\n"
        contenido += f"Fecha: {datetime.now()}\n"

        # Lee flake8 y escribe en el reporte
        ruta_flake8 = "logs/flake8.log"
        if self.gestor_archivos.existe_archivo(ruta_flake8):
            contenido += "Flake8:\n"
            contenido += self.gestor_archivos.leer_archivo(ruta_flake8)
            contenido += "\n"
        else:
            contenido += "Flake8: no ejecutado\n"

        # Lee pytest y escribe en el reporte
        ruta_pytest = "logs/pytest.log"
        if self.gestor_archivos.existe_archivo(ruta_pytest):
            contenido += "Pytest: ejecutado correctamente\n"
            contenido += self.gestor_archivos.leer_archivo(ruta_pytest)
            contenido += "\n"
        else:
            contenido += "Pytest: no ejecutado\n"

        # Lee shellcheck y escribe en el reporte
        ruta_shellcheck = "logs/shellcheck.log"
        if self.gestor_archivos.existe_archivo(ruta_shellcheck):
            contenido += "Shellcheck: ejecutado correctamente\n"
            contenido += self.gestor_archivos.leer_archivo(ruta_shellcheck)
            contenido += "\n"
        else:
            contenido += "Shellcheck: no ejecutado\n"

        # Guarda reporte
        ruta_reporte = f"{self.directorio_salida}/reporte_estado.txt"
        self.gestor_archivos.escribir_archivo(ruta_reporte, contenido)
        return ruta_reporte
