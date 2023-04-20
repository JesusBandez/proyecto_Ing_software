import unittest
from Tests_Base import Tests_Base, session
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

from main import action_plan, action_plan_details,  app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

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
    
    def test_add_action_plan(self):
      "Agregar action plan"
      # Crear el action plan
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()

        add_button = sesion.find_element(By.CSS_SELECTOR, r"[title='Register new action plan']")
        sesion.execute_script("arguments[0].scrollIntoView();", add_button)
        sleep(0.9)

        add_button.click()
        sesion.find_element(By.ID, 'action').send_keys('testing')
        sesion.find_element(By.ID, 'activity').send_keys('testing')
        sesion.find_element(By.ID, 's_date').send_keys("2009-05-05")
        sesion.find_element(By.ID, 'c_date').send_keys('2009-05-05')
        sesion.find_element(By.NAME, "quantity").send_keys('2.0')
        sesion.find_element(By.CSS_SELECTOR, r'[data-bs-toggle="modal"]').click()
        sesion.find_element(By.CSS_SELECTOR, r'tbody tr input[id="1"]').click()
        sleep(0.9)
        sesion.find_element(By.CSS_SELECTOR, r'.btn-primary[data-bs-dismiss="modal"]').click()   
        sleep(0.9)
        sesion.find_element(By.CSS_SELECTOR, r'input.btn').click()

        # Comprobar que existe en la base
        plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='actionplans'] tbody td")

        self.assertTrue(any(
          plan.get_attribute("innerHTML").strip()=='testing' for plan in plans))


    def test_edit_action_plan(self):
      "Editar action plan"
      # Editar el action plan
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()

        add_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Edit the action_plan"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", add_button)
        sleep(0.9)

        add_button.click()

        sesion.find_element(By.ID, 'action').clear()
        sesion.find_element(By.ID, 'action').send_keys('edited')

        sesion.find_element(By.ID, 'activity').clear()
        sesion.find_element(By.ID, 'activity').send_keys('edited')
        sesion.find_element(By.CSS_SELECTOR, r'input.btn').click()

        # Comprobar que existe en la base
        plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='actionplans'] tbody td")

        self.assertTrue(any(
          plan.get_attribute("innerHTML").strip()=='edited' for plan in plans))

    def test_search_action_plan(self):
      "Busqueda de action plan"

      # Dar a la busqueda
      with session() as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="2"]').click()

        sesion.find_element(By.CSS_SELECTOR, r'[type="search"]').send_keys('Lija')
        select = Select(sesion.find_element(By.CSS_SELECTOR, r'[name="typeSearch"]'))
        select.select_by_value("activity")

        button = sesion.find_element(By.CSS_SELECTOR, r'[type="submit"]')
        sesion.execute_script("arguments[0].scrollIntoView();", button)
        sleep(0.9)        
        button.click()

        # Comprobar que se han filtrado las medidas
        plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='actionplans'] tbody tr")
        self.assertEqual(len(plans), 1)        

if __name__ == "__main__":
  unittest.main()