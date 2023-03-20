import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))
from sqlalchemy import create_engine

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from flask import url_for, session as flask_session

from src.routes.auth import has_role
from src.models import db
from src.models.User import User
from src.models.Project import Project
from src.models.Logger import Logger
from src.models.Client import Client
from src.models.Car import Car
from src.models.Department import Department
from src import errors

from datetime import datetime
from main import user_details,users_list, projects, project_details, logger, clients, client_details, app

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
      self.driver.maximize_window()
      return self.driver

  def __exit__(self,*args):
      self.driver.implicitly_wait(5)
      self.driver.quit()

class session():
    def __init__(self,user=None,**kwargs) -> None:
      self.user   = user
      self.kwargs = kwargs
    def __enter__(self):
      self.d = driver(**self.kwargs).__enter__()
      self.d.get(f'{home_page}/login')
      if self.user:
        self.d.find_element('id', 'username').send_keys(self.user['username'])
        self.d.find_element('id', 'password').send_keys(self.user['password'])        
        self.d.find_element('name', 'submit').click()
      return self.d

    def __exit__(self,*args):
      self.d.__exit__(*args)

unittest.TestLoader.sortTestMethodsUsing = None

app.config['SERVER_NAME'] = 'http://127.0.0.1:5000/'

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
        with app.app_context():
          db.drop_all()
          init_db()

    def tearDown(self):

        with app.app_context():
          db.drop_all()
          init_db()
    
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
    
    '''def test_name_length(self):
      pass 

    def test_last_name_length(self):
      pass 

    def test_role_does_not_exist(self):
      pass

    def test_job_does_not_exist(self):
      pass'''
    
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
        log = Logger('Login')
        db.session.add(log)
        db.session.commit()
        a = logger.removing_event(log.id)
        event = db.session.query(Logger).filter_by(id=a.id)
        self.assertEqual(event.count(),0)
    """


    ''' -------------------------------------------------------
    ----------------------------------------------------------------
    -------------------------------------------------------------------
    CLIENTS TESTS
    ---------------------------------------------------------
    -------------------------------------------------
    ----------------------------------------
    '''
    """
    def test_adding_client_admin(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,db.session.query(Client).filter_by(id=c.id).first())

    def test_adding_client_operation_analyst(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'opera'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,db.session.query(Client).filter_by(id=c.id).first())

    def test_adding_client_user(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,False)

    def test_adding_client_admin_and_editing(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,"25145785","Carlos","Perez",birth_date,"4161234567","carlos@mail.com","Caracas")
        edited_client = clients.adding_client(c.id,"25145785","Carlos","Perez",birth_date,"4142457896","carlosp@mail.com","Municipio Sucre")
        self.assertEqual(c.id,edited_client.id)
        edition = db.session.query(Client).filter_by(id=c.id).first()
        self.assertEqual(edition.phone,"4142457896")
        self.assertEqual(edition.mail,"carlosp@mail.com")
        self.assertEqual(edition.address,"Municipio Sucre")

    def test_adding_client_modifying_repeated_ci(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c1 = clients.adding_client(0,"25145785","Carlos","Perez",birth_date,"4161234567","carlos@mail.com","Caracas")
        c2 = clients.adding_client(0,"21817123","Jose","Perez",birth_date,"4142365871","jose@mail.com","Caracas")
        editing_c2 = clients.editing_client("25145785",c2.id,"Jose","Perez",birth_date,"4142365871","jose@mail.com","Caracas")
        self.assertEqual(editing_c2[0],False)


    def test_removing_client_admin(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,db.session.query(Client).filter_by(id=c.id).first())
        d = clients.removing_client(c.id)
        query = db.session.query(Client).filter_by(id=d.id).first()
        self.assertEqual(query,None)

    def test_removing_client_operator_analyst(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'opera'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,db.session.query(Client).filter_by(id=c.id).first())
        d = clients.removing_client(c.id)
        query = db.session.query(Client).filter_by(id=d.id).first()
        self.assertEqual(query,None)

    def test_removing_client_user(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'opera'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        d = clients.removing_client(c.id)
        self.assertEqual(d,False)

    def test_adding_car(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        client_details.adding_new_car(0,c.id,c,"AZC78E","toyota","corolla",2004,
          16168161616,68848616,"negro","no enciende")
        query = db.session.query(Car).filter_by(serial_car=68848616,serial_engine=16168161616).first()
        self.assertEqual(query.serial_engine,str(16168161616))
        self.assertEqual(query.serial_car,str(68848616))


    def test_removing_car_user(self):
      with app.test_request_context(), app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        car = client_details.adding_new_car(0,c.id,c,"AZC78E","toyota","corolla",2004,
          16168161616,68848616,"negro","no enciende")
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        removed_car = client_details.removing_car(car.license_plate,c.id)
        self.assertEqual(removed_car,False)


    #PRUEBAS CON SELENIUM
    def test_c_login(self):
        print("Login y logout correcto")
        with session(user=self.user1_params) as d:
          self.assertEqual(d.title, 'User details' )

    def test_create_project(self):
        print("Creacion de proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/projects/list')
          d.find_element(By.XPATH, r'//a[@title="Add New Project"]').click()
          self.assertEqual(d.title, 'Add New Project')
          d.find_element('id', 'description').send_keys('Project 1')
          self.assertEqual(d.title, 'Add New Project' )

    def test_add_user_to_project(self):
        print("Se agregan usuarios al proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/projects/project_details?id=1')
          d.find_element(By.XPATH, r"//a[@id='addUser']").click()
          self.assertEqual(d.title, 'Manage Project')

    def test_delete_user_in_project(self):
        print("Se eliminan usuarios del proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{home_page}/projects/project_details?id=1')
          d.find_element(By.XPATH, r"//a[@id='removeUser']").click()
          self.assertEqual(d.title, 'Manage Project' )

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
    

    def test_unauthorized_add_department(self):
      "Agregar departamento sin ser admin"
      # Crear el departamento    
      with session() as sesion:
        sesion.get(f'{home_page}/departments/new_department')

        # Comprobar que se muestra el modal con el error de autorizacion
        mensaje_en_modal = sesion.find_element(
            By.CSS_SELECTOR, r'.modal-body').get_attribute("innerHTML").strip()
        self.assertEqual(
          mensaje_en_modal,
          errors.ErrorType(errors.ERROR_MUST_BE_ADMIN_ADD_DEPARTMENT).description
          )

    def test_add_department(self):
      "Agregar departamento"
      # Crear el departamento
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{home_page}/departments/list')
        sesion.find_element(By.ID, 'addButton').click()
        sesion.find_element(By.ID, 'description').send_keys('Aire')
        sesion.find_element(By.NAME, 'submit').click()

        # Comprobar que existe en la base
        with app.app_context():
          department = db.session.query(Department).filter_by(
            description='Aire'
          ).first()
          self.assertTrue(department)

    def test_edit_department(self):
      "Editar departamento"

      # Buscar el departamento a editar
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{home_page}/departments/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Edit department"][value="1"]').click()
        sesion.find_element(By.ID, 'description').send_keys(' 2345')
        sesion.find_element(By.NAME, 'submit').click()

        # Comprobar que se ha editado
        with app.app_context():
          department = db.session.query(Department).filter_by(
            description='Latoneria 2345'
          ).first()
          self.assertTrue(department)

    def test_remove_department(self):
      "Eliminar departamento"
      # Buscar el departamento a eliminar
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{home_page}/departments/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Remove department"][value="1"]').click()
        # Comprobar que se ha eliminado el departamento
        with app.app_context():
          department = db.session.query(Department).filter_by(
            id='1'
          ).first()
          self.assertFalse(department)

    def test_search_department(self):
      "Busqueda de departamentos"

      # Buscar el departamento a eliminar
      with session() as sesion:
        sesion.get(f'{home_page}/departments/list')
        sesion.find_element(By.CSS_SELECTOR, r'[type="search"]').send_keys('La')
        select = Select(sesion.find_element(By.CSS_SELECTOR, r'[name="typeSearch"]'))
        select.select_by_value("description")
        sesion.find_element(By.CSS_SELECTOR, r'[type="submit"]').click()
        # Comprobar que se han filtrado los departamentos
        departments = sesion.find_elements(By.CSS_SELECTOR, r'table tbody tr')
        self.assertEqual(len(departments), 2)
    
if __name__ == "__main__":
    unittest.main()


"""
# Buscar en la base
with engine.connect() as connect:
    result = connect.execute(text('SELECT * FROM user WHERE username=\'1\''))
    for row in result:
        print(row[0])
"""

