from datetime import datetime
from src.helpers.gestor_directorios import GestorDirectorios
from src.helpers.gestor_archivos import GestorArchivos


class RegistradorLogs(GestorDirectorios):
    """
    Clase que se encargara de registrar
    los resultados obtenidos de flake8, pytest y shellcheck
    """

    def __init__(self):
        """
        Inicializa el registrador para guardar nuestros logs en ./logs/
        """
        super().__init__(directorio_salida="./logs")
        self.gestor_archivos = GestorArchivos()

    def registrar_resultados_flake8(self, salida_flake8):
        """
        Guarda el resultados obtenido
        de flake8 con el dia y hora que se realizo
        """
        self.crear_directorio()
        ruta_log = f"{self.directorio_salida}/flake8.log"
        contenido = f"[{datetime.now()}] Flake8: {salida_flake8}"
        self.gestor_archivos.escribir_archivo(ruta_log, contenido)

    def registrar_resultados_pytest(self, total_pruebas, aprobadas, fallidas):
        """
        Guarda el resultado obtenido
        de pytest con el dia y hora que se realizo
        """
        self.crear_directorio()
        ruta_log = f"{self.directorio_salida}/pytest.log"
        total_pruebas = f"Tests: {total_pruebas}"
        cantidad_aprobados = f"Aprobadas: {aprobadas}"
        cantidad_fallidos = f"Fallidas: {fallidas}"
        resultado = f"{total_pruebas},{cantidad_aprobados},{cantidad_fallidos}"
        contenido = f"({datetime.now()}) {resultado}"
        self.gestor_archivos.escribir_archivo(ruta_log, contenido)

    def registrar_resultados_shellcheck(self, salida_shellcheck):
        """
        Guarda el resultado obtenido de
        shellcheck con el dia y hora que se realizo
        """
        self.crear_directorio()
        ruta_log = f"{self.directorio_salida}/shellcheck.log"
        contenido = f"[{datetime.now()}] Shellcheck: {salida_shellcheck}"
        self.gestor_archivos.escribir_archivo(ruta_log, contenido)
