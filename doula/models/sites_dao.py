import json
from doula.util import pprint
from doula.cache import Cache
from doula.models.sites import Site
from doula.models.sites import Node
from doula.models.sites import Application
from doula.models.sites import Package

class SiteDAO(object):
    def __init__(self):
        self.cache = Cache.cache()
        self.site_prefix = 'site:'
    
    def register_node(self, node):
        site = self._get_site(node['site'])
        site['nodes'][node['name']] = node
        
        key = self._get_site_cache_key(node['site'])
        self.cache.set(key, json.dumps(site))
    
    def _get_site_cache_key(self, name):
        return self.site_prefix + name
    
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
        return self.cache.keys('site:*')
    
    def get_sites(self):
        """
        Get list of registered sites. Returns actual Site object.
        """
        all_sites = { }
        
        for site_key in self._all_site_keys():
            site_name = site_key.replace(self.site_prefix, '')
            all_sites[site_name] = self.get_site(site_name)
        
        return all_sites
    
    def get_site(self, site_name):
        simple_site = self._get_site(site_name)
        return SiteFactory.build_site(simple_site)
    

class SiteFactory(object):
    """
    Builds Site objects, with Node and Applications as well
    """
    @staticmethod
    def build_site(simple_site):
        """
        Take the simple dictionary version of a site object, i.e.
            {name:value, nodes[{'name':value, 'site':value, 'url':value}]}
        and return an actual Site object with all the nodes and applications
        built as well.
        """
        site = Site(simple_site['name'])
        site.nodes = SiteFactory._build_nodes(simple_site['nodes'])
        site.applications = SiteFactory._get_combined_applications(site.nodes)
        
        return site
    
    @staticmethod
    def _build_nodes(simple_nodes):
        """
        Takes the nodes with format:
            nodes[{'name':value, 'site':value, 'url':value}]
        And builds Node objects
        """
        nodes = { }
        
        for name,n in simple_nodes.iteritems():
            node = Node(name, n['url'])
            node.load_applications()
            nodes[name] = node
        
        return nodes
    
    @staticmethod
    def _get_combined_applications(nodes):
        """
        Takes the nodes (contains actual Node objects) and 
        builds the applications as a combined list of their 
        applications for the entire site.
        """
        combined_applications = { }
        
        for k, node in nodes.iteritems():
            for app_name, app in node.applications.iteritems():
                combined_applications[app_name] = app
        
        return combined_applications
