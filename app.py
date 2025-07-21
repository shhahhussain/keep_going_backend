import os
from flask import Flask
from dotenv import load_dotenv
from .models import db
from .scheduler import scheduler
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bigsur/Desktop/projects/personal projects/keep_going/keep_going_backend/instance/keep_going.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    from .routes import bp
    app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 