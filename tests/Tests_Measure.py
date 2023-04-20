import unittest
from Tests_Base import Tests_Base, driver, session

from src.models.User import User
from main import measures,  app


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

if __name__ == "__main__":
  unittest.main()