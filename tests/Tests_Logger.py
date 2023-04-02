import unittest
from Tests_Base import Tests_Base, driver, session

from src.models.Logger import Logger
from main import  logger

class Tests_Logger_Unit(Tests_Base):

    def test_removing_event(self):
      with self.app.test_request_context():
        log = Logger('Login')
        self.db.session.add(log)
        self.db.session.commit()
        a = logger.removing_event(log.id)
        event = self.db.session.query(Logger).filter_by(id=a.id)
        self.assertEqual(event.count(),0)
   

if __name__ == "__main__":
  unittest.main()