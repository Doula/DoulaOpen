import json
import unittest
from doula.models.sites import Application

class ApplicationTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_compare_url(self):
        app = Application('test_app', 'test_node', 'http://test.com')
        app.origin = 'git@code.corp.surveymonkey.com:DevOps/WebApp1.git'
        app.last_tag_app = '1.0.3'
        app.current_branch_app = 'master'
        
        compare_url = 'http://code.corp.surveymonkey.com'
        compare_url+= '/DevOps/test_app/compare/1.0.3...master'
        
        self.assertEqual(app.get_compare_url(), compare_url)
    

if __name__ == '__main__':
    unittest.main()