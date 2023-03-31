import unittest
from Tests_Base import Tests_Base, driver, session
from flask import session as flask_session
from src.models.User import User
from main import projects, project_details, user_details, app
from selenium.webdriver.common.by import By
from src.models.Project import Project

from datetime import datetime

import time

class Tests_Project(Tests_Base):

    def test_create_project(self):
      with app.app_context():
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
        self.assertEqual(project,self.db.session.query(Project).filter_by(description=description).first())

    def test_create_and_remove_project(self):
      with app.app_context():
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Reparaciones","2","Cambio de aceite",
          "Cambiar aceite",400,"")
        self.assertEqual(project,self.db.session.query(Project).filter_by(description=description).first())
        project_removed = projects.removing_project(project.id)
        self.assertEqual(None,self.db.session.query(Project).filter_by(id=project_removed.id).first())

    def test_project_availability(self):
      with app.app_context():
        description = "Nuevo proyecto"
        start_date = datetime.strptime("2022-12-15", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-04-20", r'%Y-%m-%d')
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
        before_availability = project.available
        current_project = projects.change_availability(project.id)
        self.assertEqual(project.id, current_project.id)
        search = self.db.session.query(Project).filter_by(id=current_project.id).first()
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
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
        manager_id_before = project.manager_id
        self.assertEqual(manager_id_before,2)
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
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
        manager_id_before = project.manager_id
        self.assertEqual(manager_id_before,2)
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
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
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
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
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
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
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
        project = projects.adding_new_project(False, description, start_date, close_date,"ASD14XZ","Painting","2","Pintar color negro",
          "Pintar",100,"")
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
          self.assertEqual(get[1],self.db.session.query(User).filter_by(id=1).first())


class Tests_Project_Selenium(Tests_Base):
    
    def test_create_project(self):
        print("Creacion de proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{self.home_page}/projects/list')
          d.find_element(By.XPATH, r'//a[@title="Add New Project"]').click()
          self.assertEqual(d.title, 'Add New Project')
          d.find_element('id', 'description').send_keys('Project 1')
          self.assertEqual(d.title, 'Add New Project' )

    def test_add_user_to_project(self):
        print("Se agregan usuarios al proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{self.home_page}/projects/project_details?id=1')
          d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(2)
          d.find_element(By.XPATH, r"//a[@id='addUser']").click()
          self.assertEqual(d.title, 'Manage Project')

    def test_delete_user_in_project(self):
        print("Se eliminan usuarios del proyecto")
        with session(user=self.user1_params) as d:
          d.get(f'{self.home_page}/projects/project_details?id=1')
          d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(2)
          d.find_element(By.XPATH, r"//a[@id='removeUser']").click()
          self.assertEqual(d.title, 'Manage Project' )

    def test_delete_project(self):
        print("Eliminar proyecto de usuario")
        with session(user=self.user1_params) as d:
          d.get(f'{self.home_page}/projects/list')
          d.find_element(By.XPATH, r"//button[@title='Remove project']")
          self.assertEqual(d.title, 'Projects list' ) 

if __name__ == "__main__":
  unittest.main()