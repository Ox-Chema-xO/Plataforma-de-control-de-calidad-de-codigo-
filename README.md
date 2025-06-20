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

## Sprint 2

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
│   ├── main.tf
│   └── variables.tf                    
│
├── iac_tests/
│   ├── __init__.py
│   ├── test_terraform_validation.py
│   ├── test_iac_variables.py           
│   └── test_iac_dummy.py               
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
│       ├── list_utils.py
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
│   ├── test_string_utils_con_mock.py
│   ├── test_string_utils_exceptions.py
│   ├── test_string_utils.py
│   └── test_monkeypatch_simulation.py
│
├── .gitignore
├── coverage.xml
├── dashboard_ascii.py                  
├── pytest_results.log                 
├── README.md
└── requirements.txt

```

### Pruebas unitarias

#### Fixtures module y function

Se expandio el sistema de testing con fixtures module y function implementados en `tests/conftest.py`:

-   **Fixtures module**:  Se ejecutan una sola vez por archivo de test, proporcionando datos compartidos como `datos_compartidos_modulo` con strings y numeros que persisten durante todo el modulo para optimizar el rendimiento
-   **Fixtures function**: Se ejecutan antes de cada test individual generando datos unicos como `datos_inicializados` con listas vacias, contadores y estados que se reinician para cada test, garantizando aislamiento completo entre pruebas

Se agregaron tests adicionales para demostrar el uso de estos fixtures:

-   **`test_string_utils.py`**: Agregados tests `test_string_con_datos_compartidos()` que utiliza datos compartidos del modulo para validar funciones de strings con configuracion persistente y `test_string_con_datos_inicializados()` que usa datos unicos por test para verificar comportamiento aislado
-   **`test_list_utils.py`**: Implementados tests `test_list_con_numeros_compartidos()` que aprovecha numeros compartidos del modulo para validar operaciones con listas usando la configuracion global y `test_list_con_datos_inicializados()` que modifica datos unicos por test para comprobar que cada ejecucion inicia con estados limpios

#### Simulacion con monkeypatch

Se creo `test_monkeypatch_simulation.py` que utiliza la funcionalidad de monkeypatch de pytest para simular llamadas a funciones del sistema:

-   **Simulacion de variables de entorno**: Tests que utilizan `monkeypatch.setenv()`, `monkeypatch.delenv()`, etc, para simular diferentes escenarios de configuracion
-   **Simulacion de filesystem**: Uso de `monkeypatch.setattr()` para simular `os.listdir()` y `os.getcwd()`

En total se crearon 8 test para simular llamadas a funciones del sistema en diferentes escenarios

#### implementacion de patch.object y pytest.create_autospec en los test de utils/
Se agregaron tests para usar tecnicas de mocking para probar metodos de `src/utils/`:

-   **patch.object**: Reemplaza temporalmente metodos especificos de clases para simular diferentes comportamientos durante las pruebas
-   **create_autospec**: Crea mocks que mantienen las firmas originales de los metodos evitando errores

#### Tests con markers xfail y skip
Se agregaron nuevos tests en `test_list_utils.py` y `test_string_utils_con_mock.py` que usan marcas especiales de pytest para manejar casos especificos:
-   **@pytest.mark.xfail**: Para tests que sabemos que van a fallar por ahora. Esto nos permite documentar bugs conocidos sin que se detenga todo la ejecucion de los tests
-   **@pytest.mark.skip**: Para tests que dependen de cosas externas como variables de entorno que tal vez no esten instalados en todas las maquinas

Cada marca incluye mensajes descriptivos que explican el motivo del marcado, facilitando asi el mantenimiento y la comprension del codigo de pruebas

### IAC

#### Variables de Terraform
Se creo `iac/variables.tf` con:

-   3 variables definidas con tipos correctos
-   Descripciones para cada variable
-   Valores por defecto apropiados

#### Provisioner local

Se modifico `iac/main.tf` para incluir:

-   Un recurso `null_resource` con provisioner local
-   Creacion automatica del archivo `iac_dummy.txt`

#### Tests de infraestructura

Se implementaron dos nuevos scripts de testing de infraestructura:

**`iac_tests/test_iac_variables.py`**:

-   Valida que las variables en `variables.tf` tengan tipos correctos
-   Verifica que las variables requeridas no esten vacías
-   Utiliza la librería `hcl2` para parsear archivos Terraform

**`iac_tests/test_iac_dummy.py`**:

-   Ejecuta el ciclo completo de Terraform: `init`, `apply`, validacion y `destroy`
-   Valida que el archivo `iac_dummy.txt` se cree correctamente
-   Implementa limpieza automatica del estado de Terraform

#### Mejora de run_tests.sh 

Se mejoro `scripts/run_tests.sh` para incluir:

-   **Integracion con Terraform**: Ejecucion de `terraform init` y `terraform apply -auto-approve`
-   **Captura de errores**: El script falla si alguna prueba IAC no pasa
-   **Generación de logs**: Guarda la salida de pytest en `pytest_results.log` para el dashboard

Para ejecutar el bash script `run_tests.sh`:
```bash
# Ejemplo de ejecucion
$ ./scripts/run_tests.sh
# Ejecuta tests python + tests de infraestructura + genera logs
```

### Dashboard ASCII

Se creo `dashboard_ascii.py` un script que proporciona visualizacion de resultados:

-   **Lectura de cobertura**: Parsea `coverage.xml` y extrae el porcentaje de cobertura
-   **Barra de progreso ASCII**: Genera barras visuales proporcionales usando caracteres `█` y `░`
-   **Estadísticas de tests**: Lee `pytest_results.log` para mostrar tests pasados y fallidos

Para ejecutar `dashboard_ascii.py` primero hay que ejecutar `run_tetst.sh` ya que esta genera el reporte de cobertura y el log de resultados de pytest, por lo que los pasos para ejecutar `dashboard_ascii.py` serian los siguientes:
```bash
# Generacion de reporte de cobertura y resultados de pytest
$ ./scripts/run_tests.sh
# Generacion del dashboard ascii
$ python3 dashboard_ascii.py
```
La salida al ejecutar `dashboard_ascii.py` seria la siguiente:

```
==================================================
  DASHBOARD ASCII - REPORTE DE COBERTURA
