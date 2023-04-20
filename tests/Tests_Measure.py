import unittest
from Tests_Base import Tests_Base, session


from main import measures,  app

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
#create_measure(dimension, unit)   return [measure,True]
#verify_measure_exist(guser_id, dimension, unit)   true o false
#deleting(measure_id)  return [log,measure]
class Tests_Measures_Unit(Tests_Base):

    def test_create_and_delete_measure(self):
      with app.app_context():
        unit = measures.create_measure(1024, "centimeters")
        verified = measures.verify_measure_exist(unit[0].id, unit[0].dimension, unit[0].unit)
        self.assertEqual(verified,True)
        deleted = measures.deleting(unit[0].id)
        verified_deleted = measures.verify_measure_exist(deleted[1].id, deleted[1].dimension, deleted[1].unit)
        self.assertEqual(verified_deleted,False)
        verified_del = measures.verify_measure_exist(unit[0].id, unit[0].dimension, unit[0].unit)
        self.assertEqual(verified_del,False)

    def test_verify_nonexistent_measure(self):
      with app.app_context():
        verify = measures.verify_measure_exist(100, 7182, "km")
        self.assertEqual(verify,False)

class Tests_Measures_Selenium(Tests_Base):
        
    def test_remove_measure(self):
      "Eliminar measure"
      # Buscar el departamento a eliminar
      user = {'username': '1', 'password': '1'}
      with session(user) as sesion:
        sesion.get(f'{self.home_page}/measures_list')
        sesion.find_element(By.CSS_SELECTOR, r'[name="id"][title="Delete measure"][value="1"]').click()
        
        # Comprobar que se ha eliminado el measure
        departments = sesion.find_elements(By.CSS_SELECTOR, 'tbody td')
        self.assertTrue(all(
            department.get_attribute("innerHTML").strip()!='1' for department in departments
          ))
    
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