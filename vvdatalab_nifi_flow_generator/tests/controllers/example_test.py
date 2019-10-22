from vvdatalab_nifi_flow_generator import app, static
from nipyapi import security
import json
import os.path
import unittest

class ExampleTest(unittest.TestCase):

    def setup(self):
        app.config['TESTING'] = True

        self.app = app.test_client()
        self.assertEqual(app.testing, True)

        key = None
        file = os.path.split(os.path.dirname(__file__))[0].replace('/tests', '') + '/static/key.json'
        with open(file) as json_file:
            data = json.load(json_file)
            key = data

        self.assertEqual(security.service_login('nifi',key['user'],key['password'],True), True)

    def tearDown(self):
        pass

    def test_example2(self):

        self.setup()

        parameter = ''
        file = os.path.split(os.path.dirname(__file__))[0].replace('/tests', '') + '/static/data/example.json'
        with open(file) as json_file:
            data = json.load(json_file)
            parameter = json.dumps(data)

        response = self.app.post('/example2', data=dict(process_group=parameter))

        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
  unittest.main()