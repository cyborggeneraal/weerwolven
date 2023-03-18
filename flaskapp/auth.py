from flask import request
from flask import current_app

from flaskapp.models import User

from datetime import datetime, timedelta
import jwt

def login_required(f):
    
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "")
        
    return _verify

def generate_authtoken(user: User):
    return jwt.encode(
        {
            "id": user.id,
            "start": datetime.utcnow(),
            "expiration": datetime.utcnow() + timedelta(hours=1)
        },
        current_app.config["SECRET_KEY"],
    )
        