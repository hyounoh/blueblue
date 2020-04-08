from src import *
from collections import defaultdict

from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger


class Graph(Resource):
    @swagger.doc({
        "description": "get the number of petition by time-domain",
        "tags": ["Petition"],
        "parameters": [
            {
                "name": "recent",
                "type": "integer",
                "in": "query",
                "required": True,
                "description": "0 or 1, if true get the number of petition of last week (default: 1 True)"
            }
        ],
        "responses": {
            "200": {
                "description": "success",
                "examples": {
                    "application/json": {
                        "message": "success",
                        "results": [
                            {
                                "date": "date (ex. 2020-04-01)",
                                "count": "petition count"
                            }
                        ]
                    }
                }
            },
            "500": {
                "description": "error message",
                "examples": {
                    "application/json": {
                        "message": "error message"
                    }
                }
            }
        }
    })
    def get(self):

        # Check args
        parser = reqparse.RequestParser()
        parser.add_argument('recent', type=int)

        # Handle requested args
        args = parser.parse_args()
        recent = args.get('recent')

        # Compose petition-graph data
        petition_graph = mysql_controller.petition_graph(recent=recent)
        results = defaultdict(list)
        results['sum'] = sum(petition[1] for petition in petition_graph)
        results['graph'] = [{"date": petition[0], "count": petition[1]} for petition in petition_graph]

        # response
        return output_json({
            "message": "success",
            "results": results
        }, 200)
