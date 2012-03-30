import json
import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_register(self):
        from doula.views import register
        request = testing.DummyRequest()
        
        node = {
            'site': 'Monkey Test One',
            'url' : 'http://127.0.0.1:6542'
        }
        
        request.POST['node'] = json.dumps(node)
        result = register(request)
        
        self.assertEqual(result['pass'], 'true')
    

if __name__ == '__main__':
    unittest.main()
