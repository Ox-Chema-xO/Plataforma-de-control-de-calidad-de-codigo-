# Proyecto 2: Plataforma de Control de Calidad de Codigo

Este proyecto consiste en el desarrollo de una plataforma de control de calidad de código, diseñada para integrar pruebas unitarias y de integración usando pytest y pruebas de infraestructura local utilizando terraform

## Estructura base del proyecto

Esctructura inicial del proyecto:

```
Plataforma-de-control-de-calidad-de-codigo/
│
├── hooks/
│   ├── commit-msg
│   ├── pre-commit
│   └── pre-push
│
├── iac/
│   └── __init__.py
│
├── iac_tests/
│   └── __init__.py
│
├── scripts/
│   ├── __init__.py
│   └── setup.sh
│
├── src/
│   ├── helpers/
│   │   └── __init__.py
│   │
│   └── utils/
│       └── __init__.py
│
├── tests/
│   └── __init__.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

Se crearon 3 hooks iniciales:

- **commit-msg:** valida el formato de los commits
- **pre-commit:** valida archivos permitidos (.py, .sh, .tf, .tfvars, .md, .svg, .txt)
- **pre-push:** evita push directo a main, protege la rama main

Y un bash script `setup.sh` para inicializar el proyecto, este script instalara las librerias de requeriments,txt e instalara los hooks en el local de cada desarrollador, listo para el desarrollo del proyecto

## Git Flow

Seguimos las politicas de Git Flow lo que nos permitio seguir un flujo de trabajo estructurado para separar los procesos de desarrollo y asi mantener un historial más legible y reversible.

   <div align="center">
      <img src="https://i.postimg.cc/x1qspHYj/image.png" alt="image" width="700" />
   </div>

## Instalacion del Proyecto

Para instalar o inicializar el proyecto hay que seguir los siguientes pasos

- Clonar repositorio

```bash
$ git clone https://github.com/Ox-Chema-xO/Plataforma-de-control-de-calidad-de-codigo-.git
$ cd Plataforma-de-control-de-calidad-de-codigo-
```

- Crear entorno virtual

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate 
```

- Instalacion de dependencias y hooks

```bash
$ chmod +x scripts/setup.sh 
$ ./scripts/setup.sh
```

## Sprint 1

### Estructura del proyecto

```
Plataforma-de-control-de-calidad-de-codigo/
│
├── hooks/
│   ├── commit-msg
│   ├── pre-commit
│   └── pre-push
│
├── iac/
│   ├── __init__.py
│   └── main.tf
│
├── iac_tests/
│   ├── __init__.py
│   └── test_terraform_validation.py
│
├── scripts/
│   ├── __init__.py
│   ├── lint_qa.sh
│   ├── run_tests.sh
│   └── setup.sh
│
├── src/
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── gestor_archivos.py
│   │   └── gestor_directorios.py
│   │
│   ├── logs/
│   │   ├── __init__.py
│   │   └── registrador_logs.py
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── reportador.py
│   │
│   └── utils/
│       ├── __init__.py
|       ├── list_utils.py
│       └── string_utils.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_helpers.py
│   ├── test_list_utils_exceptions.py
│   ├── test_list_utils.py
│   ├── test_logs.py
│   ├── test_reportador.py
│   ├── test_string_utils_exceptions.py
│   └── test_string_utils.py
│
├── .gitignore
├── coverage.xml
├── README.md
└── requirements.txt
```

### Modulos

#### src/

En src/ se ha organizado el proyecto en cuatro carpetas principales:

