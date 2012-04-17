import unittest
from doula.cache import Cache
from doula.models.sites_dao import SiteDAO

class TestSitesDAO(unittest.TestCase):
    
    def setUp(self):
        Cache.env = 'dev'
        Cache.clear_cache()
        self.cache = Cache.cache()
    
    def test_cache_store(self):
        # Just make sure we get a valid cache store from cache
        self.cache.set('key', 'value')
        self.assertEqual(self.cache.get('key'), 'value')
    
    def test_register_node(self):
        site = 'site1'
        
        node1 = {
            'name': 'node1',
            'site': site,
            'url' : 'http://node1'
        }
        
        node2 = {
            'name': 'node2',
            'site': site,
            'url' : 'http://node2'
        }
        
        dao = SiteDAO()
        dao.register_node(node1)
        dao.register_node(node2)
        
        self.assertEqual(len(dao.nodes(site).keys()), 2)
        
        node3 = {
            'name': 'node3',
            'site': site,
            'url' : 'http://node3'
        }
        
        dao.register_node(node3)
        
        self.assertEqual(len(dao.nodes(site).keys()), 3)
    
    def test_register_node_two(self):
        dao = SiteDAO()
        nodes = dao.nodes('unknown site')
        self.assertEqual(len(nodes), 0)


if __name__ == '__main__':
    unittest.main()