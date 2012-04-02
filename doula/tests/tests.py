import json
import unittest

from pyramid import testing
from doula.views import register
from doula.views import sites

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_register(self):
        request = testing.DummyRequest()
        
        node = {
            'site': 'Monkey Test One',
            'url' : 'http://127.0.0.1:6542'
        }
        
        request.POST['node'] = json.dumps(node)
        result = register(request)
        self.assertEqual(result['success'], 'true')
    
    def test_sites(self):
        request = testing.DummyRequest()
        
        all_sites = sites(request)
        self.assertTrue(all_sites)

if __name__ == '__main__':
    unittest.main()
