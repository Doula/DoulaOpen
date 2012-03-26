from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    
    # Jinja2 config
    config.add_renderer('.html', renderer_factory)
    config.include('pyramid_jinja2')
    
    # Scan this module
    config.scan('doula_wires.views')
    
    config.add_static_view(name='js', path='static/js')
    config.add_static_view(name='prodjs', path='static/prodjs')
    config.add_static_view(name='css', path='static/css')
    config.add_static_view(name='images', path='static/images')
    
    # routes for application
    config.add_route('home', '/')
    config.add_route('site', '/{site}/')
    config.add_route('application', '/{site}/{application}/')
    
    return config.make_wsgi_app()
