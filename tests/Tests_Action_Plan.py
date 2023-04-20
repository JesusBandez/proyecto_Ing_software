import unittest
from Tests_Base import Tests_Base, driver, session
from datetime import datetime

from src.models.User import User
from main import action_plan, action_plan_details,  app


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

if __name__ == "__main__":
  unittest.main()