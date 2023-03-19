from flask import Flask
from flask_restful import Resource, Api
from flaskapp.resources import Login, Account
from flaskapp.models import db
from flaskapp.auth import bcrypt

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "hello world"

db.init_app(app)
bcrypt.init_app(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(Login, '/login')
api.add_resource(Account, '/account')

if __name__ == "__main__":
    app.run(debug=True)