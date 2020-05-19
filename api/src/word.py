from src import *

from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger


class WordCloud(Resource):
    @swagger.doc({
        "description": "get word cloud data from petition",
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
                "description": "the number of word (default: 10)"
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

        # Handle requested args
        args = parser.parse_args()
        use_stopword = args.get('use_stopword')
        limit = args.get('limit')

        # Compose wordcloud data
        words = mysql_controller.wordcloud(use_stopword=use_stopword, limit=limit)
        results = [{"word": word[0], "count": word[1]} for word in words]

        # response
        return output_json({
            "message": "success",
            "results": results
        }, 200)


class RecentWord(Resource):
    @swagger.doc({
        "description": "get recent top 3 word from petition last week",
        "tags": ["Word"],
        "parameters": [

        ],
        "responses": {
            "200": {
                "description": "success",
                "examples": {
                    "application/json": {
                        "message": "success",
                        "results": "word#1, word#2, word#3"
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

        # Handle requested args
        args = parser.parse_args()
        use_stopword = args.get('use_stopword')

        # Compose wordcloud data
        words = mysql_controller.recentword(use_stopword=use_stopword)
        words = [word[0] for word in words]
        words = ', '.join(words)
        results = words

        # response
        return output_json({
            "message": "success",
            "results": results
        }, 200)


class Stopword(Resource):
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

        # Compose wordcloud data
        stopword_id = mysql_controller.create_stopword(stopword)

        # response
        return output_json({
            "message": "success",
            "results": {
                "id": stopword_id,
                "stopword": stopword
            }
        }, 200)
