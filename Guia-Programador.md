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



## Creación de la base de datos

Para inicializar la base de datos, se puede ingresar el siguiente link:

	http://127.0.0.1:5000/restart_bbdd

O también se pueden colocar los siguientes comandos (una vez ejecutado el entorno virtual):

	flask --app manage shell
	init_db()

## Iniciar el servidor
Para iniciar el servidor se debe correr desde el entorno virtual el siguiente comando:

	flask --app main --debug run