- **utils/**
    - `list_utils.py`: Funciones genéricas para manejar listas como listas anidadas, filtrado, agrupación por extensión, eliminación de duplicados, ordenación, usadas para procesar resultados de código Python, Terraform y pruebas.
    - `string_utils.py`: Funciones genericas para manejar cadenas, como limpiar cadenas, extraer métricas de salida y estructurar texto para dashboards y reportes.
- **helpers/**
    
    Clases GestorArchivos y GestorDirectorios que abstraen las operaciones de creación, lectura/escritura y mantenimiento de la estructura de ficheros y carpetas que requiere el sistema.
    
- **logs/**
    
    `registrador_logs.py`: Implementa un logger centralizado que persiste eventos y resultados de las herramientas de QA con marcas temporales precisas.
    
- **reporting/**
    
    `reportador.py`: Lee los logs generados, los transforma y formatea en documentos fáciles de supervisar.
    

#### iac/

En iac/ se creo un módulo terraform mínimo main.tf que contiene un recurso null_resource y  una variable para nuestra infraestructura local.

#### iac_tests/

Se realizo una prueba unitaria para validar sintaxis del archivo main.tf de iac/

#### tests/

Se realizaron pruebas unitarias para casos positivos y de excepcion que nos permitio validar el correcto funcionamiento de las funciones genericas de utils, las clases base de helpers/, logs/, reporting/ y asi como tambien nuestra infraestructura en iac/

Ademas se incluye conftest para agregar una fixture global que preparar un entorno temporal para que ejecutar determinadas pruebas que requieran de un entorno limpio y aislado.

#### scripts/

Se crearon 2 bash scripts:

- **lint_qa.sh:** Analiza el codigo con linters como flake8, shellcheck y terraform fmt -check. Para ejecutar este bash script hay que seguir los siguientes pasos:
    
```bash
    # dar permisos de ejecucion
    $ chmod +x scripts/setup.sh
    # ejecutar el bash script
    $ ./scripts/lint_qa.sh
``` 
    
- **run_tests.sh:** Ejecuta todo los test y para ejecutar este bash script hay que seguir los siguientes pasos:
    
```bash
    # dar permisos de ejecucion
    $ chmod +x scripts/setup.sh
    # ejecutar el bash script
    $ ./scripts/run_tests.sh
```
    

### Flujo de Trabajo

En este Sprint delegamos issues parte del sprint 1 a cada integrante

   <div align="center">
      <img src="https://i.postimg.cc/8CXfKJpG/image-1.png" alt="image1" width="600" />
   </div>

Para cada issue se agregaron los siguientes fields:

- **Puntos:** Nivel de importancia de la issue en un rango de 1-5
- **Horas estimadas:** Tiempo estimado para completar la issue
- **Horas reales:** Tiempo real invertido al completar la issue
- **Sprint:** Sprint al que pertenece

Por ejemplo esta son los fields de la issue #2 Crear funciones genericas para manejo de listas:

   <div align="center">
      <img src="https://i.postimg.cc/Bvn1BcGN/image-2.png" alt="image2" width="250" />
   </div>

El kanban board inicial para el sprint 1, en donde todas las issues estan en Sprint Backlog

   <div align="center">
      <img src="https://i.postimg.cc/nz6jxy9w/image-3.png" alt="image3" width="1000" />
   </div>

Se comenzo completando la Issue #2, #3, #6 por lo que estas issues se movieron a la columna In progress

   <div align="center">
      <img src="https://i.postimg.cc/qRth9Jq3/image-4.png" alt="image4" width="1000" />
   </div>

Al terminar la issue, esta se movieron a la columna Review/QA en donde los otros desarrolladores revisaron los cambios si estan bien implementados

   <div align="center">
      <img src="https://i.postimg.cc/1Xwg3vpR/image-5.png" alt="image5" width="1000" />
   </div>

El desarrollador encargado de la issue envia una Pull Request desde la rama que trabajo a la rama develop en donde se solicita la revision de los cambios y si estan conformes con los cambios o nuevas implementaciones hechas 

   <div align="center">
      <img src="https://i.postimg.cc/J7kHxz9w/image-6.png" alt="image6" width="600" />
   </div>

Los otros desarrolladores revisan el PR y envian un mensaje de confirmacion en donde se aprueba el PR

   <div align="center">
      <img src="https://i.postimg.cc/L6FYbMpJ/image-7.png" alt="image7" width="600" />
   </div>

Cuando los otros desarrolladores aceptaron los cambios hechos, el desarrollador encargado de la issue le asigna las horas reales que le tomo completar esta issue y se mueve a la columna Done

   <div align="center">
      <img src="https://i.postimg.cc/02GMgHkc/image-8.png" alt="image8" width="1000" />
   </div>

Conforme se va avanzando el proceso se va actualizando el tablero hasta que todas las issues del sprint 1 llegan a la columna Done

   <div align="center">
      <img src="https://i.postimg.cc/kgnV7FD9/image-9.png" alt="image9" width="1000" />
   </div>

### Historial y ramas
Durante todo el desarrollo del sprint 1 creamos estas ramas:

   <div align="center">
      <img src="https://i.postimg.cc/7hw4S9FZ/imagen10.png" alt="image10" width="700" />
   </div>

Y el historial de commits durante todo el desarrollo del sprint 1 fue el siguiente:

   <div align="center">
      <img src="https://i.postimg.cc/Fzp4pcvg/imagen11.png" alt="image11" width="900" />
   </div>

Durante el desarrollo del Sprint 1 cada desarrollador trabajo cada issue asignada en ramas diferentes en paralelo, al terminar todas las issues y tener todo los cambios en la rama develop, nace otra rama release desde develop en donde se agrega la documentacion correspondiente al sprint 1, asi aplicando correctamente las politicas de Git Flow

## Videos
Se referencia el link de los video de cada cada Sprint hecho:

- **Sprint 1**: https://unipe-my.sharepoint.com/:v:/g/personal/guido_chipana_c_uni_pe/EVUE_SK1IBZHuLs1czTY_pIBxpEpdmKeIMkNz2c_hSwtyA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=vZLDGc
