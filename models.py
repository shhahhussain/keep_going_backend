from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    messages = db.Column(db.Text, nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    brutal_mode = db.Column(db.Boolean, default=False)
    brutal_messages = db.Column(db.Text)
    last_acknowledged_time = db.Column(db.DateTime, default=datetime.utcnow)

    def get_messages(self):
        return json.loads(self.messages)

    def set_messages(self, messages_list):
        self.messages = json.dumps(messages_list)

    def get_brutal_messages(self):
        if self.brutal_messages:
            return json.loads(self.brutal_messages)
        return []

    def set_brutal_messages(self, messages_list):
        self.brutal_messages = json.dumps(messages_list) 