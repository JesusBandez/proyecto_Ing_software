# Guía del programador

Este documento es una guía para el uso de SAGTMA por parte del programador. Se indican ciertos detalles de la implementación y diseño que pueden ser de importancia al momento de realizar la corrida del sistema.

Versiones principales de paquetes
Se requiere de los siguientes paquetes para que el sistema pueda correrse en el computador:

		Flask==2.2.2
		flask_sqlalchemy==3.0.3
		pdfkit==1.0.0
		selenium==4.8.2
		SQLAlchemy==2.0.0
		Werkzeug==2.2.2


## Base de datos
La base de datos fue diseñada de la siguiente manera:

| Entidades        | Atributos                                                                                                                      | Métodos                    |
|------------------|--------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| User             | first_name, last_name, username, password, role, job, status, managed_projects, action_plans, human_talents, supplies          | repr, init                 |
| Project          | description, start, finish, available, issue, solution, observations, users, amount, car, department, manager_id, action_plans | repr, init                 |
| Car              | license_plate, brand, model, year, serial_car, serial_engine, color, issue, owner, associated_projects                         | repr, init                 |
| Clients          | ci, first_name, last_name, birth_date, mail, phone, address, cars                                                              | repr, init                 |
| Logger           | event, date, hour                                                                                                              | repr, init                 |
| Department       | description, associated_projects                                                                                               | repr, init                 |
| Measures         | dimension, unit                                                                                                                | repr, init                 |
| ActionPlan       | action, activity, start_date, finish_date, hours, responsible, cost, project, human_talents, supplies                          | repr, init                 |
| HumanTalent      | action, activity, time, quantity, cost, responsible, plan                                                                      | repr, init, total_amount   |
| MaterialSupplies | action, activity, category, description, quantity, measure, cost, responsible, total_amount, action_plan                       | repr, init, total_amount() |


## Ejecución de pruebas
Las pruebas pueden ejecutarse desde la carpeta tests, ejecutando el entorno virtual.

#### Ejecución de todas las pruebas:
`python3 -m unittest Tests_*.py` 

#### Ejecución de solo las pruebas de selenium:

`python3 -m unittest Tests_*.py -k Selenium`

#### Ejecución de pruebas de un módulo especifico

`python3 -m unittest Tests_Department.py`

#### Ejecución de una prueba especifica de un modulo en especifico

`python3 -m unittest Tests_Department.py -k test_remove_department`

En caso de realizar la corrida en Windows, debe modificarse python3 por python.


## Creación de un entorno virtual

Para la instalación de python venv

En Unix:

	python3 -m pip install --user virtualenv

En Windows:

	py -m pip install --user virtualenv

Para crear el entorno virtual:

En Unix:

	python -m venv env

En Windows: 

	python -m venv env


## Ejecución del entorno virtual
Dentro de la carpeta root del proyecto
En Unix:

	source env/bin/activate

En Windows: 

	.\env\Scripts\Activate.bat


## Instalar dependencias
Para instalar las dependencias del proyecto se usa el archivo requirements.txt

	pip install -r requirements.txt



## Iniciar el servidor
Para iniciar el servidor se debe correr desde el entorno virtual el siguiente comando:

	flask --app main --debug run

## Creación de la base de datos

Una vez iniciado el servidor, para inicializar la base de datos, se puede ingresar el siguiente link:

	http://127.0.0.1:5000/restart_bbdd
