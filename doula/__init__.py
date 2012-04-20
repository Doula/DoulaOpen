from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory

def main(global_config, **settings):
    """
    Serve Doula.
    """
    config = Configurator(settings=settings)
    
    # Jinja2 config
    config.add_renderer('.html', renderer_factory)
    config.include('pyramid_jinja2')
    
    # Scan this module
    config.scan('doula.views')
    
    config.add_static_view(name='js', path='static/js')
    config.add_static_view(name='prodjs', path='static/prodjs')
    config.add_static_view(name='css', path='static/css')
    config.add_static_view(name='images', path='static/images')
    
    # routes for application
    config.add_route('home', '/')
    config.add_route('sites', '/sites')
    config.add_route('site', '/sites/{site}')
    config.add_route('application', '/sites/{site}/{application}')
    config.add_route('register', '/register')
    config.add_route('deploy', '/deploy.json')
    config.add_route('tag', '/tag')
    
    return config.make_wsgi_app()
