from flask import jsonify, request, current_app
from flask_restful import abort
from flask_bcrypt import Bcrypt

from flaskapp.models import User

from datetime import datetime, timedelta
import jwt

bcrypt = Bcrypt()

expired_msg = "Expired token. Reauthentication required"

def login_required(f):
    
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "")
        
        try:
            data = jwt.decode(
                auth_headers, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user = User.query.filter_by(id=data["id"]).first()
            if not user:
                raise RuntimeError("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            abort(401, message=expired_msg)
        
    return _verify

def generate_authtoken(user: User):
    return jwt.encode(
        {
            "id": user.id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        current_app.config["SECRET_KEY"],
    )
        