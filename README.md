# Sistema Automatizado de Gestión del Taller Mecánica Automotriz de Alta Gama (SAGTMA) - Holiday Int.

Repositorio del Sistema Automatizado de Gestión del Taller Mecánica Automotriz de Alta Gama (SAGTMA), proyecto de desarrollo de la asignatura Ingeniería de Software I (CI-3715) durante el trimestre Enero-Marzo 2023 en la Universidad Simón Bolívar.

## Sobre SAGTMA

<img src="images/project_details_1.png" alt="project_details_1"/>

El Sistema Automatizado de Gestión del Taller Mecánica Automotriz de Alta Gama (SAGTMA) es un sistema de gestión administrativa de los talleres para la empresa transnacional Holiday Internacional que ofrece servicios de mecánica automotriz. Permite gestionar la información de los trabajadores, los proyectos desarrollados en cada taller, el registro de clientes, sus respectivos automóviles y la creación de planes de acción para la solución de los proyectos asignados a distintos trabajadores. 

<img src="images/menu.png" alt="menu"/>


## Funcionalidades del sistema

El sistema SAGTMA cuenta con las siguientes funcionalidades:

* Permitir el ingreso al sistema a los usuarios autenticados por el administrador.
* Gestionar la creación de usuarios en caso de ser un administrador del sistema.
* Registro de trabajadores como usuarios del sistema en el que cuentan con diversos roles y permisos para el manejo del sistema.
* Registro de clientes que solicitan servicios en los talleres de Holiday Int. y registro de sus respectivos vehículos.
* Creación de proyectos y asignación de un gerente para cada uno de ellos.
* Manejo de los proyectos por parte del gerente de proyectos quien puede editar el proyecto, asignar nuevos integrantes y suspender el proyecto.
* Creación de nuevos departamentos.
* Creación de planes de acción para solucionar los problemas asociados a un proyecto.
* Creación de unidades de medidas para especificar el plan de acción de un proyecto.
* Sección de logger que permite observar los movimientos realizados en el sistema por un usuario en particular.


## Desarrollo

SAGTMA se encuentra en fase de pruebas. El desarrollo se elaboró con Python 3.11.1, Flask 2.2.2, SQLAlchemy 2.0. y flask_sqlalchemy 3.0.3. El resto de requerimientos del sistema pueden conocerse visitando el archivo "requirements.txt".

## Documentación

La documentación de SAGTMA se puede encontrar en:

* Guía de usuario: En esta guía se encuentra una serie de explicaciones acerca del funcionamiento de la interfaz del sistema.

* Guía del programador: En esta guía se encuentran los detalles de la implementación, el diseño y cómo se debe correr el sistema.

## Pruebas

Las pruebas de este sistema se encuentran alojadas en la carpeta tests y pueden ser corridas de la siguiente manera:

Para linux:

#### Ejecución de todas las pruebas:
`python3 -m unittest Tests_*.py` 

#### Ejecución de solo las pruebas de selenium:

`python3 -m unittest Tests_*.py -k Selenium`

#### Ejecución de pruebas de un módulo especifico

`python3 -m unittest Tests_Department.py`

#### Ejecución de una prueba especifica de un modulo en especifico

`python3 -m unittest Tests_Department.py -k test_remove_department`

En caso de realizar la corrida en Windows, debe modificarse python3 por python.

Las pruebas incluyen unit tests y pruebas con Selenium, para garantizar la calidad de código y la ausencia de errores.
Para más información acerca de la ejecución del sistema, visitar la guía del programador.

## Autores

* Jesús Bandez
* Adelina Figueira 
* Luis Blanco


