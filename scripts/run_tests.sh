#!/bin/bash

for dir in src/ tests/; do
    if [ ! -d "$dir" ]; then
        echo "Error: No existe $dir"
        exit 1
    fi
done

echo "Ejecutando pytest en tests/ con cobertura en src/"
if ! pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=xml; then
    exit 1
fi

if [ ! -f "coverage.xml" ]; then
    echo "Error: No se genero reporte de cobertura"
    exit 1
fi

echo "Pruebas finalizadas correctamente con reporte de cobertura"
