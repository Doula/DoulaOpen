import unittest
from doula.util import pprint
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
    
    def test_all_site_keys(self):
        dao = SiteDAO()
        
        node = {
            'name': 'node1',
            'site': 'site1',
            'url' : 'http://node1'
        }
        
        dao.register_node(node)
        keys = dao._all_site_keys()
        
        self.assertEqual(keys[0], 'site:site1')
    
    def test_get_sites(self):
        # Get Site objects array, [Site, Site, Site...]
        dao = SiteDAO()
        self._register_node(dao)
        
        sites = dao.get_sites()
        self.assertEqual(len(sites), 1)
        self.assertEqual(len(sites['site1'].nodes.keys()), 1)
        pprint(sites)
    
    def _register_node(self, dao):
        node = {
            'name': 'node1',
            'site': 'site1',
            'url' : 'http://node1'
        }
        
        dao.register_node(node)

if __name__ == '__main__':
    unittest.main()