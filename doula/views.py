from pyramid.view import view_config
from pyramid.events import ApplicationCreated
from pyramid.events import subscriber

from models.sites import register_node
from models.sites import get_sites
from models.sites import get_updated_sites

import json

@view_config(route_name='home', renderer='index.html')
def show_home(request):
    return show_sites(request)

@view_config(route_name='sites', renderer='index.html')
def show_sites(request):
    sites = get_updated_sites(request.registry.settings)
    
    return {'sites': sites}

@view_config(route_name='site', renderer="site.html")
def show_site(request):
    sites = get_updated_sites(request.registry.settings)
    site = ''
    
    for s in sites:
        if s.name == request.matchdict['site']:
            site = s
            break
    
    # alextodo, need to throw 404 execpetion if not found
    return { 'site': site }


@view_config(route_name='application', renderer="application.html")
def show_application(request):
    sites = get_updated_sites(request.registry.settings)
    
    return {  }
        
@view_config(route_name='register', renderer='json')
def register(request):
    # use validcitory to validate post
    node = json.loads(request.POST['node'])
    register_node(node, request.registry.settings)
    
    return {'success': 'true'}

# Used only for testing during development
@subscriber(ApplicationCreated)
def register_node_on_start(event):
    """
    Register this Bambino node with Doula.
    """
    node = {
        'name': 'Machine Numero Uno',
        'site': 'Monkey Test One',
        'url' : 'http://127.0.0.1:6542'
    }
    
    register_node(node, event.app.registry.settings)
