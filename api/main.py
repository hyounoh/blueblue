from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src import *
from src.word import *
from src.petition import *

app = Flask(__name__)

# setting CORS
cors = CORS(app, resources={r'*': {'origins': '*'}})

limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per day"])

# setting swagger api doc
api = Api(app, title='API Template', api_version='0.0.1', api_spec_url='/swagger', host='localhost', description='API Template')

# add resources
# ex) http://localhost:5000/api_resource_name
api.add_resource(Status, '/status')
api.add_resource(WordCloud, '/wordcloud')
api.add_resource(Graph, '/petition-graph')
api.add_resource(Word, '/petition-word')
api.add_resource(RecentWord, '/recentword')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
