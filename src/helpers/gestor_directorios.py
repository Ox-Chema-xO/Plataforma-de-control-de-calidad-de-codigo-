import os

class GestorDirectorios:
    """
    Clase base que creara directorios
    """
    def __init__(self, directorio_salida):
        """
        Constructor que inicializara la ruta donde se creara el directorio
        """
        self.directorio_salida = directorio_salida

    def crear_directorio(self):
        """
        Crea el directorio si todavia no existe
        """
        os.makedirs(self.directorio_salida, exist_ok=True)
