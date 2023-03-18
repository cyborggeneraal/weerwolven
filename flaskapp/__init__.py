from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flaskapp.resources import Login

api = Api()
db = SQLAlchemy()

app = Flask(__name__)
db.init_app(app)
api.init_app(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Login, '/login')
api.add_resource(HelloWorld, '/')

if __name__ == "__main__":
    app.run(debug=True)