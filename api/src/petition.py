from src import *

from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger


class WordCloud(Resource):
    @swagger.doc({
        'description': 'get word cloud data from petition',
        'tags': ['Petition'],
        'parameters': [
            {
                "name": "use_stopword",
                "type": "integer",
                'in': "query",
                'required': True,
                "description": "decide to use stopword or not (default: True)"
            },
            {
                "name": "limit",
                "type": "integer",
                "in": "query",
                "required": True,
                "description": "the number of word (default: 10)"
            }
        ],
        'responses': {
            '200': {
                'description': 'success',
                'examples': {
                    'application/json': {
                        "message": 'success',
                        "results": [
                            {
                                "word": "word text",
                                "count": "word count"
                            }
                        ]
                    }
                }
            },
            '500': {
                'description': 'error message',
                'examples': {
                    'application/json': {
                        "message": 'error message'
                    }
                }
            }
        }
    })
    def get(self):

        # Check args
        parser = reqparse.RequestParser()
        parser.add_argument('use_stopword', type=int)
        parser.add_argument('limit', type=int)

        # Handle requested args
        args = parser.parse_args()
        use_stopword = args.get('use_stopword')
        limit = args.get('limit')

        # Compose wordcloud data
        results = []

        words = mysql_controller.wordcloud(use_stopword=use_stopword, limit=limit)
        for word in words:
            results.append({
                "word": word[0],
                "count": word[1]
            })

        # response
        return output_json({
            "message": 'success get',
            "results": results
        }, 200)
