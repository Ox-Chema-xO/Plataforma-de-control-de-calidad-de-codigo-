#!/bin/bash

for dir in src/ scripts/ iac/; do
    if [ ! -d "$dir" ]; then
        echo "Error: No existe $dir"
        exit 1
    fi
done

echo "Ejecutando flake8 --select para encontrar errores criticos en src/"
if ! flake8 --select=E9,F63,F7,F82 --show-source src/; then
    exit 1
fi

echo "Ejecutando flake8 para estilo de codigo en src/"
if ! flake8 src/; then
    exit 1
fi

echo "Ejecutando shellcheck en scripts/"
for script in scripts/*.sh; do
    if [ -f "$script" ]; then
        if ! shellcheck "$script"; then
            exit 1
        fi
    fi
done

echo "Ejecutando terraform fmt -check en iac/"
cd iac/ || { echo "Error: No se pudo entrar al directorio iac/"; exit 1; }
if ! terraform fmt -check; then
    exit 1
fi

echo "Ejecutando tflint en iac/"
if ! command -v tflint &> /dev/null; then
    echo "Advertencia: tflint no esta instalado, omitiendo validacion"
else
    if [ -f ".tflint.hcl" ]; then
        if ! tflint; then
            exit 1
        fi
    else
        echo "Advertencia: No existe .tflint.hcl, ejecutando tflint basico"
        if ! tflint; then
            exit 1
        fi
    fi
fi
cd ..

echo "lint-qa finalizo correctamente"
