import os
import sys
sys.path.append(os.path.abspath('..'))
from sqlalchemy import create_engine
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.models import db
from src.routes.auth import has_role
from flask import url_for, session as flask_session

from src.models.User import User
from src.models.Project import Project
from src.models.Logger import Logger

from datetime import datetime

from main import user_details,users_list, projects, project_details, logger

from main import app
from manage import init_db


engine = create_engine("sqlite:///instance/database.db")
home_page = "http://127.0.0.1:5000"

class driver():
  def __init__(self,browser = 'chrome',**kwargs) -> None:
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
app.config['SERVER_NAME'] = 'http://127.0.0.1:5000/'

appCont = app.app_context() 

class tests(unittest.TestCase):

    def setUp(self):
        self.user1_params = {
          'first_name': 'fadmin',
          'last_name': 'ladmin',
          'username': '2',
          'password': '2',
          'role': 'admin',
          'job': 'Enginer', 
        }

        with appCont:
          init_db()

    def tearDown(self):
        with app.app_context():
          db.drop_all()
    
    def test_create_user_duplicated_username_db(self):
      with app.app_context():
        user = users_list.create_user("Maria", "Perez","mperez", "1234567", "admin", "Administrator")
        self.assertEqual(user[0],db.session.query(User).filter_by(username="mperez").first())
        user = users_list.create_user("Mario", "Perez","mperez", "486486", "user", "Social")
        self.assertEqual(user[1],False)   #da False cuando el usuario no se pudo registrar 
        user1 = db.session.query(User).filter_by(username="mperez").first()
        deleted = users_list.deleting(user1.id)
        user_not_found = db.session.query(User).filter_by(username="mperez").first()
        self.assertEqual(user_not_found,None)

    def test_password_length(self):
      with app.app_context():
        user = users_list.create_user("Maria", "Perez","mperez", "", "admin", "Administrator") 

    def test_name_length(self):
      pass 

    def test_last_name_length(self):
      pass 

    def test_role_does_not_exist(self):
      pass

    def test_job_does_not_exist(self):
      pass

    def test_create_delete_user(self):
      with app.app_context():
        user = users_list.create_user("Maria", "Perez","mperez", "1234567", "admin", "Administrator")
        self.assertEqual(user[0],db.session.query(User).filter_by(username="mperez").first())
        user_deletion = users_list.deleting(user[0].id)
        deleted = db.session.query(User).filter_by(id=user_deletion[1].id).first()
        self.assertEqual(None,deleted)

    def test_create_project(self):
      with app.app_context():
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        self.assertEqual(project,db.session.query(Project).filter_by(description=description).first())

    def test_create_and_remove_project(self):
      with app.app_context():
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        self.assertEqual(project,db.session.query(Project).filter_by(description=description).first())
        project_removed = projects.removing_project(project.id)
        self.assertEqual(None,db.session.query(Project).filter_by(id=project_removed.id).first())

    def test_project_availability(self):
      with app.app_context():
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        before_availability = project.available
        current_project = projects.change_availability(project.id)
        self.assertEqual(project.id, current_project.id)
        search = db.session.query(Project).filter_by(id=current_project.id).first()
        self.assertEqual(before_availability, not search.available)

    def test_edit_project_manager(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        manager_id_before = project.manager_id
        self.assertEqual(manager_id_before,None)
        project_new_manager = project_details.editing_manager(project.id,1)
        self.assertEqual(project_new_manager.manager_id,1)

    def test_remove_project_manager(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        manager_id_before = project.manager_id
        self.assertEqual(manager_id_before,None)
        project_new_manager = project_details.editing_manager(project.id,1)
        self.assertEqual(project_new_manager.manager_id,1)
        project_manager_removed = project_details.removing_manager(project_new_manager.id)
        self.assertEqual(project_new_manager.manager_id,None)

    def test_add_user_project(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        project_changed = project_details.adding_user_to_project(project.id,2)
        user = None
        for users in project_changed.users:
          if users.id == 2:
            self.assertEqual(users.id,2)
            break

    def test_remove_user_project(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        project_changed = project_details.adding_user_to_project(project.id,2)
        removed = project_details.removing_user_from_project(project_changed.id,2)
        self.assertEqual(len(removed.users),0)

    def test_adding_user_project_no_admin(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        project_changed = project_details.adding_user_to_project(project.id,2)
        self.assertEqual(project_changed,False)

    def test_removing_user_project_no_admin(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date)
        project_changed = project_details.removing_user_from_project(project.id,2)
        self.assertEqual(project_changed,False)

    def test_getting_user_projects(self):
        with app.test_request_context(), app.test_client() as c:
          flask_session['user'] = {
                  'id' : '1',
                  'username' : '1',
                  'role' : 'user'
              }
          get = user_details.user_projects(1)
          self.assertEqual(get[1],db.session.query(User).filter_by(id=1).first())

    def test_removing_event(self):
      with app.test_request_context():
        time_data = datetime.now()
        date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
        hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
        log = Logger('Login', date, hour)
        db.session.add(log)
        db.session.commit()
        a = logger.removing_event(log.id)
        event = db.session.query(Logger).filter_by(id=a.id)
        self.assertEqual(event.count(),0)

    def test_c_login(self):
        print("Login y logout correcto")
        with session(user=self.user1_params) as d:
          self.assertEqual(d.title, 'User details' )

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

