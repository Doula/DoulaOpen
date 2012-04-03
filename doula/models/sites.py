# Handles node registration
import json
import re
import requests

def register_node(node, settings):
    sites = get_sites(settings)
    add_node_to_site(node, sites)


def get_sites(settings):
    """
    Get the sites list from settings. If it doesn't exist
    make one
    """
    if 'sites' in settings:
        return settings['sites']
    else:
        settings['sites'] = [ ]
        return settings['sites']


def add_node_to_site(node, sites):
    """
    Find the site with node information.
    If a site isn't found create a site with the node info
    and return that.
    """
    found_site = False
    
    for site in sites:
        if site.has_node(node['name']):
            return found_site
    
    # Since no site exist for this node, 
    # Create a new site with info from the node.
    # Add it to the sites list
    site = Site(node['site'])
    node = Node(node['name'], node['url'])
    site.nodes.append(node)
    sites.append(site)
    
    return site


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
            return s
    
    return False


def dirify(url):
    url = url.lower()
    url = url.replace('<', '')
    url = url.replace('>', '')
    url = url.replace('&', '')
    url = url.replace('"', '')
    url = re.sub(r'\s+', '_', url)
    url = re.sub(r'[^\d\w\s]!', '', url)
    
    return url

class Site(object):
    def __init__(self, name):
        self.name = name
        self.name_url = dirify(name)
        self.status = 'unknown'
        self.nodes = [ ]
        self.applications = [ ]
    def get_status(self):
        """
        The status of the site is the most serious status of all it's applications.
        Status from least serious to most are:
            unchanged (1), change_to_config (2), change_to_app (3), 
            change_to_app_and_config (4), uncommitted_changes (5)
        """
        if self.status != 'unknown':
            return self.status
        
        status_value = 0
        status_values = {
            'unchanged'               : 1,
            'change_to_config'        : 2, 
            'change_to_app'           : 3,
            'change_to_app_and_config': 4,
            'uncommitted_changes'     : 5
        }
        
        for app in self.applications:
            app_status_value = status_values[app.status]
            
            if app_status_value > status_value:
                status_value = app_status_value
                self.status = app.status
        
        return self.status
    
    def has_node(self, node_name):
        for node in self.nodes:
            if node.name == node_name:
                return True
        return False
    
    def has_application(self, app_name):
        for app in self.applications:
            if app.name == app_name:
                return True
        return False
    
    def update_applications(self):
        """
        Runs through the nodes and has each one return details
        about it's applications.
        """
        for node in self.nodes:
            applications = node.get_applications()
            
            for app in applications:
                if not self.has_application(app.name):
                    self.applications.append(app)
    
    def find_app_by_name_url(self, name_url):
        for app in self.applications:
            if app.name_url == name_url:
                return app
        return False

class Node:
    def __init__(self, name, url):
        self.name = name
        self.name_url = dirify(name)
        self.url = url
        self.applications = [ ]
    
    def get_applications(self):
        if len(self.applications) == 0:
            self._update_applications()
        
        return self.applications
    
    def _update_applications(self):
        """
        Update the applications
        """
        try:
            self.applications = [ ]
            
            r = requests.get(self.url + '/applications')
            rslt = json.loads(r.text)
            
            for app in rslt['applications']:
                a = Application(app['name'], self.name, self.url)
                a.current_branch_app = app['current_branch_app']
                a.change_count_app = app['change_count_app']
                a.change_count_config = app['change_count_config']
                a.is_dirty_config = app['is_dirty_config']
                a.last_tag_config = app['last_tag_config']
                a.status = app['status']
                a.last_tag_app = app['last_tag_app']
                a.current_branch_config = app['current_branch_config']
                
                self.applications.append(a)
        except requests.exceptions.ConnectionError as e:
            print 'Unable to load applications: ', e.message
    


class Application:
    def __init__(self, name, node_name, url):
        self.name = name
        self.node_name = node_name
        self.name_url = dirify(name)
        self.url = url
        
        self.current_branch_app = ''
        self.change_count_app = ''
        self.change_count_config = ''
        self.is_dirty_config = False
        self.is_dirty_app = False
        self.last_tag_config = ''
        self.status = ''
        self.last_tag_app = ''
        self.current_branch_config = ''
    def get_pretty_status(self):
        """
        Return a print friendly status
        """
        if self.status == 'unchanged':
            return 'Unchanged'
        elif self.status == 'change_to_config':
            return 'Changes to Configuration'
        elif self.status == 'change_to_app':
            return 'Changes to Application Environment'
        elif self.status == 'change_to_app_and_config':
            return 'Changes to Configuration and Application Environment'
        elif self.status == 'uncommitted_changes':
            return 'Uncommitted Changes'
        else:
            return 'Unknown'
    
