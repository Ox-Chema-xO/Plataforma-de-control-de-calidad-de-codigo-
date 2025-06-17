# Proyecto 2: Plataforma de Control de Calidad de Codigo

Este es un proyecto en donde se creara una plataforma de control de calidad de codigo, esta plataforma integrara pruebas unitarias y de integracion con pytest y pruebas de infraestructura Terraform. 

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

Y un bash script “[setup.sh](http://setup.sh)” para inicializar el proyecto, este script instalara las librerias de requeriments,txt e instalara los hooks en el local de cada desarrollador, listo para el desarrollo del proyecto

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