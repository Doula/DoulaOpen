# Handles node registration
import json
import requests

def register_node(node, settings):
    add_sites(settings)
    site = add_site_to_sites(node, settings['sites'])
    
    add_apps_to_site(site, node)


def add_sites(settings):
    """
    Add the top level sites dict.
    """
    if 'sites' not in settings:
        settings['sites'] = [ ]


def add_site_to_sites(node, sites):
    # check that the site exists within the sites list
    site = get_site(node['site'], sites)
    
    if not site:
        site = {
            'name'         : node['site'], 
            'status'       :'',
            'applications' : [ ]
        }
        sites.append(site)
    
    return site


def get_site(name, sites):
    site = False
    
    for s in sites:
        print s
        
        if s['name'] == name:
            site = s
            break
    
    return site


def add_apps_to_site(site, node):
    """
    Add applications to site
    """
    pass


def get_sites(settings):
    sites = { }
    
    for site, site in settings['sites'].iteritems():
        sites['site'] = node['site']
        sites['url'] = node['url']
        
        # alextodo, update the sites
        # overall status here
        if not node['updated']:
            update_node_details(node)
        
        sites
    
    return sites


def update_node_details(node):
    r = requests.get(node['url'] + '/applications')
    details = json.loads(r.text)
    node['applications'] = details['applications']
    node['updated'] = True