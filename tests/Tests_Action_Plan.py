import unittest
from Tests_Base import Tests_Base, session
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

from main import action_plan, action_plan_details,  app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep

#action plan
#create_action_plan(action, activity, start_date, close_date, quantity, responsible, project) return [action_plan,True]
#deleting(action_plan_id) return [log,action_plan]

#actionplan detail
#searchSupplies(typeS,search,plan_id) 
#searchTalents(typeS,search,plan_id):
class Tests_Action_Plan_Unit(Tests_Base):

    def test_create_action_plan(self):
      with app.app_context():
        start_date = datetime.strptime("2023-01-12", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-01-14", r'%Y-%m-%d')
        AP = action_plan.create_action_plan("Arreglar carro", "Cambiar aceite", start_date, close_date, 1, 1, 2)
        self.assertEqual(AP[1],True)
        deleted = action_plan.deleting(AP[0].id)
        self.assertEqual(deleted[1].id,AP[0].id)
        
    def test_search_supplies(self):
      with app.app_context():
        start_date = datetime.strptime("2023-01-12", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-01-14", r'%Y-%m-%d')
        AP = action_plan.create_action_plan("Arreglar carro", "Cambiar aceite", start_date, close_date, 1, 1, 2)
        self.assertEqual(AP[1],True)
        s = action_plan_details.searchSupplies("action-s","Arreglar",AP[0].id)
        self.assertNotEqual(s,[])

    def test_search_talents(self):
      with app.app_context():
        start_date = datetime.strptime("2023-01-12", r'%Y-%m-%d')
        close_date = datetime.strptime("2023-01-14", r'%Y-%m-%d')
        AP = action_plan.create_action_plan("Arreglar carro", "Cambiar aceite", start_date, close_date, 1, 1, 2)
        self.assertEqual(AP[1],True)
        x = action_plan_details.searchTalents("action","Arreglar",AP[0].id)
        self.assertNotEqual(x,[])


class Tests_Action_Plan_Selenium(Tests_Base):
        
    def test_remove_action_plan(self):
      "Eliminar action plan"
      # Buscar el plan a eliminar
      user = {'username': '1', 'password': '1'}
      
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        remove_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Delete action plan"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", remove_button)
        sleep(0.7)
        remove_button.click()
        # Comprobar que se ha eliminado el plan
        action_plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='actionplans'] tbody td")
  
        self.assertTrue(any(
          action_plan.get_attribute("innerHTML").strip()=='Empty list' for action_plan in action_plans))
    
    def test_add_measure(self):
      "Agregar medida"
      # Crear el medida
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/measures_list')
        sesion.find_element(By.CSS_SELECTOR, r"[title='Register new measure']").click()
        sesion.find_element(By.ID, 'dimension').send_keys('9')
        sesion.find_element(By.ID, 'unit').send_keys('Kg')
        sesion.find_element(By.CSS_SELECTOR, r'input.btn').click()
        
        # Comprobar que existe en la base
        departments = sesion.find_elements(By.CSS_SELECTOR, 'tbody td')

        self.assertTrue(any(
          department.get_attribute("innerHTML").strip()=='9' for department in departments))

        self.assertTrue(any(           
          department.get_attribute("innerHTML").strip()=='Kg' for department in departments))

    def test_edit_measure(self):
      "Editar medida"
      # Crear el medida
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/measures_list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Edit the measure"][value="1"]').click()
        sesion.find_element(By.ID, 'dimension').clear()
        sesion.find_element(By.ID, 'dimension').send_keys('9')
        sesion.find_element(By.ID, 'unit').clear()
        sesion.find_element(By.ID, 'unit').send_keys('Kg')
        sesion.find_element(By.CSS_SELECTOR, r'input.btn').click()
        
        # Comprobar que existe en la base
        departments = sesion.find_elements(By.CSS_SELECTOR, 'tbody td')
        
        self.assertTrue(any(
          department.get_attribute("innerHTML").strip()=='9' for department in departments))

        self.assertTrue(any(           
          department.get_attribute("innerHTML").strip()=='Kg' for department in departments))

    def test_search_measures(self):
      "Busqueda de departamentos"

      # Dar a la busqueda
      with session() as sesion:
        sesion.get(f'{self.home_page}/measures_list')
        sesion.find_element(By.CSS_SELECTOR, r'[type="search"]').send_keys('8')
        select = Select(sesion.find_element(By.CSS_SELECTOR, r'[name="typeSearch"]'))
        select.select_by_value("dimension")
        sesion.find_element(By.CSS_SELECTOR, r'[type="submit"]').click()
        
        # Comprobar que se han filtrado las medidas
        measures = sesion.find_elements(By.CSS_SELECTOR, r'table tbody tr')
        self.assertEqual(len(measures), 1)        

if __name__ == "__main__":
  unittest.main()