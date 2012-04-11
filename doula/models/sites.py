import json
import re
import requests

from dolib.sites.site import Site
from dolib.sites.site import Node
from dolib.sites.site import Application
from dolib.sites.site import Package

class DoulaSite(Site):
    def __init__(self, name, status='unknown', nodes=[], applications=[]):
        Site.__init__(self, name, status, nodes, applications)
    
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
    
    def get_app(self, name_url):
        for app in self.applications:
            if app.name_url == name_url:
                return app
        return False
    


class DoulaNode(Node):
    def __init__(self, name, url, applications=[]):
        Node.__init__(self, name, url, applications)
    
    def get_applications(self):
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
                a.remote = app['remote']
                a.last_tag_app = app['last_tag_app']
                a.current_branch_config = app['current_branch_config']
                
                if 'packages' in app:
                    for name, version in app['packages'].iteritems():
                        a.packages.append(Package(name, version))
                
                self.applications.append(a)
            
            return self.applications
        except requests.exceptions.ConnectionError as e:
            print 'Unable to load applications: ', e.message
    

