import os
from flask import Flask
from dotenv import load_dotenv
from .models import db
from .scheduler import scheduler

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keep_going.db'
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