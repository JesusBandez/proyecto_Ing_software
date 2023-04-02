import unittest
from Tests_Base import Tests_Base, driver, session


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from src import errors
from src.models.Department import Department

class Tests_Login_Selenium(Tests_Base):

    def test_bad_password(self):
        print("Contrasena equivocada")
        with driver() as d:
          d.get(f'{self.home_page}/login')
          d.find_element('id', 'username').send_keys(self.user1_params['username'])
          d.find_element('id', 'password').send_keys(f'{self.user1_params["password"]}5')        
          d.find_element('name', 'submit').click()
          self.assertEqual(d.title, 'Login' )

    def test_non_existent_user(self):
      print("Usuario no existente")
      with driver() as d:
        d.get(f'{self.home_page}/login')
        d.find_element('id', 'username').send_keys('nonexistent')
        d.find_element('id', 'password').send_keys('1')        
        d.find_element('name', 'submit').click()
        self.assertEqual(d.title, 'Login' )  

    def test_login(self):
        print("Login y logout correcto")
        with session(user=self.user1_params) as d:
          self.assertEqual(d.title, 'User details' )  
   

if __name__ == "__main__":
  unittest.main()