"""
WSGI config for diploma_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diploma_backend.settings')

application = get_wsgi_application()

"""Server configuration"""

# import os, sys
#
# virtenv = os.path.expanduser('~') + '/venv/'
# virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
# try:
#     if sys.version.split(' ')[0].split('.')[0] == '3':
#         exec(compile(open(virtualenv, "rb").read(), virtualenv, 'exec'), dict(__file__=virtualenv))
#     else:
#         execfile(virtualenv, dict(__file__=virtualenv))
# except IOError:
#     pass
# sys.path.append(os.path.expanduser('~'))
# sys.path.append(os.path.expanduser('~') + '/ROOT/backend/')
# sys.path.append(os.path.expanduser('~') + '/ROOT/backend/diploma_backend/')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'diploma_backend.settings'
# from django.core.wsgi import get_wsgi_application
#
# application = get_wsgi_application()
