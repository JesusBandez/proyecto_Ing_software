import os
import sys
sys.path.append(os.path.abspath('..'))
from sqlalchemy import create_engine
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.models import db
from main import app
from manage import init_db


engine = create_engine("sqlite:///instance/database.db")
home_page = "http://127.0.0.1:5000"

class driver():
  def __init__(self,browser = 'firefox',**kwargs) -> None:
      self.browser_name = browser
      self.kwargs       = kwargs
  def __enter__(self):
      if (self.browser_name == 'edge'):
        self.driver = webdriver.Edge(**self.kwargs)
      if (self.browser_name == 'chrome'):
        self.driver = webdriver.Chrome(**self.kwargs)
      if (self.browser_name == 'firefox'):
        self.driver = webdriver.Firefox(**self.kwargs)
      return self.driver

  def __exit__(self,*args):
      self.driver.implicitly_wait(5)
      self.driver.quit()

class session():
    def __init__(self,user,**kwargs) -> None:
      self.user   = user
      self.kwargs = kwargs
    def __enter__(self):
      self.d = driver(**self.kwargs).__enter__()
      self.d.get(f'{home_page}/login')
      self.d.find_element('id', 'username').send_keys(self.user['username'])
      self.d.find_element('id', 'password').send_keys(self.user['password'])        
      self.d.find_element('name', 'submit').click()
      return self.d

    def __exit__(self,*args):
      self.d.__exit__(*args)

unittest.TestLoader.sortTestMethodsUsing = None
# Estas pruebas son realizadas con el navegador Edge. Se necesita
# selenium y el driver geckodriver para poder iniciarlas

class tests(unittest.TestCase):

    def setUp(self):
        self.user1_params = {
          'first_name': 'fadmin',
          'last_name': 'ladmin',
          'username': '1',
          'password': '1',
          'role': 'admin',
          'job': 'Enginer', 
        }

        with app.app_context():
          init_db()

    def tearDown(self):
        with app.app_context():
          db.drop_all()

    def test_c_login(self):
        print("Login y logout correcto")
        with session(user=self.user1_params) as d:
          self.assertEqual(d.title, 'User details' )

    #agregar realmente un proyecto
    #agregar usuarios a un proyecto

    def test_create_project(self):
        print("Creacion de proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/projects/list')
          d.find_element(By.XPATH, r"//a[@id='addButton']").click()
          self.assertEqual(d.title, 'Add New Project')
          d.find_element('id', 'description').send_keys('Project 1')
          self.assertEqual(d.title, 'Add New Project' )

    def test_add_user_to_project(self):
        print("Se agregan usuarios al proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/projects/project_details?id=1')
          d.find_element(By.XPATH, r"//a[@id='addUser']").click()
          self.assertEqual(d.title, 'Manage project')

    def test_delete_user_in_project(self):
        print("Se eliminan usuarios del proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/projects/project_details?id=1')
          d.find_element(By.XPATH, r"//a[@id='removeUser']").click()
          self.assertEqual(d.title, 'Manage project' )

    def test_delete_project(self):
        print("Eliminar proyecto de usuario")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/projects/list')
          d.find_element(By.XPATH, r"//button[@title='Remove project']")
          self.assertEqual(d.title, 'Projects list' ) 

    def test_b_bad_password(self):
        print("Contrasena equivocada")
        with driver() as d:
          d.get(f'{home_page}/login')
          d.find_element('id', 'username').send_keys(self.user1_params['username'])
          d.find_element('id', 'password').send_keys(f'{self.user1_params["password"]}5')        
          d.find_element('name', 'submit').click()
          self.assertEqual(d.title, 'Login' )

    def test_a_non_existent_user(self):
      print("Usuario no existente")
      with driver() as d:
        d.get(f'{home_page}/login')
        d.find_element('id', 'username').send_keys('nonexistent')
        d.find_element('id', 'password').send_keys('1')        
        d.find_element('name', 'submit').click()
        self.assertEqual(d.title, 'Login' )       
    
    def test_d_delete_user(self):
        print("Borrar usuario")
        with session(user=self.user1_params) as d:
           d.get(f'{home_page}/users_list')
           button = d.find_elements(By.NAME,'id')[-1]
           value = button.get_attribute('value')
           button.click()
           new_values = [b.get_attribute('value') for b in d.find_elements(By.NAME,'id')]
           self.assertNotIn(value,new_values)

    def test_e_add_user_admin(self):
        print("Agregar usuario")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/users_list')
          number_users_before = len(d.find_elements(By.CSS_SELECTOR, 'tr'))
          self.assertNotEqual(number_users_before,0)
          d.get(f'{home_page}/users_list/new_user')
          d.find_element('id', 'username').send_keys("10")
          d.find_element('id', 'password').send_keys("10")
          d.find_element('id', 'f_name').send_keys("10")
          d.find_element('id', 'l_name').send_keys("10")
          d.find_element('id', 'job').send_keys("10")   
          d.find_element('name', 'submit').click()
          d.get(f'{home_page}/users_list')
          number_users_after = len(d.find_elements(By.CSS_SELECTOR, 'tr'))
          self.assertLess(number_users_before,number_users_after)

if __name__ == "__main__":
    unittest.main()


"""
# Buscar en la base
with engine.connect() as connect:
    result = connect.execute(text('SELECT * FROM user WHERE username=\'1\''))
    for row in result:
        print(row[0])
"""

