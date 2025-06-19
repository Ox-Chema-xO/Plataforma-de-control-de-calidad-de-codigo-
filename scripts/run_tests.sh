#!/bin/bash

for dir in src/ tests/ iac/ iac_tests/; do
    if [ ! -d "$dir" ]; then
        echo "Error: No existe $dir"
        exit 1
    fi
done

capturar_error(){
    local codigo_salida=$1
    local nombre_comando=$2
    if [ "$codigo_salida" -ne 0 ]; then
        echo "Error: $nombre_comando (codigo: $codigo_salida)"
        exit "$codigo_salida"
    fi
}
echo "Ejecutando pytest en tests/ con cobertura en src/"
if ! pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=xml | tee pytest_results.log; then
    exit 1
fi

if [ ! -f "coverage.xml" ]; then
    echo "Error: No se genero reporte de cobertura"
    exit 1
fi

echo "Ejecutando terraform init en iac/"
cd iac/ || capture_error $? "cd iac/"
terraform init
capturar_error $? "terraform init"

echo "Ejecutando terraform apply en iac/"
terraform apply -auto-approve -no-color | tee ../terraform_apply.log
capturar_error $? "terraform apply"
cd ..

echo "Ejecutando pytest en iac_tests/"
pytest -v iac_tests/
capturar_error $? "pytest en iac_tests/"

echo "Pruebas finalizadas correctamente con reporte de cobertura y resultados"
