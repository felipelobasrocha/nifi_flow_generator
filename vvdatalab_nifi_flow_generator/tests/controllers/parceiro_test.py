from vvdatalab_nifi_flow_generator import app, static
from nipyapi import security
import json
import os.path
import unittest

class ParceiroTest(unittest.TestCase):

    def setup(self):
        app.config['TESTING'] = True

        self.app = app.test_client()
        self.assertEqual(app.testing, True)

    def tearDown(self):
        pass

    def test_mroi(self):

        self.setup()

        parameter = ''
        file = os.path.split(os.path.dirname(__file__))[0].replace('/tests', '') + '/static/data/data_flow.json'
        with open(file) as json_file:
            data = json.load(json_file)
            parameter = json.dumps(data)

        response = self.app.post('/mroi', data=dict(process_group=parameter))

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
  unittest.main()