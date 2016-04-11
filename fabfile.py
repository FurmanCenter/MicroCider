'''
This fabfile defines methods for automated tasks, allowing
for easier building, publishing, etc. of the pelican site.

To specify the location of the site content, set the PATH option when invoking
``fabric``, which will be passed on to Pelican, overriding the :py:data:`pelicanconf.PATH`
attribute in the config file.

For example::

    fab build --set=PATH="path/to/content\ escaping\ spaces/"

'''
from fabric.api import *
import fabric.contrib.project as project
import os
import sys
import SimpleHTTPServer
import SocketServer


#: Remote server configuration
try:
    from secretconf import production, dest_path
except:
    from secretconf_SAMPLE import production, dest_path

#: Local path configuration (can be absolute or relative to fabfile)
#: This is where the output from Pelican is saved
if 'deploy_path' not in env:
     env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path




def clean():
    '''Deletes the output directory and makes a new, empty one'''
    if os.path.isdir(DEPLOY_PATH):
        try:
            res = local('del /s /q {deploy_path}\\*'.format(**env), capture=True)
        except:
            local('rm -R {deploy_path}'.format(**env), capture=True)
            local('mkdir {deploy_path}'.format(**env), capture=True)
    else:
        local('mkdir {deploy_path}'.format(**env))

def build():
    '''Builds the site (locally) using the default local config file'''
    local('pelican -s pelicanconf.py {PATH}'.format(PATH=getattr(env, "PATH", "")))

def debug():
    '''Cleans and then builds locally with the debug flag on, to show
    all debug messages'''
    clean()
    local('pelican -D -s pelicanconf.py {PATH}'.format(PATH=getattr(env, "PATH", "")))

def rebuild():
    '''Clear output directory, then build locally'''
    clean()
    build()

def regenerate():
    '''Re-build whenever a file is saved; useful for local testing'''
    local('pelican -r -s pelicanconf.py {PATH}'.format(PATH=getattr(env, "PATH", "")))

def serve():
    '''Serve the output directory at ``localhost:8000``. Use for local testing'''
    os.chdir(env.deploy_path)

    PORT = 8000
    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    '''Build then serve'''
    build()
    serve()

def preview():
    '''Build the site locally as if publishing to the server.
    Use this to see what the files would look like on the remote server,
    without actually changing the contents of the server. Note that, since
    resources are referred to by their URL on the server, rather than their
    file location, some things won't load locally, or will load possibly
    unchanged versions from the live server.'''
    local('pelican -s publishconf.py {PATH}'.format(PATH=getattr(env, "PATH", "")))

# The @hosts decorator says that the publish command should always
# use the production host (which is defined in the secretconf.py file)
@hosts(production)
def publish():
    '''Publish to website
    To call this, you either need to have SSH set up, or use the following
    options when invoking ``fabric``:

    -I  switch to have password entered initially, or
    -p  switch with the password.

    For example:

        ``fab publish -I``

            Prompt for password first, though the password won't actually be
            checked that it's correct

        ``fab publish -p mypassword``

            Pass ``mypassword`` through to publish site without prompting
            (where actual password replaces ``mypassword``)

    .. note::

        This requires `winscp <https://winscp.net/eng/download.php>`_ to be
        downloaded for Windows machines, including the command-line utility

    .. note::

        This method calls the :file:`sync_output_to_remote.script` WinSCP
        script, which will actually sync the ``output`` directory with the
        :data:`destpath` path on the remote server. :data:`destpath` is set in
        the :mod:`secretconf` config file.

    TODO: Set up to work on OSX/Linux
    '''
     # Run pelican using the publish config file
    #local('pelican -s publishconf.py {PATH}'.format(**env))
    preview()

    ################
    # WINDOWS
    ################
    # Then push the output directory to the remote server, using winscp.com
    # which must be installed
    local('winscp.com /script=sync_output_to_remote.script /parameter ' \
            '// {username} {password} {hostname} {destpath}'.format(
                        username= production.split('@')[0],
                        password= env.password,
                        hostname= production.split('@')[1],
                        destpath= dest_path
                ))


    ################
    # OSX (probably Linux?)
    ################
    #: TODO: Figure out how to do this on Mac
