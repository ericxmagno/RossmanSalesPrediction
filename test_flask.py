import unittest
import json

from joblib import load 
import os
os.environ['TEST_RUNNING'] = 'True'

from app import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    # Check for response 200
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # Check predict endpoint
    def test_predict(self):
        payload = {
            "Store":1111,
            "DayOfWeek":4,
            "Date":"2014-07-10",
            "Customers":410,
            "Open":1,
            "Promo":0,
            "StateHoliday":"0",
            "SchoolHoliday":1
        }
        response = self.app.post('/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
   