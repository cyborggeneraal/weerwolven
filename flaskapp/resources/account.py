from sqlite3 import IntegrityError
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flaskapp.models import User, db
from flaskapp.auth import generate_authtoken, login_required
from flaskapp.auth import bcrypt

login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'username',
    required=True,
)
login_parser.add_argument(
    'password',
    required=True
)

sign_up_parser = login_parser.copy()

login_fields = {
    'authtoken': fields.String(attribute=lambda x: x),
}

sign_up_fields = {
    'authtoken': fields.String(attribute=lambda x: x),
}

class Login(Resource):
    @marshal_with(login_fields)
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args.username).first()
        if not user or not bcrypt.check_password_hash(user.hashed_password, args.password):
            abort(401, message="Username or Password incorrect")
        token = generate_authtoken(user)
        return token
        
        
    
class Account(Resource):
    @marshal_with(sign_up_fields)
    def post(self):
        args = sign_up_parser.parse_args()
        hashed_password = bcrypt.generate_password_hash(args.password)
        user = User(username=args.username, hashed_password=hashed_password)
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            print(f"Integrity Error, this user is already in the database. Error: {e}")
            
            abort(500, message="Unexpected Error!")
        
        token = generate_authtoken(user)
        print(token)
        return token
    
    @login_required
    def put(self, user: User):
        return "hi"