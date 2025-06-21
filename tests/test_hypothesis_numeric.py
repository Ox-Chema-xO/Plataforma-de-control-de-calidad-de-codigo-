from hypothesis import given, strategies as st, assume


def calcular_cobertura_combinada(lineas_cubiertas: int, lineas_totales: int,
                                 peso_actual: float = 0.7):
    """
    Se calcula la cobertura teniendo en cuenta no solo el control
    de calidad de codigo actual, sino tambien de una version anterior
    El porcentaje de cobertura siempre debe estar entre 0 y 100
    """
    if lineas_totales <= 0:
        return 0.0
    if lineas_cubiertas > lineas_totales:
        lineas_cubiertas = lineas_totales
    cobertura_actual = (lineas_cubiertas / lineas_totales) * 100
    cobertura_historica = max(0, cobertura_actual - 10)
    cobertura_combinada = (cobertura_actual * peso_actual +
                           cobertura_historica * (1 - peso_actual))
    return round(cobertura_combinada, 2)


class TestCalcularCoberturaInvariante:
    @given(
        lineas_cubiertas=st.integers(min_value=0, max_value=10000),
        lineas_totales=st.integers(min_value=1, max_value=10000),
        peso=st.floats(min_value=0.0, max_value=1.0)
    )
    def test_cobertura_entre_0_y_100(self, lineas_cubiertas,
                                     lineas_totales, peso):
        cobertura = calcular_cobertura_combinada(lineas_cubiertas,
                                                 lineas_totales, peso)
        assert 0.0 <= cobertura <= 100.0

    @given(
        lineas_totales=st.integers(min_value=1, max_value=1000),
        peso=st.floats(min_value=0.0, max_value=1.0)
    )
    def test_cobertura_completa(self, lineas_totales, peso):
        cobertura = calcular_cobertura_combinada(lineas_totales,
                                                 lineas_totales, peso)
        assert cobertura >= 90.0

    @given(
        lineas_totales=st.integers(min_value=1, max_value=1000),
        peso=st.floats(min_value=0.0, max_value=1.0)
    )
    def test_sin_cobertura(self, lineas_totales, peso):
        cobertura = calcular_cobertura_combinada(0, lineas_totales, peso)
        assert cobertura <= 10.0

    @given(
        lineas_cubiertas=st.integers(min_value=0, max_value=1000),
        lineas_totales=st.integers(min_value=1, max_value=1000),
        peso1=st.floats(min_value=0.0, max_value=1.0),
        peso2=st.floats(min_value=0.0, max_value=1.0)
    )
    def test_monotonia_peso(self, lineas_cubiertas, lineas_totales,
                            peso1, peso2):
        assume(abs(peso1 - peso2) > 0.01)
        cobertura_c1 = calcular_cobertura_combinada(lineas_cubiertas,
                                                    lineas_totales, peso1)
        cobertura_c2 = calcular_cobertura_combinada(lineas_cubiertas,
                                                    lineas_totales, peso2)
        cobertura = (lineas_cubiertas / lineas_totales) * 100
        distancia1 = abs(cobertura_c1 - cobertura)
        distancia2 = abs(cobertura_c2 - cobertura)
        if peso1 > peso2:
            assert distancia1 <= distancia2 + 0.0001
        elif peso1 < peso2:
            assert distancia2 <= distancia1 + 0.0001
