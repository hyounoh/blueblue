from src import *
from collections import defaultdict

from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger


class Graph(Resource):
  @swagger.doc({
    "description": "get the number of petition by time-domain",
    "tags"       : ["Petition"],
    "parameters" : [
      {
        "name"       : "interval",
        "type"       : "integer",
        "in"         : "query",
        "required"   : True,
        "description": ""
      }
    ],
    "responses"  : {
      "200": {
        "description": "success",
        "examples"   : {
          "application/json": {
            "message": "success",
            "results": [
              {
                "date" : "date (ex. 2020-04-01)",
                "count": "petition count"
              }
            ]
          }
        }
      },
      "500": {
        "description": "error message",
        "examples"   : {
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
    parser.add_argument('interval', type=int)

    # Handle requested args
    args = parser.parse_args()
    interval = args.get('interval')
    if not interval: return output_json({"message": "no interval"}, 500)

    # Compose petition-graph data
    petition_graph = mysql_controller.read_graph(interval=interval)
    results = defaultdict(list)
    results['sum'] = sum(petition[1] for petition in petition_graph)
    results['graph'] = [{"date": petition[0], "count": petition[1]} for petition in petition_graph]
    results['graph'].reverse()

    # response
    return output_json({
      "message": "success",
      "results": results
    }, 200)


class Petition(Resource):
  @swagger.doc({
    "description": "get a list of petition",
    "tags"       : ["Petition"],
    "parameters" : [
      {
        "name"       : "keyword",
        "type"       : "string",
        "in"         : "query",
        "required"   : False,
        "description": "a keyword included in petition"
      },
      {
        "name"       : "limit",
        "type"       : "integer",
        "in"         : "query",
        "required"   : False,
        "description": "a number of petitions"
      },
      {
        "name"       : "interval",
        "type"       : "integer",
        "in"         : "query",
        "required"   : False,
        "description": ""
      }
    ],
    "responses"  : {
      "200": {
        "description": "success",
        "examples"   : {
          "application/json": {
            "message": "success",
            "results": [
              {
                "title"     : "title",
                "detail_url": "detail_url"
              }
            ]
          }
        }
      },
      "500": {
        "description": "error message",
        "examples"   : {
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
    parser.add_argument('keyword', type=str)
    parser.add_argument('limit', type=int)
    parser.add_argument('interval', type=int)

    # Handle requested args
    args = parser.parse_args()
    keyword = args.get('keyword')
    if not keyword: return output_json({"message": "no keyword"}, 500)
    interval = args.get('interval')
    if not interval: return output_json({"message": "no interval"}, 500)

    # Compose petition list
    petitions = mysql_controller.read_petitions(keyword=keyword, interval=interval)
    results = [{"title": petition[1], "url": petition[2]} for petition in petitions]

    # response
    return output_json({
      "message": "success",
      "results": results
    }, 200)
