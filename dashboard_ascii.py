import xml.etree.ElementTree as ET
import os
import re


def leer_cobertura_xml():
    """
    Lee el archivo coverage.xml y extrae el porcentaje de cobertura
    """
    try:
        if not os.path.exists("coverage.xml"):
            print("Error: Archivo coverage.xml no encontrado")
            return None

        tree = ET.parse("coverage.xml")
        root = tree.getroot()

        # Buscamos el elemento coverage con atributo line-rate
        coverage_element = root.find(".")
        if coverage_element is not None:
            line_rate = coverage_element.get("line-rate")
            if line_rate:
                # Convertimos de decimal (0.85) a porcentaje (85)
                porcentaje = float(line_rate) * 100
                return round(porcentaje, 1)  # Redondeamos a 1 decimal

        print("Error: No se pudo extraer el porcentaje de cobertura")
        return None

    except Exception as e:
        print(f"Error al leer coverage.xml: {e}")


def generar_barra_ascii(porcentaje, ancho=20):
    """
    Genera una barra de progreso ASCII
    """
    if porcentaje is None:
        return "░" * ancho + " N/A"

    # Calculamos cuantas barritas deben estar llenos
    llenos = int((porcentaje / 100) * ancho)
    vacios = ancho - llenos

    # Creacion de la barra
    barra = "█" * llenos + "░" * vacios

    return f"{barra} {porcentaje}%"


def obtener_estadisticas_pytest():
    """
    Lee estadisticas de tests
    desde pytest_results.log generado por run_tests.sh
    """
    try:
        if not os.path.exists("pytest_results.log"):
            return None, None

        with open("pytest_results.log", "r") as contenido_resultado:
            contenido = contenido_resultado.read()

        lineas = contenido.strip().split("\n")

        # Buscamos la linea que contengan el resumen de pytest
        for linea in lineas:
            linea = linea.strip()
            # Buscamos passed y failed
            # Definimos el patron para "X passed, Y failed"
            patron = r'(?:(\d+)\s+passed)?(?:.*?(\d+)\s+failed)?'
            match = re.search(patron, linea)
            if match and (match.group(1) or match.group(2)):
                passed = int(match.group(1)) if match.group(1) else 0
                failed = int(match.group(2)) if match.group(2) else 0
                return passed, failed

        return None, None

    except Exception as e:
        print(f"Error al leer pytest_results.log: {e}")


def mostrar_dashboard():
    """
    Muestra el dashboard completo en consola
    """
    print("=" * 50)
    print("  DASHBOARD ASCII - REPORTE DE COBERTURA")
    print("=" * 50)
    print()

    # 1. Mostrar cobertura
    porcentaje_cobertura = leer_cobertura_xml()
    barra_cobertura = generar_barra_ascii(porcentaje_cobertura)

    print("COBERTURA DE CODIGO:")
    print(f"   {barra_cobertura}")

    # Indicador de calidad de cobertura
    if porcentaje_cobertura is not None:
        if porcentaje_cobertura >= 85:
            estado = "EXCELENTE"
        elif porcentaje_cobertura >= 70:
            estado = "ACEPTABLE"
        else:
            estado = "MEJORAR"
        print(f"   Estado: {estado}")
    print()

    # 2. Mostrar estadisticas de tests
    passed, failed = obtener_estadisticas_pytest()

    print("RESULTADOS DE TESTS:")
    if passed is not None and failed is not None:
        total = passed + failed
        print(f"   Total ejecutados: {total}")
        print(f"   Pasados: {passed}")
        print(f"   Fallidos: {failed}")

        if failed == 0:
            print("   Estado: TODOS LOS TESTS PASARON")
        else:
            print(f"   Estado: {failed} TESTS FALLARON")
    else:
        print("   Estadisticas no disponibles")
        print("   (Ejecuta run_tests.sh para generar pytest_results.log)")

    print()
    print("=" * 50)


def main():
    mostrar_dashboard()


if __name__ == "__main__":
    main()
