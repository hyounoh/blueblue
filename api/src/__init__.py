from flask import make_response
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from libs.mysql_controller import MySQLController

import json

mysql_controller = MySQLController()


def output_json(data, code):
  """
  Makes a Flask response with a JSON encoded body
  """
  resp = make_response(json.dumps(data), code)
  resp.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
  resp.headers.extend({
    "content-type": "application/json"
  })
  return resp


class Status(Resource):
  @swagger.doc({
    "description": "get a status of api",
    "tags"       : ["Info"],
    "parameters" : [
    ],
    "responses"  : {
      "200": {
        "description": "success",
        "examples"   : {
          "application/json": {
            "message": "success"
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
    # response
    return output_json({
      "message": "success"
    }, 200)
