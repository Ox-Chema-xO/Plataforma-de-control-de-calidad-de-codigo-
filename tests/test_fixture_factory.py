def test_archivo_factory(archivo_factory):
    archivo_tf = archivo_factory(extension=".tf", es_test=False)
    archivos = [archivo_factory() for _ in range(5)]
    assert not archivo_tf.startswith("test_")
    assert archivo_tf.endswith(".tf")
    assert len(set(archivos)) == 5


def test_metricas_factory(metricas_factory):
    metricas_normal = metricas_factory("pytest", "normal")
    metricas_error = metricas_factory("pytest", "error")
    assert metricas_normal["tests_failed"] >= 0
    assert metricas_normal["tests_passed"] > 0
    assert metricas_normal["duration"] > 0
    assert metricas_error["tests_failed"] > 0


def test_proyecto_factory(proyecto_factory):
    proyecto_py = proyecto_factory("trivia_game", "python")
    proyecto_tf = proyecto_factory("infraestructura_local", "terraform")
    assert len(proyecto_py.archivos_python) == 3
    assert len(proyecto_py.archivos_tests) == len(proyecto_py.archivos_python)
    assert "src/" in proyecto_py.estructura_directorios
    assert "tests/" in proyecto_py.estructura_directorios
    assert "iac/modules/" in proyecto_tf.estructura_directorios
