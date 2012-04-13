from pyramid.view import view_config

from models.sites_dao import register_node
from models.sites_dao import get_sites
from models.sites_dao import find_site_by_name_url
from models.sites_dao import get_updated_sites
from models.util import encode

from pyramid.httpexceptions import HTTPNotFound

import json

@view_config(route_name='home', renderer='home.html')
def show_home(request):
    return show_sites(request)

@view_config(route_name='sites', renderer='home.html')
def show_sites(request):
    sites = get_updated_sites(request.registry.settings)

    return {'sites': sites}

@view_config(route_name='site', renderer="site.html")
def show_site(request):
    sites = get_updated_sites(request.registry.settings)
    site = find_site_by_name_url(sites, request.matchdict['site'])

    if not site:
        raise HTTPNotFound('Unable to find site "' + request.matchdict['site'] + '"')

    return { 'site': site, 'site_json': dumps(site) }


@view_config(route_name='application', renderer="application.html")
def show_application(request):
    sites = get_updated_sites(request.registry.settings)
    site = find_site_by_name_url(sites, request.matchdict['site'])
    app = site.get_app(request.matchdict['application'])

    return { 'site': site, 'app': app }

@view_config(route_name='tag', renderer="string")
def tag_application(request):
    # alextodo, need to fold these into a single call
    sites = get_updated_sites(request.registry.settings)
    site = find_site_by_name_url(sites, request.POST['site'])
    app = site.get_app(request.POST['name_url'])
    app.tag(request.POST['tag'], request.POST['msg'])

    return dumps({ 'success': True, 'app': app })

@view_config(route_name='register', renderer='json')
def register(request):
    # use validcitory to validate post
    node = json.loads(request.POST['node'])
    register_node(node, request.registry.settings)

    return {'success': 'true'}

@view_config(context=HTTPNotFound, renderer='404.html')
def not_found(self, request):
    request.response.status = 404

    return { 'msg': request.exception.message }

