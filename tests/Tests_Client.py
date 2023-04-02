import unittest
from Tests_Base import Tests_Base, driver, session
from flask import session as flask_session
from datetime import datetime
from main import clients, client_details
from src.models.Client import Client
from src.models.Car import Car


class Tests_Client_Unit(Tests_Base):
    def test_adding_client_admin(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,self.db.session.query(Client).filter_by(id=c.id).first())

    def test_adding_client_operation_analyst(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'opera'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,self.db.session.query(Client).filter_by(id=c.id).first())

    def test_adding_client_user(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,False)

    def test_adding_client_admin_and_editing(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,"25145785","Carlos","Perez",birth_date,"4161234567","carlos@mail.com","Caracas")
        edited_client = clients.adding_client(c.id,"25145785","Carlos","Perez",birth_date,"4142457896","carlosp@mail.com","Municipio Sucre")
        self.assertEqual(c.id,edited_client.id)
        edition = self.db.session.query(Client).filter_by(id=c.id).first()
        self.assertEqual(edition.phone,"4142457896")
        self.assertEqual(edition.mail,"carlosp@mail.com")
        self.assertEqual(edition.address,"Municipio Sucre")

    def test_adding_client_modifying_repeated_ci(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c1 = clients.adding_client(0,"25145785","Carlos","Perez",birth_date,"4161234567","carlos@mail.com","Caracas")
        c2 = clients.adding_client(0,"21817123","Jose","Perez",birth_date,"4142365871","jose@mail.com","Caracas")
        editing_c2 = clients.editing_client("25145785",c2.id,"Jose","Perez",birth_date,"4142365871","jose@mail.com","Caracas")
        self.assertEqual(editing_c2[0],False)

    def test_removing_client_admin(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,self.db.session.query(Client).filter_by(id=c.id).first())
        d = clients.removing_client(c.id)
        query = self.db.session.query(Client).filter_by(id=d.id).first()
        self.assertEqual(query,None)

    def test_removing_client_operator_analyst(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'opera'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        self.assertEqual(c,self.db.session.query(Client).filter_by(id=c.id).first())
        d = clients.removing_client(c.id)
        query = self.db.session.query(Client).filter_by(id=d.id).first()
        self.assertEqual(query,None)

    def test_removing_client_user(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'opera'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        d = clients.removing_client(c.id)
        self.assertEqual(d,False)

    def test_adding_car(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        client_details.adding_new_car(0,c.id,c,"AZC78E","toyota","corolla",2004,
          16168161616,68848616,"negro","no enciende")
        query = self.db.session.query(Car).filter_by(serial_car=68848616,serial_engine=16168161616).first()
        self.assertEqual(query.serial_engine,str(16168161616))
        self.assertEqual(query.serial_car,str(68848616))


    def test_removing_car_user(self):
      with self.app.test_request_context(), self.app.test_client() as c:
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'admin'
            }
        birth_date = datetime.strptime('1996-10-10', r'%Y-%m-%d') 
        c = clients.adding_client(0,25145785,"Carlos","Perez",birth_date,4161234567,"carlos@mail.com","Caracas")
        car = client_details.adding_new_car(0,c.id,c,"AZC78E","toyota","corolla",2004,
          16168161616,68848616,"negro","no enciende")
        flask_session['user'] = {
                'id' : '1',
                'username' : '1',
                'role' : 'user'
            }
        removed_car = client_details.removing_car(car.license_plate,c.id)
        self.assertEqual(removed_car,False)




if __name__ == "__main__":
  unittest.main()