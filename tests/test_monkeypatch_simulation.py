import os


def test_os_getenv_variable_existe(monkeypatch):
    """Test que simula variable de entorno existente"""
    monkeypatch.setenv("TEST_VAR", "valor_test")

    resultado = os.getenv("TEST_VAR")
    assert resultado == "valor_test"


def test_os_getenv_variable_no_existe(monkeypatch):
    """Test que simula variable de entorno inexistente"""
    monkeypatch.setenv("TEST_VAR", "valor_test")
    monkeypatch.delenv("TEST_VAR")

    resultado = os.getenv("TEST_VAR")
    assert resultado is None


def test_os_getenv_variable_vacia(monkeypatch):
    """Test que simula variable de entorno vacia"""
    monkeypatch.setenv("EMPTY_VAR", "")

    resultado = os.getenv("EMPTY_VAR")
    assert resultado == ""


def test_os_path_exists_archivo_existe(monkeypatch):
    """Test que simula archivo existente"""
    monkeypatch.setattr(os.path, "exists", lambda path: True)

    resultado = os.path.exists("/direccion/file.txt")
    assert resultado is True


def test_os_path_exists_archivo_no_existe(monkeypatch):
    """Test que simula archivo inexistente"""
    monkeypatch.setattr(os.path, "exists", lambda path: False)

    resultado = os.path.exists("/direccion/file.txt")
    assert resultado is False


def test_os_listdir_simulado(monkeypatch):
    """Test que simula contenido de directorio"""
    fake_files = ["archivo1.txt", "archivo2.py", "carpeta1"]
    monkeypatch.setattr(os, "listdir", lambda path: fake_files)

    resultado = os.listdir("/fake/directorio")
    assert len(resultado) == 3
    assert "archivo1.txt" in resultado
    assert "archivo2.py" in resultado
    assert "carpeta1" in resultado


def test_os_getcwd_simulado(monkeypatch):
    """Test que simula directorio actual"""
    fake_directorio_actual = "/fake/directorio_actual"
    monkeypatch.setattr(os, "getcwd", lambda: fake_directorio_actual)

    resultado = os.getcwd()
    assert resultado == fake_directorio_actual


def test_multiples_variables_entorno(monkeypatch):
    """Test que simula multiples variables de entorno"""
    monkeypatch.setenv("APP_NAME", "plataforma_qa")
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("PORT", "8080")

    app_name = os.getenv("APP_NAME")
    debug = os.getenv("DEBUG")
    port = os.getenv("PORT")

    assert app_name == "plataforma_qa"
    assert debug == "True"
    assert port == "8080"
