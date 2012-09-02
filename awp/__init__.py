# Imports
from flask import *
import riak


# Create the application
app = Flask(__name__)

# App imports

from awp import views, default_settings

# Configuration
#app.config.from_object('awp.default_settings.Config')
app.config.from_object('awp.default_settings.DevelopmentConfig')
#app.config.from_envvar('AWP_APP_SETTINGS', silent=True)

def get_riak_client():
 	g.rc = riak.RiakClient(host=app.config['RIAK_HOST'], port=app.config['RIAK_PORT'], prefix=app.config['RIAK_PREFIX'], transport_class=app.config['RIAK_TRANSPORT_CLASS'])

# set up connections etc
@app.before_request
def before_request():
	get_riak_client()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_page_not_found.html'), 404