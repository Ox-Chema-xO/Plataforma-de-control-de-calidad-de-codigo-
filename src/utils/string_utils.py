import re
import os


def extraer_metricas_de_output(texto: str) -> dict:
    """
    Extrae métricas numéricas comunes de outputs de herramientas.
    
    Contexto en el proyecto:
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
    
    Contexto en el proyecto:
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
