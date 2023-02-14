from sqlalchemy import create_engine, text
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

engine = create_engine("sqlite:///instance/database.db")

unittest.TestLoader.sortTestMethodsUsing = None
# Estas pruebas son realizadas con el navegador Firefox. Se necesita
# selenium y el driver geckodriver para poder iniciarlas

class tests(unittest.TestCase):

    def test_a_non_existent_user(self):
        print("Usuario no existente")
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
        browser.get('http://127.0.0.1:5000/login')
        browser.find_element('id', 'username').send_keys("NOEXISTO")        
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'Login' )        
        browser.quit()

    def test_b_bad_password(self):
        print("Contrasenia equivocada")
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
        browser.get('http://127.0.0.1:5000/login')
        browser.find_element('id', 'username').send_keys("1")
        browser.find_element('id', 'password').send_keys("Contrasenia Inexistente")        
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'Login' )        
        browser.quit()
    
    def test_c_login(self):
        print("Login y logout correcto")
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
        browser.get('http://127.0.0.1:5000/login')
        browser.find_element('id', 'username').send_keys("1")
        browser.find_element('id', 'password').send_keys("1")        
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'User\'s list' )        
        browser.find_element(By.CSS_SELECTOR, 'div.container-fluid>a.btn').click()        
        browser.quit()
        

    def test_d_delete_user_admin(self):
        print("Borrar usuario")
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
        browser.get('http://127.0.0.1:5000/login')
        browser.find_element('id', 'username').send_keys("1")
        browser.find_element('id', 'password').send_keys("1")        
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'User\'s list' )        
        browser.find_element(By.XPATH, r"// td[ text() = '3' ]/..").find_element(By.CSS_SELECTOR, r'button').click()        
        browser.find_element(By.CSS_SELECTOR, 'div.container-fluid>a.btn').click()
        browser.quit()

    def test_e_add_user_admin(self):
        print("Agregar usuario borrado")
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
        browser.get('http://127.0.0.1:5000/login')
        browser.find_element('id', 'username').send_keys("1")
        browser.find_element('id', 'password').send_keys("1")        
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'User\'s list' )
        browser.find_element(By.CSS_SELECTOR, 'div.container-sm>a').click()        
        browser.find_element('id', 'username').send_keys("3")
        browser.find_element('id', 'password').send_keys("3")        
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'User\'s list' )        
        browser.find_element(By.CSS_SELECTOR, 'div.container-fluid>a.btn').click()
        browser.quit()

    def test_f_non_admin_user(self):
        print("Login usuario comun")
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
        browser.get('http://127.0.0.1:5000/login')
        browser.find_element('id', 'username').send_keys("4")
        browser.find_element('id', 'password').send_keys("4")        
        browser.find_element('name', 'submit').click()
        self.assertEqual(browser.title, 'User\'s list' )        
        browser.get("http://127.0.0.1:5000/users_list/new_user")        
        browser.find_element(By.CSS_SELECTOR, 'div.container-fluid>a.btn').click()
        browser.quit()

if __name__ == "__main__":
    unittest.main()


"""
# Buscar en la base
with engine.connect() as connect:
    result = connect.execute(text('SELECT * FROM user WHERE username=\'1\''))
    for row in result:
        print(row[0])
"""

