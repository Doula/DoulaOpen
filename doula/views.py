import json
import time

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
        msg = 'Unable to find site "{0}"'.format(request.matchdict['site'])
        raise HTTPNotFound(msg)

    return { 'site': site, 'site_json': dumps(site) }


@view_config(route_name='application', renderer="application.html")
def show_application(request):
    try:
        dao = SiteDAO()
        site = dao.get_site(request.matchdict['site'])
        app = site.applications[request.matchdict['application']]

        if take_note(request, app):
            app.add_note(request.POST['note'])

    except:
        if 'note' in request.POST:
            msg = 'Unable to add note to "{0}"'
            msg = msg.format(request.matchdict['application'])
        else:
            msg = 'Unable to find site and application under "{0}" and "{1}"'
            msg = msg.format(request.matchdict['site'], request.matchdict['application'])

        raise HTTPNotFound(msg)
    

    return { 'site': site, 'app': app }

def take_note(request, app):
    if 'note' in request.POST:
        # ensure the user isn't reposting same last comment by accident
        keys = sorted(app.notes.keys())
        
        if len(keys) > 0:
            last_note = app.notes[keys.pop()]
            
            if request.POST['note'] == last_note:
                # Stop users from resubmitting the last note twice
                return False
        
        return True
    else:
        return False


@view_config(route_name='tag', renderer="string")
def tag_application(request):
    try:
        dao = SiteDAO()
        site = dao.get_site(request.POST['site'])
        app = site.applications[request.POST['application']]
        app.tag(request.POST['tag'], request.POST['msg'])
        
        return dumps({ 'success': True, 'app': app })
    except KeyError as e:
        msg = 'Unable to tag site and application under "{0}" and "{1}"'
        msg = msg.format(request.POST['site'], request.POST['application'])
        
        return dumps({ 'success': False, 'msg': msg })
    

@view_config(route_name='deploy', renderer="string")
def deploy_application(request):
    try:
        dao = SiteDAO()
        site = dao.get_site(request.POST['site'])
        app = site.applications[request.POST['application']]
        app.deploy_application(site)

        return dumps({ 'success': True, 'app': app })
    except KeyError as e:
        msg = 'Unable to deploy application under "{0}"'
        msg = msg.format(request.POST['site'], request.POST['application'])
        
        return dumps({ 'success': False, 'msg': msg })
    
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
    node['time'] = time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())
    pprint(node)

    if(request.POST['action'] == 'register'):
        SiteDAO().register_node(node)
    else:
        SiteDAO().unregister_node(node)
    
    return {'success': 'true'}

