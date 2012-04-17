import json
from doula.util import pprint
from doula.util import dumps
from doula.models.sites_dao import SiteDAO
from doula.models.util import encode
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound


@view_config(route_name='home', renderer='home.html')
def show_home(request):
    return show_sites(request)

@view_config(route_name='sites', renderer='home.html')
def show_sites(request):
    dao = SiteDAO()
    
    return { 'sites': dao.get_sites() }

@view_config(route_name='site', renderer="site.html")
def show_site(request):
    dao = SiteDAO()
    site = dao.get_site(request.matchdict['site'])

    if not site:
        raise HTTPNotFound('Unable to find site "' + request.matchdict['site'] + '"')

    return { 'site': site, 'site_json': dumps(site) }


@view_config(route_name='application', renderer="application.html")
def show_application(request):
    dao = SiteDAO()
    site = dao.get_site(request.matchdict['site'])
    app = site.applications[request.matchdict['application']]

    return { 'site': site, 'app': app }

@view_config(route_name='tag', renderer="string")
def tag_application(request):
    dao = SiteDAO()
    site = dao.get_site(request.matchdict['site'])
    app = site.applications[request.matchdict['application']]
    app.tag(request.POST['tag'], request.POST['msg'])

    return dumps({ 'success': True, 'app': app })

@view_config(context=HTTPNotFound, renderer='404.html')
def not_found(self, request):
    request.response.status = 404
    
    return { 'msg': request.exception.message }


@view_config(route_name='register', renderer='json')
def register(request):
    """
    Register a Bambino node with Doula.
    """
    node = json.loads(request.POST['node'])
    pprint(node)
    dao = SiteDAO()
    dao.register_node(node)
    
    return {'success': 'true'}

