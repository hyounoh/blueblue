from flask import make_response
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