import json
import re
import requests
import logging

log = logging.getLogger('doula')

# Defines the Data Models for Doula and Bambino.
#
# sites
#   Site
#     nodes
#       applications
#         Application
#           packages
#             Package
#     applications
#       Application
#         packages
#           Package
import re
from doula.util import dirify
from doula.util import dumps

class Site(object):
    def __init__(self, name, status='unknown', nodes={}, applications={}):
        self.name = name
        self.name_url = dirify(name)
        self.status = status
        self.nodes = nodes
        self.applications = applications
    def get_status(self):
        """
        The status of the site is the most serious status of all it's applications.
        The more serious the status, the higher the status value number.
        """
        status_value = 0
        status_values = {
            'unknown'                 : 0,
            'deployed'                : 1,
            'tagged'                  : 2,
            'change_to_config'        : 3,
            'change_to_app'           : 3,
            'change_to_app_and_config': 3,
            'uncommitted_changes'     : 4
        }
        
        for app_name, app in self.applications.iteritems():
            app_status_value = status_values[app.status]
            
            if app_status_value > status_value:
                status_value = app_status_value
                self.status = app.status
        
        return self.status
    

class Node(object):
    def __init__(self, name, site_name, url, applications={}):
        self.name = name
        self.name_url = dirify(name)
        self.site_name = site_name
        self.url = url
        self.applications = applications
        self.errors = [ ]
    
    def load_applications(self):
        """
        Update the applications
        """
        try:
            self.errors = [ ]
            self.applications = { }
            
            r = requests.get(self.url + '/applications')
            # If the response is non 200, we raise an error
            r.raise_for_status()
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
                a.last_tag_message = app['last_tag_message']
                a.current_branch_config = app['current_branch_config']
                a.changed_files = app['changed_files']
                a.notes = app['notes']
                a.packages = [ ]
                
                for name, version in app['packages'].iteritems():
                    a.packages.append(Package(name, version))
                
                self.applications[a.name_url] = a
        except requests.exceptions.ConnectionError as e:
            msg = 'Unable to contact node {0} at URL {1}'.format(self.name, self.url)
            log.error(msg)
            self.errors.append(msg)
        except Exception as e:
            msg = 'Unable to load applications. Error: {0}'.format(e)
            log.error(msg)
            self.error.append(msg)
        
        return self.applications
    

class Application(object):
    def __init__(self, name, site_name, node_name, url,
        current_branch_app='', current_branch_config='',
        change_count_app='', change_count_config='',
        is_dirty_app=False, is_dirty_config=False,
        last_tag_app='', last_tag_config='', last_tag_message='',
        status='', remote='', repo='', packages=[], changed_files=[], notes={}):
        self.name = name
        self.site_name = site_name
        self.node_name = node_name
        self.name_url = dirify(name)
        self.url = url
        
        self.current_branch_app = current_branch_app
        self.current_branch_config = current_branch_config
        
        self.change_count_app = change_count_app
        self.change_count_config = change_count_config
        
        self.is_dirty_app = is_dirty_app
        self.is_dirty_config = is_dirty_config
        
        self.last_tag_app = last_tag_app
        self.last_tag_config = last_tag_config
        self.last_tag_message = last_tag_message
        
        self.status = status
        self.remote = remote
        self.packages = packages
        self.changed_files = changed_files
        self.notes = notes
    
    def get_compare_url(self):
        """
        Use the remote url to return the Github Comapre view URL.
        The Github Compare URL has the format:
        http://<GITHUB_URL>/<USER>/<REPO>/compare/<START>...<END>
        For us this means
        http://code.corp.surveymonkey.com/DevOps/[name]/compare/[last_tag_app]...[current_branch_app]
        """
        if self.remote.startswith('http'):
            # parses http://code.corp.surveymonkey.com/tbone/anweb.git type remote
            m = re.search(r'http:\/\/([\w\.]+)\/([\w\d]+)\/([\w\d]+)', self.remote)
        else:
            # parses git@code.corp.surveymonkey.com:tbone/anweb-1.git type remote
            m = re.search(r'@([\w\.]+):([\w\d]+)\/([\w\d]+)', self.remote)
        
        compare_url = 'http://' + m.group(1) + '/' + m.group(2) + '/' + self.name
        compare_url+= '/compare/' + self.last_tag_app + '...' + self.current_branch_app
        
        return compare_url
    def tag(self, tag, msg):
        """
        Tag the current application
        """
        payload = {'tag': tag, 'description': msg, 'apps': self.name}
        r = requests.post(self.url + '/tag', data=payload)
        # If the response is non 200, we raise an error
        r.raise_for_status()

        self.tag = tag
        self.msg = msg
        self.status = 'tagged'
    
    def add_note(self, note):
        """
        Add a note to the Bambino
        """
        payload = { 'note': note, 'app': self.name }
        r = requests.post(self.url + '/note', data=payload)
        # If the response is non 200, we raise an error
        r.raise_for_status()

        rslt = json.loads(r.text)
        self.notes = rslt['notes']
    
    @property
    def status(self):
        # alextodo, implement the 
        pass
    
    def deploy_application(self, site):
        """
        Mark an application as deployed
        """
        self.status = 'deployed'
        
        cache = Cache.cache()
        key = self.get_cache_app_status_key(site)
        cache.set(key, self.status)
    
    def get_cache_app_status_key(self, site):
        return site.name_url + self.name_url + '_status'

class Package(object):
    """
    Represents a python package
    """
    def __init__(self, name, version):
        self.name = name
        self.version = version
    
