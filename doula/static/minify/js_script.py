from jinja2 import environmentfilter
from jinja2 import contextfilter
from jsmin import jsmin
from pyramid import threadlocal
from time import time

import fnmatch
import shutil
import os
import pdb
import re
import sys
import time

VERSION_FILE = 'version.txt'

# Template files to search in project
TPL_FILE_TYPES = ['.htm', '.html', '.jinja2']

# also for optimization, if you have jquery already minified, then you don't have to 
# minify it, once this is used
# for survey monkey be able to pull from something else
# todo, take a look at putting a common file list into a special combine list
# the COM_LIB_LIST files would always go into they're own file and served as a single
# resource. That list of files would always come down as a whole. So even if you don't
# list a specific lib file, you'll still get it to ensure we don't have to recompile
COM_LIB_LIST = ['jquery.js', 'jquery.cookie.js']

# The cStringIO class used for speed and memory efficiency
# see http://www.skymind.com/~ocrow/python_string/
from cStringIO import StringIO

def js_script_dev(js_files):
    """
    Handles creating the script tags for development.
    """
    script_tags = ''
    
    for js_file in js_files:
        script_tags += '<script type="text/javascript" src="'
        script_tags += js_file + '"></script>'
        script_tags += "\n"
    
    return script_tags


@contextfilter
def js_script(ctx, js_files, js_file_name = ''):
    """
    Handles creating the script tags for production.
    If the js_file_name isn't passed in, the last js file name
    passed in the list js_file will be used to name the prod
    js file.
    
    For example the following function call:
        js_script(env, ['jquery.js', 'jquery.someplugin.js', '/subfolder/form.js'])
    
    from the template file named home.html
        /prodjs/subfolder/home.js
    """
    registry = threadlocal.get_current_registry()
    prodjs_path = registry.settings['prod_js_path']
    version = get_version_from_env(ctx.environment, prodjs_path)
    prod_filename = get_prod_filename(ctx.name, prodjs_path, version)
    
    script_tag = '<script type="text/javascript" src="'
    script_tag+= '/prodjs/' + prod_filename + '"></script>'
    
    return script_tag


def get_version_from_env(env, prodjs_path):
    if env.globals.get('js_version', 0) > 0:
        return env.globals.get('js_version')
    else:
        # get version, save to env
        version = read(clean_path(prodjs_path + '/' + VERSION_FILE))
        env.globals['js_version'] = version
        
        return version


def get_prod_filename(tpl_name, prodjs_path, version):
    name, ext = os.path.splitext(tpl_name)
    return name + '.' + version + '.js'


def read(file_path):
    if os.path.isfile(file_path):
        f = open(file_path, 'r')
        contents = f.read()
        f.close()
        
        return contents
    else:
        raise Exception(file_path + ' is not a file')


def clean_path(path):
    """
    Ensure we don't get any double forward slashes if 
    ini settings are entered incorrectly
    """
    return path.replace('//', '/')

                
