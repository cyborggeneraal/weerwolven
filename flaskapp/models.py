from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String)
    
    def get_user(username = None, hashed_password = None):
        if not username or not hashed_password:
            return None
        
        return User.query.filter_by(username=username, hashed_password=hashed_password).first()