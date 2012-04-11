from sites import DoulaSite
from sites import DoulaNode

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
    site = DoulaSite(node['site'])
    node = DoulaNode(node['name'], node['url'])
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
            s.update_applications()
            return s
    
    return False

