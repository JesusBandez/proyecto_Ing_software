# Tests

Suite de pruebas para la aplicación.

Los siguientes ejemplos asumen que la terminal se encuentra en el directorio actual.

#### Ejecutar todas las pruebas:
`python3 -m unittest Tests_*.py` 

#### Ejecutar solo las pruebas de selenium:

`python3 -m unittest Tests_*.py -k Selenium`

#### Ejecutar pruebas de un modulo especifico

`python3 -m unittest Tests_Department.py`

#### Ejecutar una prueba especifica de un modulo en especifico

`python3 -m unittest Tests_Department.py -k test_remove_department`


python -m unittest Tests_Measure.py
python -m unittest Tests_Action_Plan.py