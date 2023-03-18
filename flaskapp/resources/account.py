from flask_restful import Resource, reqparse
from flaskapp.models import User

login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'username',
    required=True,
)
login_parser.add_argument(
    'password',
    required='True'
)

sign_up_parser = login_parser.copy()

class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        
    
class SignUp(Resource):
    def post(self):
        args = sign_up_parser.parse_args()