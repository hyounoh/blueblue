from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.word import *
from src.petition import *

app = Flask(__name__)

# Set CORS
cors = CORS(app, resources={r'*': {'origins': '*'}})

# Set limiter
limiter = Limiter(app, key_func=get_remote_address, default_limits=["1000 per day"])

# Set swagger
api = Api(app, title='API Template', api_version='0.0.1', api_spec_url='/swagger', host='localhost',
          description='API Template')

# Add resources
api.add_resource(Status, '/status')

api.add_resource(Graph, '/graph')
api.add_resource(Petition, '/petition')

api.add_resource(Word, '/word')
api.add_resource(Stopword, '/stopword')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
