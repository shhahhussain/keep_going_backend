from flask import Blueprint, request, jsonify, current_app
from .models import db, User
from .scheduler import scheduler
from .whatsapp_utils import send_whatsapp_message
from datetime import datetime, timedelta
import random

bp = Blueprint('main', __name__)

def get_default_brutal_messages():
    return [
        'You said you would do it. Why are you slacking?',
        'No excuses. Get it done.',
        'You are better than this. Move!'
    ]

def schedule_reminder(user):
    job_id = f'reminder_{user.phone_number}'
    scheduler.remove_job(job_id=job_id, jobstore=None, remove_all_jobs=False)
    scheduler.add_job(
        func=send_reminder,
        trigger='interval',
        minutes=user.interval,
        id=job_id,
        args=[user.phone_number],
        replace_existing=True
    )

def send_reminder(phone_number):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return
    now = datetime.utcnow()
    if (now - user.last_acknowledged_time).total_seconds() / 60 >= user.interval:
        if user.brutal_mode:
            brutal_messages = user.get_brutal_messages() or get_default_brutal_messages()
            message = random.choice(brutal_messages)
            send_whatsapp_message(user.phone_number, message)
        else:
            messages = user.get_messages()
            message = random.choice(messages)
            send_whatsapp_message(user.phone_number, message)

@bp.route('/start', methods=['POST'])
def start():
    data = request.json
    phone_number = data.get('phone_number')
    messages = data.get('messages')
    interval = data.get('interval')
    brutal_mode = data.get('brutal_mode', False)
    brutal_messages = data.get('brutal_messages', [])
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        user = User(phone_number=phone_number, interval=interval, brutal_mode=brutal_mode)
        user.set_messages(messages)
        if brutal_messages:
            user.set_brutal_messages(brutal_messages)
        db.session.add(user)
    else:
        user.interval = interval
        user.brutal_mode = brutal_mode
        user.set_messages(messages)
        if brutal_messages:
            user.set_brutal_messages(brutal_messages)
    db.session.commit()
    schedule_reminder(user)
    return jsonify({'status': 'started'})

@bp.route('/stop', methods=['POST'])
def stop():
    data = request.json
    phone_number = data.get('phone_number')
    user = User.query.filter_by(phone_number=phone_number).first()
    if user:
        job_id = f'reminder_{user.phone_number}'
        scheduler.remove_job(job_id=job_id, jobstore=None, remove_all_jobs=False)
    return jsonify({'status': 'stopped'})

@bp.route('/done', methods=['POST'])
def done():
    data = request.json
    phone_number = data.get('phone_number')
    user = User.query.filter_by(phone_number=phone_number).first()
    if user:
        user.last_acknowledged_time = datetime.utcnow()
        db.session.commit()
    return jsonify({'status': 'acknowledged'})

@bp.route('/status', methods=['GET'])
def status():
    phone_number = request.args.get('phone_number')
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({'status': 'not found'}), 404
    return jsonify({
        'phone_number': user.phone_number,
        'interval': user.interval,
        'brutal_mode': user.brutal_mode,
        'last_acknowledged_time': user.last_acknowledged_time.isoformat()
    }) 