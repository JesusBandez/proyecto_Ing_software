import unittest
from Tests_Base import Tests_Base, session
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

from main import action_plan, action_plan_details,  app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from time import sleep

class Tests_Human_Talent_Selenium(Tests_Base):
        
    def test_remove_human_talent(self):
      "Eliminar human talent"
      # Buscar el human talent a eliminar
      user = {'username': '1', 'password': '1'}
      
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
        details_button.click()

        remove_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Delete Human Talent"][value="5"]')
        sesion.execute_script("arguments[0].scrollIntoView();", remove_button)
        sleep(0.7)
        remove_button.click()

        # Comprobar que se ha eliminado el human talent
        action_plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='human_talent'] tbody tr")

        self.assertTrue(len(action_plans)==1)
    
    def test_add_human_talent(self):
      "Agregar ahuman_talent"
      # Crear el human_talent
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
        details_button.click()

        add_button = sesion.find_element(By.CSS_SELECTOR, r"[title='Register new Human Talent']")
        sesion.execute_script("arguments[0].scrollIntoView();", add_button)
        sleep(0.7)
        add_button.click()


        sesion.find_element(By.ID, 'action').send_keys('testing')
        sesion.find_element(By.ID, 'activity').send_keys('testing')
        sesion.find_element(By.NAME, "time").send_keys('2.0')
        sesion.find_element(By.NAME, "quantity").send_keys('2.0')
        # Select responsible
        sesion.find_element(By.CSS_SELECTOR, r'[data-bs-toggle="modal"]').click()
        sesion.find_element(By.CSS_SELECTOR, r'tbody tr input[id="1"]').click()
        sleep(0.9)
        sesion.find_element(By.CSS_SELECTOR, r'.btn-primary[data-bs-dismiss="modal"]').click()   
        sleep(0.9)
        sesion.find_element(By.NAME, "cost").send_keys('3.0')

        submit = sesion.find_element(By.CSS_SELECTOR, r"input.btn")
        sesion.execute_script("arguments[0].scrollIntoView();", submit)
        sleep(0.9)
        submit.click()

        # Comprobar que existe en la base
        humans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='human_talent'] tbody td")
        self.assertTrue(any(
          human.get_attribute("innerHTML").strip()=='testing' for human in humans))


    def test_edit_human_talent(self):
      "Editar ahuman_talent"
      # Editarlo el human_talent
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
        details_button.click()

        Edit_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Edit Human Talent"][value="5"]')
        sesion.execute_script("arguments[0].scrollIntoView();", Edit_button)
        sleep(0.7)
        Edit_button.click()


        sesion.find_element(By.ID, 'action').clear()
        sesion.find_element(By.ID, 'action').send_keys('edited')
        sesion.find_element(By.ID, 'activity').clear()
        sesion.find_element(By.ID, 'activity').send_keys('testing')       

        submit = sesion.find_element(By.CSS_SELECTOR, r"input.btn")
        sesion.execute_script("arguments[0].scrollIntoView();", submit)
        sleep(0.9)
        submit.click()

        # Comprobar que existe en la base
        humans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='human_talent'] tbody td")
        self.assertTrue(any(
          human.get_attribute("innerHTML").strip()=='edited' for human in humans))

    def test_search_human_talent(self):
      "Busqueda de action plan"

      # Dar a la busqueda
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/projects/list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Project Details"][value="1"]').click()
        details_button = sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="View plan details"][value="3"]')
        sesion.execute_script("arguments[0].scrollIntoView();", details_button)
        sleep(0.7)
       
        details_button.click()

        search = sesion.find_elements(By.CSS_SELECTOR, r'[type="search"]')[0]
        sesion.execute_script("arguments[0].scrollIntoView();", search)
        sleep(0.7)
        search.send_keys('Dejar')
        select = Select(sesion.find_elements(By.CSS_SELECTOR, r'[name="typeSearch"]')[0])
        select.select_by_value("activity")

        button = sesion.find_elements(By.CSS_SELECTOR, r'[type="submit"]')[0]
        sesion.execute_script("arguments[0].scrollIntoView();", button)
        sleep(0.9)        
        button.click()

        # Comprobar que se han filtrado las medidas
        plans = sesion.find_elements(By.CSS_SELECTOR, r"div[name='human_talent'] tbody tr")
        self.assertEqual(len(plans), 1)        

if __name__ == "__main__":
  unittest.main()