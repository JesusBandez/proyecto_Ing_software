import unittest
from Tests_Base import Tests_Base, driver, session

from src.models.User import User
from main import users_list,  app



class Tests_Users_Unit(Tests_Base):

    def test_create_user_duplicated_username_db(self):
      with app.app_context():
        user = users_list.create_user("Maria", "Perez","mperez", "1234567", "admin", "Administrator")
        self.assertEqual(user[0],self.db.session.query(User).filter_by(username="mperez").first())
        user = users_list.create_user("Mario", "Perez","mperez", "486486", "user", "Social")
        self.assertEqual(user[1],False)   #da False cuando el usuario no se pudo registrar 
        user1 = self.db.session.query(User).filter_by(username="mperez").first()
        deleted = users_list.deleting(user1.id)
        user_not_found = self.db.session.query(User).filter_by(username="mperez").first()
        self.assertEqual(user_not_found,None)

    def test_password_length(self):
      with app.app_context():
        user = users_list.create_user("Maria", "Perez","mperez", "", "admin", "Administrator") 
    
    '''def test_name_length(self):
      pass 

    def test_last_name_length(self):
      pass 

    def test_role_does_not_exist(self):
      pass

    def test_job_does_not_exist(self):
      pass'''
    
    def test_delete_user(self):
      with app.app_context():
        user = users_list.create_user("Maria", "Perez","mperez", "1234567", "admin", "Administrator")
        self.assertEqual(user[0],self.db.session.query(User).filter_by(username="mperez").first())
        user_deletion = users_list.deleting(user[0].id)
        deleted = self.db.session.query(User).filter_by(id=user_deletion[1].id).first()
        self.assertEqual(None,deleted)




if __name__ == "__main__":
  unittest.main()