from src import *

from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger


class Word(Resource):
  @swagger.doc({
    "description": "get word list used in petition",
    "tags": ["Word"],
    "parameters": [
      {
        "name": "use_stopword",
        "type": "integer",
        "in": "query",
        "required": True,
        "description": "0 or 1, decide to use stopword or not (default: 1 True)"
      },
      {
        "name": "limit",
        "type": "integer",
        "in": "query",
        "required": True,
        "description": "the number of word (default: 3)"
      },
      {
        "name": "interval",
        "type": "integer",
        "in": "query",
        "required": True,
        "description": ""
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
                "word": "word text",
                "count": "word count"
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
    parser.add_argument('use_stopword', type=int)
    parser.add_argument('limit', type=int)
    parser.add_argument('interval', type=int)

    # Handle requested args
    args = parser.parse_args()
    use_stopword = args.get('use_stopword')
    if not use_stopword: return output_json({"message": "no use_stopword"}, 500)
    limit = args.get('limit')
    if not limit: return output_json({"message": "no limit"}, 500)
    interval = args.get('interval')
    if not interval: return output_json({"message": "no interval"}, 500)

    # Compose wordcloud data
    words = mysql_controller.read_words(use_stopword=use_stopword, limit=limit, interval=interval)
    results = [{"word": word[0], "count": word[1]} for word in words]

    # response
    return output_json({
      "message": "success",
      "results": results
    }, 200)


class Stopword(Resource):
  @swagger.doc({
    "description": "create a stopword",
    "tags"       : ["Word"],
    "parameters" : [
      {
        "name"       : "stopword",
        "type"       : "string",
        "in"         : "query",
        "required"   : True,
        "description": "a word which not be used"
      },
    ],
    "responses"  : {
      "200": {
        "description": "success",
        "examples"   : {
          "application/json": {
            "message": "success",
            "results": "input stopword"
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
  def post(self):
    # Check args
    parser = reqparse.RequestParser()
    parser.add_argument('stopword', type=str)

    # Handle requested args
    args = parser.parse_args()
    stopword = args.get('stopword')
    if not stopword: return output_json({"message": "no stopword"}, 500)

    # Compose wordcloud data
    stopword_id = mysql_controller.create_stopword(stopword)

    # response
    return output_json({
      "message": "success",
      "results": {
        "id"      : stopword_id,
        "stopword": stopword
      }
    }, 200)

  @swagger.doc({
    "description": "get a list of stopword",
    "tags": ["Word"],
    "parameters": [

    ],
    "responses": {
      "200": {
        "description": "success",
        "examples": {
          "application/json": {
            "message": "success",
            "results": [
              "stopword #1",
              "stopword #2",
              "stopword #3",
              "stopword #n",
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
    # Compose wordcloud data
    words = mysql_controller.read_stopword()
    words = [word[1] for word in words]
    results = words

    # response
    return output_json({
      "message": "success",
      "results": results
    }, 200)
