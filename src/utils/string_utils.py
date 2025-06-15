import re
import os


def extraer_metricas_de_output(texto: str) -> dict:
    """
    Extrae métricas numéricas comunes de outputs de herramientas.
    
    - Parsear outputs de pytest (tests passed/failed/duration)
    - Extraer métricas de cobertura de coverage.xml
    - Procesar outputs de terraform plan (resources to add/change/destroy)
    - Analizar outputs de linters (error count, warning count)
    """
    if not isinstance(texto, str):
        raise TypeError("Se requiere una cadena de texto")
    
    metricas = {}
    
    # Patrones comunes de métricas
    patrones = {
        'tests_passed': r'(\d+)\s*passed',
        'tests_failed': r'(\d+)\s*failed',
        'coverage_percent': r'(\d+(?:\.\d+)?)%?\s*coverage',
        'errors': r'(\d+)\s*errors?',
        'warnings': r'(\d+)\s*warnings?',
        'duration': r'(\d+(?:\.\d+)?)\s*seconds?',
        'lines_total': r'(\d+)\s*lines?',
        'to_add': r'(\d+)\s*to\s*add',
        'to_change': r'(\d+)\s*to\s*change',
        'to_destroy': r'(\d+)\s*to\s*destroy'
    }
    
    for metrica, patron in patrones.items():
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            try:
                valor = float(match.group(1))
                metricas[metrica] = int(valor) if valor.is_integer() else valor
            except ValueError:
                continue
    
    return metricas


def normalizar_output_comando(output: str) -> str:
    """
    Normaliza outputs de comandos shell eliminando ruido común.
    
    - Limpiar outputs de flake8, shellcheck, tflint
    - Procesar outputs de terraform plan/apply
    - Limpiar logs de pytest
    - Preparar texto para dashboard ASCII
    """
    if not isinstance(output, str):
        raise TypeError("Se requiere una cadena de texto")
    
    # Eliminar códigos de color ANSI
    output_limpio = re.sub(r'\x1b\[[0-9;]*m', '', output)
    
    # Normalizar espacios y saltos de línea
    output_limpio = re.sub(r'\s+', ' ', output_limpio)
    
    # Eliminar espacios al inicio y final
    output_limpio = output_limpio.strip()
    
    return output_limpio


def parsear_ruta_archivo(ruta: str) -> dict:
    """
    Parsea una ruta de archivo extrayendo componentes útiles.

    - Procesar rutas de archivos Python para coverage
    - Analizar rutas de archivos Terraform 
    - Categorizar archivos por directorio/módulo
    - Generar rutas relativas para reportes
    """
    if not isinstance(ruta, str):
        raise TypeError("Se requiere una cadena de texto")
    
    # Normalizar la ruta
    ruta_normalizada = os.path.normpath(ruta)
    
    return {
        'ruta_completa': ruta_normalizada,
        'directorio': os.path.dirname(ruta_normalizada),
        'nombre_archivo': os.path.basename(ruta_normalizada),
        'nombre_sin_extension': os.path.splitext(os.path.basename(ruta_normalizada))[0],
        'extension': os.path.splitext(ruta_normalizada)[1],
        'nivel_profundidad': len(ruta_normalizada.split(os.sep)),
        'es_archivo_test': 'test' in ruta_normalizada.lower(),
        'es_archivo_terraform': ruta_normalizada.endswith(('.tf', '.tfvars')),
        'es_archivo_python': ruta_normalizada.endswith('.py')
    }


def limpiar_nombre_archivo(nombre: str) -> str:
    """
    Limpia un nombre de archivo eliminando caracteres problemáticos.
    
    Útil para sanitizar nombres de archivos de logs, reportes y outputs
    de herramientas de infraestructura.
    
    - Nombres de archivos de cobertura generados
    - Sanitizar nombres de módulos Terraform
    - Limpiar nombres de recursos de AWS/cloud
    """
    if not isinstance(nombre, str):
        raise TypeError("Se requiere una cadena de texto")
    
    # Reemplazar caracteres problemáticos con guiones
    nombre_limpio = re.sub(r'[<>:"/\\|?*\s]+', '-', nombre)
    
    # Eliminar guiones al inicio y final
    nombre_limpio = nombre_limpio.strip('-')
    
    # Limitar longitud (útil para sistemas de archivos)
    return nombre_limpio[:100] if len(nombre_limpio) > 100 else nombre_limpio


def procesar_salida_herramienta(salida: str, herramienta: str) -> dict:
    """
    Procesa la salida de herramientas de QA extrayendo métricas y estado.
    
    - Analizar outputs de pytest, flake8, terraform
    - Determinar estado de ejecución (success/error/warning)
    - Extraer archivos mencionados en los outputs
    - Integrar métricas con el sistema de logging
    """
    if not isinstance(salida, str) or not isinstance(herramienta, str):
        raise TypeError("Se requieren cadenas de texto")
    
    herramienta_norm = herramienta.lower().strip()
    
    # Determinar estado básico
    estado = 'unknown'
    if 'error' in salida.lower() or 'failed' in salida.lower():
        estado = 'error'
    elif 'passed' in salida.lower() or 'success' in salida.lower():
        estado = 'success'
    elif 'warning' in salida.lower():
        estado = 'warning'
    
    return {
        'herramienta': herramienta_norm,
        'estado': estado,
        'metricas': extraer_metricas_de_output(salida),
        'salida_limpia': normalizar_output_comando(salida)
    }
