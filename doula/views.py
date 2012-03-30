from pyramid.view import view_config
from pyramid.events import ApplicationCreated
from pyramid.events import subscriber

from models.sites import register_node
from models.sites import get_sites

import json

@view_config(route_name='sites', renderer='index.html')
def sites(request):
    sites = get_sites(request.registry.settings)
    
    return {'sites': sites}

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
        'site': 'Monkey Test One',
        'url' : 'http://127.0.0.1:6542'
    }
    
    register_node(node, event.app.registry.settings)
