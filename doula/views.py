from pyramid.view import view_config
from pyramid.events import ApplicationCreated
from pyramid.events import subscriber

from models.sites import register_node
from models.sites import get_sites
from models.sites import find_site_by_name_url
from models.sites import get_updated_sites
from view_helpers import encode

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
    site = find_site_by_name_url(sites, request.matchdict['site'])
    
    # alextodo, need to throw 404 execpetion if not found
    return { 'site': site, 'site_json': encode(site) }


@view_config(route_name='application', renderer="application.html")
def show_application(request):
    sites = get_updated_sites(request.registry.settings)
    site = find_site_by_name_url(sites, request.matchdict['site'])
    app = site.find_app_by_name_url(request.matchdict['application'])
    
    return { 'site': site, 'app': app }
        
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
