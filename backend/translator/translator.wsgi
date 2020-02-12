# https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/#working-with-virtual-environments
activate_this = '/var/www/api/translator/.venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/api/translator/')

# https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/#creating-a-wsgi-file
from translator import app as application