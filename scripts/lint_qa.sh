#!/bin/bash

for dir in src/ scripts/ iac/; do
    if [ ! -d "$dir" ]; then
        echo "Error: No existe $dir"
        exit 1
    fi
done

echo "Ejecutando flake8 en src/"
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
cd ..

echo "lint-qa finalizo correctamente"
