import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))

from selenium import webdriver
from main import app
from src.models import db
from manage import init_db
import requests

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


class Tests_Base(unittest.TestCase):
    app = app
    db = db
    home_page = home_page

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
        requests.get(f'{home_page}/restart_bbdd')
    def tearDown(self):

        with app.app_context():
          db.drop_all()
          init_db()
        requests.get(f'{home_page}/restart_bbdd')


