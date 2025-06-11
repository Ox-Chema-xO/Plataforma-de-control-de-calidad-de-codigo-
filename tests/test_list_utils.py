import src.utils.list_utils as list_utils


def test_aplanar_lista_basica():
    lista = [5, [10, 15], [20, [25, 30]], 35]
    lista_aplanada = list_utils.aplanar_lista(lista)
    assert lista_aplanada == [5, 10, 15, 20, 25, 30, 35]
    assert len(lista_aplanada) == 7


def test_aplanar_lista_de_pruebas():
    test_results = [
        [
            {"test_unit": "test_aplanar_lista_basica", "status": "passed"},
            {"test_unit": "test_aplanar_lista_files_tf", "status": "passed"}
        ],
        [
            {"test_integration": "test_module_network", "status": "passed"},
            {"test_integration": "test_module_compute", "status": "failed"}
        ]
    ]

    test_results_plana = list_utils.aplanar_lista(test_results)
    test_esperado_results_plana = [
        {"test_unit": "test_aplanar_lista_basica", "status": "passed"},
        {"test_unit": "test_aplanar_lista_files_tf", "status": "passed"},
        {"test_integration": "test_module_network", "status": "passed"},
        {"test_integration": "test_module_compute", "status": "failed"}
    ]

    assert test_results_plana == test_esperado_results_plana
    assert len(test_results_plana) == 4


def test_separar_lista_archivos_py():
    archivos = ["list_utils.py", "test_list_utils.py",
                "variables.tf", "setup.sh"]
    archivos_py, otros_archivos = list_utils.separar_lista(
        archivos,
        lambda archivo: archivo.endswith("py")
    )
    assert archivos_py == ["list_utils.py", "test_list_utils.py"]
    assert otros_archivos == ["variables.tf", "setup.sh"]
    assert len(archivos_py) + len(otros_archivos) == len(archivos)


def test_separar_pruebas_exitosas_fallidas():
    test_results = [
        {"test_unit": "test_aplanar_lista_basica", "status": "passed"},
        {"test_unit": "test_aplanar_lista_files_tf", "status": "passed"},
        {"test_integration": "test_module_network", "status": "passed"},
        {"test_integration": "test_module_compute", "status": "failed"}
    ]
    tests_exitosos, tests_fallidos = list_utils.separar_lista(
        test_results,
        lambda test: test["status"] == "passed"
    )
    assert len(tests_exitosos) == 3
    assert len(tests_fallidos) == 1


def test_agrupar_por_extension_archivos():
    archivos = ["list_utils.py", "Makefile",
                "variables.tf", "main.py"]
    archivos_agrupados = list_utils.agrupar_por_extension(archivos)
    archivos_esperados_agrupados = {
        ".tf": ["variables.tf"],
        ".py": ["list_utils.py", "main.py"],
        "": ["Makefile"]
    }
    assert archivos_agrupados == archivos_esperados_agrupados


def test_eliminar_duplicados_archivos():
    archivos = [
        "module/network/main.tf", "module/compute/main.tf",
        "module/network/main.tf", "module/dev/variables.tf",
        "module/compute/main.tf",
    ]
    archivos_sin_duplicar = list_utils.eliminar_duplicados(archivos)
    assert len(archivos_sin_duplicar) == 3


def test_filtrar_por_patron_archivos():
    archivos = ["list_utils.py", "Makefile",
                "variables.tf", "main.py"]
    archivos_filtrados = list_utils.filtrar_por_patron(archivos, r"\.tf$")
    archivos_esperados_filtrados = ["variables.tf"]
    assert archivos_filtrados == archivos_esperados_filtrados
