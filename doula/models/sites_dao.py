import json

from pprint import pprint
from doula.cache import Cache

class SiteDAO(object):
    def __init__(self):
        self.cache = Cache.cache()
    
    def register_node(self, node):
        site = self._get_site(node['site'])
        site['nodes'][node['name']] = node
        
        key = self._get_site_cache_key(node['site'])
        self.cache.set(key, json.dumps(site))
    
    def _get_site_cache_key(self, name):
        return 'site:' + name
    
    def _get_site(self, name):
        """
        Get the site jsonified object from cache. If the site
        doesn't exist create one.
        Site is a dict:
            {'name':'value', 
            nodes: [{'name':{'name':value, 'site':value, 'url':value}}]}
        """
        site = self.cache.get(self._get_site_cache_key(name))
        
        if site:
            return json.loads(site)
        else:
            return { 'name' : name, 'nodes' : { } }
    
    def nodes(self, name):
        site = self._get_site(name)
        
        return site['nodes']
    
    def _all_site_keys(self):
        return '*'
    
    def get_sites(self):
        """
        Get list of registered sites. Returns actual Site object.
        """
        return [ ]


# Old functions!
def get_updated_sites(settings):
    """
    Get the sites array. Roll through the sites and update their statuses
    """
    sites = get_sites(settings)

    for site in sites:
        site.update_applications()

    return sites


def find_site_by_name_url(sites, name_url):
    for s in sites:
        if s.name_url == name_url:
            s.update_applications()
            return s

    return False

