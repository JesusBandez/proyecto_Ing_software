import unittest
from Tests_Base import Tests_Base, driver, session
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from src import errors
from src.models.Department import Department

class Tests_Departments_Selenium(Tests_Base):

    def test_unauthorized_add_department(self):
      "Agregar departamento sin ser admin"
      # Crear el departamento    
      with session() as sesion:
        sesion.get(f'{self.home_page}/departments/new_department')

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
        sesion.get(f'{self.home_page}/departments/list')
        sesion.find_element(By.ID, 'addButton').click()
        sesion.find_element(By.ID, 'description').send_keys('Aire')
        sesion.find_element(By.NAME, 'submit').click()
        
        # Comprobar que existe en la base
        departments = sesion.find_elements(By.CSS_SELECTOR, 'tbody td')

        self.assertTrue(any(department.get_attribute("innerHTML").strip()=='Aire' for department in departments))

    def test_edit_department(self):
      "Editar departamento"

      # Buscar el departamento a editar
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/departments/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Edit department"][value="1"]').click()
        sesion.find_element(By.ID, 'description').send_keys(' 2345')
        sesion.find_element(By.NAME, 'submit').click()
        
        # Comprobar que se ha editado
        departments = sesion.find_elements(By.CSS_SELECTOR, 'tbody td')
        self.assertTrue(any(
          department.get_attribute("innerHTML").strip()=='Latoneria 2345' for department in departments))
        

    def test_remove_department(self):
      "Eliminar departamento"
      # Buscar el departamento a eliminar
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/departments/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Remove department"][value="1"]').click()
        
        # Comprobar que se ha eliminado el departamento
        departments = sesion.find_elements(By.CSS_SELECTOR, 'tbody td')
        self.assertTrue(all(
            department.get_attribute("innerHTML").strip()!='1' for department in departments
          ))

    def test_search_department(self):
      "Busqueda de departamentos"

      # Buscar el departamento a eliminar
      with session() as sesion:
        sesion.get(f'{self.home_page}/departments/list')
        sesion.find_element(By.CSS_SELECTOR, r'[type="search"]').send_keys('ca')
        select = Select(sesion.find_element(By.CSS_SELECTOR, r'[name="typeSearch"]'))
        select.select_by_value("description")
        sesion.find_element(By.CSS_SELECTOR, r'[type="submit"]').click()
        
        # Comprobar que se han filtrado los departamentos
        departments = sesion.find_elements(By.CSS_SELECTOR, r'table tbody tr')
        self.assertEqual(len(departments), 1)
    

if __name__ == "__main__":
  unittest.main()