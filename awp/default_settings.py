# Default Settings for AWP app

## Imports
from awp import app
import riak

class Config(object):
	"""docstring for Config"""
	DEBUG = False
	TESTING = False
	RIAK_HOST = '127.0.0.1'
	#RIAK_PORT = 8098
	RIAK_PORT = 8087
	RIAK_PREFIX ='riak'
	RIAK_TRANSPORT_CLASS=riak.RiakPbcTransport
	RIAK_BUCKET_PREFIX = ''
	SECRET_KEY = ''
		
class DevelopmentConfig(Config):
	DEBUG = True
	TESTING = True
	RIAK_HOST = '127.0.0.1'
	RIAK_PORT = 8087
	RIAK_PREFIX ='riak'
	RIAK_TRANSPORT_CLASS=riak.RiakPbcTransport
	RIAK_BUCKET_PREFIX = 'test_'