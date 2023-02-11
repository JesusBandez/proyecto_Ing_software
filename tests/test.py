from sqlalchemy import create_engine, text
import unittest
import unittest
from selenium import webdriver

engine = create_engine("sqlite:///instance/database.db")


# Estas pruebas son realizadas con el navegador Firefox. Se necesita
# selenium y el driver geckodriver para poder iniciarlas
browser = webdriver.Firefox(executable_path="./drivers/geckodriver")


class tests(unittest.TestCase):
    def test(self):
        '''Esta prueba requiere que exista un usuario con nombre 1
        y contrasenia 1 en la base de datos'''
        browser.get('http://127.0.0.1:5000/login')
        browser.find_element('id', 'username').send_keys("1")
        browser.find_element('id', 'password').send_keys("1")
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'User\'s list' )

if __name__ == "__main__":
    unittest.main()


"""
# Buscar en la base
with engine.connect() as connect:
    result = connect.execute(text('SELECT * FROM user WHERE username=\'1\''))
    for row in result:
        print(row[0])
"""

