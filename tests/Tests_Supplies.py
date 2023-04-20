import unittest
from Tests_Base import Tests_Base, session
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

from main import action_plan, action_plan_details,  app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from time import sleep

class Tests_supply_Selenium(Tests_Base):
        
    def test_remove_supply(self):
      "Eliminar Supply"
      # Buscar el supply a eliminar
      user = {'username': '1', 'password': '1'}
      
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
        details_button.click()

        remove_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Delete Supply"][value="6"]')
        sesion.execute_script("arguments[0].scrollIntoView();", remove_button)
        sleep(0.7)
        remove_button.click()

        # Comprobar que se ha eliminado el human talent
        action_plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='supplies'] tbody tr")

        self.assertTrue(len(action_plans)==1)
    
    def test_add_supply(self):
      "Agregar un supply"
      # Crear el suppy
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
        details_button.click()

        add_button = sesion.find_element(By.CSS_SELECTOR, r"[title='Register new supply']")
        sesion.execute_script("arguments[0].scrollIntoView();", add_button)
        sleep(0.7)
        add_button.click()


        sesion.find_element(By.ID, 'action').send_keys('testing')
        sesion.find_element(By.ID, 'activity').send_keys('testing')
        sesion.find_element(By.ID, 'description').send_keys('testing')
        sesion.find_element(By.ID, 'category').send_keys('testing')
        sesion.find_element(By.NAME, "quantity").send_keys('2.0')
        sesion.find_element(By.NAME, "cost").send_keys('2.0')

        # Select measure
        sesion.find_elements(By.CSS_SELECTOR, r'[data-bs-toggle="modal"]')[0].click()
        sesion.find_elements(By.CSS_SELECTOR, r'tbody tr input[id="1"]')[0].click()
        sleep(0.9)
        sesion.find_elements(By.CSS_SELECTOR, r'.btn-primary[data-bs-dismiss="modal"]')[0].click()   
        sleep(0.9)

        # Select responsible
        sesion.find_elements(By.CSS_SELECTOR, r'[data-bs-toggle="modal"]')[1].click()
        sesion.find_elements(By.CSS_SELECTOR, r'tbody tr input[id="1"]')[1].click()
        sleep(0.9)
        sesion.find_elements(By.CSS_SELECTOR, r'.btn-primary[data-bs-dismiss="modal"]')[1].click()   
        sleep(0.9)

        submit = sesion.find_element(By.CSS_SELECTOR, r"input.btn")
        sesion.execute_script("arguments[0].scrollIntoView();", submit)
        sleep(0.9)
        submit.click()

        # Comprobar que existe en la base
        supplies = sesion.find_elements(By.CSS_SELECTOR, r"div[name='supplies'] tbody td")
        self.assertTrue(any(
          supply.get_attribute("innerHTML").strip()=='testing' for supply in supplies))


    def test_edit_supply(self):
      "editar un supply"
      # editar el suppy
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
        details_button.click()

        Edit_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Edit Supply"][value="6"]')
        sesion.execute_script("arguments[0].scrollIntoView();", Edit_button)
        sleep(0.7)
        Edit_button.click()


        sesion.find_element(By.ID, 'action').clear()
        sesion.find_element(By.ID, 'action').send_keys('edited')
        sesion.find_element(By.ID, 'activity').clear()
        sesion.find_element(By.ID, 'activity').send_keys('edited')

        submit = sesion.find_element(By.CSS_SELECTOR, r"input.btn")
        sesion.execute_script("arguments[0].scrollIntoView();", submit)
        sleep(0.9)
        submit.click()

        # Comprobar que existe en la base
        supplies = sesion.find_elements(By.CSS_SELECTOR, r"div[name='supplies'] tbody td")
        self.assertTrue(any(
          supply.get_attribute("innerHTML").strip()=='edited' for supply in supplies))

    def test_search_supply(self):
      "Busqueda de supply"

      # Dar a la busqueda
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
       
        details_button.click()

        search = sesion.find_elements(By.CSS_SELECTOR, r'[type="search"]')[1]
        sesion.execute_script("arguments[0].scrollIntoView();", search)
        sleep(0.7)
        search.send_keys('Herramienta')
        select = Select(sesion.find_elements(By.CSS_SELECTOR, r'[name="typeSearch"]')[1])
        select.select_by_value("category")

        button = sesion.find_elements(By.CSS_SELECTOR, r'[type="submit"]')[1]
        sesion.execute_script("arguments[0].scrollIntoView();", button)
        sleep(0.9)        
        button.click()

        # Comprobar que se han filtrado las medidas
        plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='supplies'] tbody tr")
        self.assertEqual(len(plans), 1)        

if __name__ == "__main__":
  unittest.main()