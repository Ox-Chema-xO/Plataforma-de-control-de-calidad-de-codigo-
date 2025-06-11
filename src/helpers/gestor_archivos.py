import os


class GestorArchivos:
    """
    Clase basica para el manejo de archivos
    crear, escribir, leer y verificar si existe un archivo
    """
    def __init__(self):
        pass

    def crear_archivo(self, ruta_archivo):
        """
        Crea un archivo
        """
        with open(ruta_archivo, 'x'):
            pass

    def escribir_archivo(self, ruta_archivo, contenido):
        """
        Escribe contenido en un archivo
        """
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(contenido)

    def leer_archivo(self, ruta_archivo):
        """
        Lee el contenido de un archivo
        """
        with open(ruta_archivo, 'r') as archivo:
            return archivo.read()

    def existe_archivo(self, ruta_archivo):
        """
        Verifica si existe un archivo,
        devuelve True si existe el archivo y
        False si no existe el archivo
        """
        return os.path.exists(ruta_archivo)
