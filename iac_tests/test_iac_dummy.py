import subprocess
from pathlib import Path


def test_terraform_apply_creates_dummy_file():
    """
    - Ejecuta terraform apply -auto-approve en modo no-interactive
    - Valida que se crea un archivo dummy en el directorio iac
    - Elimina automáticamente el estado de terraform al finalizar la prueba
    """
    # Rutas
    iac_dir = Path("iac")
    dummy_file = iac_dir / "iac_dummy.txt"
    # Asegurar que el archivo no existe antes de la prueba
    if dummy_file.exists():
        dummy_file.unlink()
    try:
        # Ejecutar terraform init
        subprocess.run(
            ["terraform", "init"],  # Comando a ejecutar como una lista
            cwd=iac_dir,            # Directorio donde se ejecutará el comando
            capture_output=True,    # Capturar la salida del comando
            text=True,              # Convertir la salida a texto
            check=True              # Lanzar una excepción si el comando falla
        )
        # Ejecutar terraform apply
        subprocess.run(
            ["terraform", "apply", "-auto-approve"],
            cwd=iac_dir,
            capture_output=True,
            text=True,
            check=True
        )
        # Verificar que el archivo fue creado por terraform apply
        assert dummy_file.exists()
    finally:
        # Limpieza: destruir los recursos de terraform
        subprocess.run(
            ["terraform", "destroy", "-auto-approve"],
            cwd=iac_dir,
            capture_output=True,
            text=True,
            check=True
        )
        # Incluso si destroy falla, intentar eliminar archivos de estado
        for state_file in iac_dir.glob("*.tfstate*"):
            try:
                state_file.unlink()
            except FileNotFoundError:
                pass  # Ignorar si el archivo no existe
