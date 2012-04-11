import json
import re
import requests
import logging

from dolib.sites.site import Site
from dolib.sites.site import Node
from dolib.sites.site import Application
from dolib.sites.site import Package

log = logging.getLogger('doula')

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
            for app in node.get_applications():
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
                a = DoulaApplication(app['name'], self.name, self.url)
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
        except requests.exceptions.ConnectionError as e:
            log.error('Unable to contact node "' + self.name + '" at URL ' + self.url)
        
        return self.applications
    

class DoulaApplication(Application):
    def __init__(self, name, node_name, url, 
        current_branch_app='', current_branch_config='', 
        change_count_app='', change_count_config='',
        is_dirty_app=False, is_dirty_config=False, 
        last_tag_app='', last_tag_config='', 
        status='', remote='', repo='', packages=[]):
        Application.__init__(self, name, node_name, url, 
            current_branch_app, current_branch_config, 
            change_count_app, change_count_config,
            is_dirty_app, is_dirty_config, 
            last_tag_app, last_tag_config, 
            status, remote, repo, packages)
    def tag(self, tag, msg):
        """
        Tag the current application
        """
        payload = {'tag': tag, 'description': msg, 'apps': self.name}
        r = requests.post(self.url + '/tag', data=payload)
        
        self.tag = tag
        self.msg = msg
        # figure out how we will update doula
        # we should get the app details back from bambino
        # save that to in memory storage
        self.status = 'tagged'
        