# MINIFY PROJECT FILES
class MinifyProject():
    def __init__(self, tpl_path, js_path, prodjs_path):
        self.tpl_path = tpl_path
        self.js_path = js_path
        self.prodjs_path = prodjs_path
    
    
    def minify_all_js_files(self):
        """
        Find all the js_script filters embedded in template files.
        Find the scripts in the js folder and minify them into a single js file
        named after the template they were created for.
        
        For example the template home_page.html with the following filter:
            {{ ['/js/jquery.js', '/js/home.js']|js_script|safe }}
        
        Will create a production file named:
            /prodjs/home_page.[version].js
        
        The version number is stored in the /prodjs/version.txt file.
        """
        self._prep_prodjs_dir()
        
        files = self._index_project_files()
        filenames_to_scripts = self._get_filename_to_scripts(files)
        
        for filename, scripts in filenames_to_scripts.items():
            self._minify_page_scripts(filename, scripts)
    
    
    def _prep_prodjs_dir(self):
        """
        Prepare the /prodjs/ directory for minification
        """
        # Remove all the files in this directory
        shutil.rmtree(self.prodjs_path)
        
        # Make sure the prod js dir exists
        os.makedirs(self.prodjs_path)
        
        # Make the /prodjs/version.txt file and save current unix timestamp
        t = str(time.time())
        version = t.split('.')[0]
        
        version_file = open(clean_path(self.prodjs_path + '/' + VERSION_FILE), 'w')
        version_file.write(version)
        version_file.close()
    
    
    def _index_project_files(self):
        """
        Builds a list of all the template files that need to
        be searched for js_scripts
        """
        files = [ ]
        
        for root, dirnames, filenames in os.walk(self.tpl_path):
            # Ignore directories that start with a dot
            if root.find('/.') == -1:
                for file_name in filenames:
                    if self._is_approved_file_type(file_name):
                        path_to_file = root.rstrip('/') + '/' + file_name
                        files.append(path_to_file)
        
        return files
    
    
    def _is_approved_file_type(self, file_name):
        is_approved = False
        
        for ftype in TPL_FILE_TYPES:
            if file_name.endswith(ftype):
                is_approved = True
                break
        
        return is_approved
    
    
    def _get_filename_to_scripts(self, files):
        """
        Roll through the project files and find the scripts.
        Add to the dict, with format:
            { filename: [list_of_js_files] }
        """
        filenames_to_scripts = { }
        
        for f in files:
            js_scripts = self._find_js_scripts(f)
            
            if js_scripts:
                filenames_to_scripts[f] = js_scripts
        
        return filenames_to_scripts
    
    
    def _find_js_scripts(self, path_to_file):
        """
        Find the js_scripts embedded in our templates
            ex. ['/js/jquery.js', '/js/bootstrap-dropdown.js', '/js/doula.js']
        """
        regex = r'\[(.*)\]|js_script'
        contents = self._get_clean_contents(path_to_file)
        matches = re.findall(regex, contents)
        js_scripts = ''
        
        if len(matches) > 0:
            js_scripts = matches[0].strip()
        
        return js_scripts
    
    
    def _get_clean_contents(self, path_to_file):
        """
        Read the contents of the file into a single string.
        Replace all new line characters with a space so that
        we can run regex on the entire file as a single string
        """
        contents = read(path_to_file)
        return re.sub(r'\s+', ' ', contents)
    
    
    def _minify_page_scripts(self, filename, scripts):
        scripts = self._get_cleaned_scripts(scripts)
        minified_js = self._get_minified_js(scripts)
        prod_filename = self._get_prod_filename(filename)
        
        self._create_prod_file(prod_filename, minified_js)
    
    
    def _get_cleaned_scripts(self, scripts):
        """
        Return string '/js/jquery.js', '/js/home.js'
        as list of individual strings split by commas
        """
        scripts_list = scripts.split(',')
        scripts = [script.replace('"', '').replace("'", "").strip() 
                    for script in scripts_list ]
        
        return scripts
    
    
    def _get_minified_js(self, js_files):
        """
        Minify js files in the list as a single file.
        Roll through the js_files, read their contents,
        put them into a single string for writing
        """
        minified_js = StringIO()
        
        for js_file in js_files:
            js_file_path = clean_path(self.js_path + js_file.replace('/js', ''))
            js_contents = read(js_file_path)
            
            minified_js.write(jsmin(js_contents))
            minified_js.write(';')
        
        return minified_js.getvalue()
    
    
    def _get_prod_filename(self, filename, version=0):
        """
        Return the production file name:
            Format template_name.version.js
        """
        rel = filename.replace(self.tpl_path, '')
        prod_file, ext = os.path.splitext(rel)
        
        return prod_file + '.' + self._get_version(version) + '.js'
    
    
    def _get_version(self, version):
        if version > 0:
            return str(version)
        else:
            return read(clean_path(prodjs_path + '/' + VERSION_FILE))
    
    
    def _create_prod_file(self, prod_filename, minified_js):
        # Actually write the minified files
        prod_file = clean_path(self.prodjs_path + '/' + prod_filename)
        # Make sure the prod js dir exists
        prod_dir = os.path.dirname(prod_file)
        
        if not os.path.isdir(prod_dir):
            os.makedirs(prod_dir)
        
        prod_file = open(prod_file, 'w')
        prod_file.write(minified_js)
        prod_file.close()
    


if __name__ == '__main__':
    path = '/Users/alexvazquezOLD/boxes/doula'
    tpl_path = path + '/doula/templates/'
    js_path = path + '/doula/static/js/'
    prodjs_path = path + '/doula/static/prodjs/'
    
    print 'Minifying ...'
    mp = MinifyProject(tpl_path, js_path, prodjs_path)
    mp.minify_all_js_files()
    
    print 'Done minifying'
    