==================================================

COBERTURA DE CODIGO:
   ███████████████████░ 98.4%
   Estado: EXCELENTE

RESULTADOS DE TESTS:
   Total ejecutados: 141
   Pasados: 141
   Fallidos: 0
   Estado: TODOS LOS TESTS PASARON

==================================================
```

   <div align="center">
      <img src="https://i.postimg.cc/3rnqc6qp/pc3-1.png" alt="image6" width="850" />
   </div>

Vemos que tiene un 98% de cobertura y tenemos 141 test en totales, de las cuales 141 pasan por lo que todos los test pasan correctamente

### Flujo de trabajo

Durante el Sprint 2 se distribuyeron las  issues entre los desarrolladores:

   <div align="center">
      <img src="https://i.postimg.cc/2jQ3P7kY/pc3-2.png" alt="image6" width="750" />
   </div>

Cada issue siguio el mismo flujo de trabajo del Sprint 1:

1.  Asignacion y estimacion en el kanban board
2.  Desarrollo en ramas feature especificas
3.  Pull requests con revision de codigo
4.  Integracion a develop tras aprobacion
5.  Actualizacion de horas reales invertidas

El kanban board comenzo con todas las issues en Sprint Backlog

   <div align="center">
      <img src="https://i.postimg.cc/Xv6DrWCt/pc3-3.png" alt="image6" width="1100" />
   </div>

Luego se fueron avanzando las issues hasta que las terminamos y llega a Review/QA para que los otros desarrolladores lo revisen y aprueben el PR

   <div align="center">
      <img src="https://i.postimg.cc/TPjNmsj1/pc3-4.png" alt="image6" width="1100" />
   </div>

   <div align="center">
      <img src="https://i.postimg.cc/Dz9Jk28p/pc3-5.png" alt="image6" width="800" />
   </div>

   <div align="center">
      <img src="https://i.postimg.cc/HLcchJs7/pc3-6.png" alt="image6" width="700" />
   </div>

Hasta que todas las issues son completas y veremos que todas las issues estan en Done

   <div align="center">
      <img src="https://i.postimg.cc/wvmt3jWJ/pc3-9.png" alt="image6" width="1100" />
   </div>

Al final quedariamos se crearon estas ramas para el Sprint 2:

   <div align="center">
      <img src="https://i.postimg.cc/52L8Kp5L/pc3-7.png" alt="image6" width="300" />
   </div>

y el historial de commits del Sprint 2 es el siguiente:

   <div align="center">
      <img src="https://i.postimg.cc/4xk9cVCd/pc3-8.png" alt="image6" width="1000" />
   </div>

## Videos
Se referencia el link de los video de cada cada Sprint hecho:

- **Sprint 1**: https://unipe-my.sharepoint.com/:v:/g/personal/guido_chipana_c_uni_pe/EVUE_SK1IBZHuLs1czTY_pIBxpEpdmKeIMkNz2c_hSwtyA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=vZLDGc
