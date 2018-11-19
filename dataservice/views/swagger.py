import os
from datetime import datetime

from flakon import SwaggerBlueprint
from flask import request, jsonify
from dataservice.database import db, User, Run


HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


@api.operation('getUsers')
def get_users():
    users = db.session.query(User)
    page = 0
    page_size = None
    if page_size:
        users = users.limit(page_size)
    if page != 0:
        # TODO: review this pagination
        users = users.offset(page * page_size)
    return [user.to_json() for user in users]


@api.operation('getUser')
def get_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    return user.to_json()


@api.operation('addUser')
def add_user():
    # Check if already exists
    existing = db.session.query(User).filter(User.email == request.json['email']).first()
    if existing:
        return {'user_id': -1}

    # Create a new user
    user = User()
    user.email = request.json['email']
    user.firstname = request.json['firstname']
    user.lastname = request.json['lastname']
    user.strava_token = request.json['strava_token']
    user.age = request.json['age']
    user.weight = request.json['weight']
    user.max_hr = request.json['max_hr']
    user.rest_hr = request.json['rest_hr']
    user.vo2max = request.json['vo2max']
    db.session.add(user)
    db.session.commit()

    # Return the new id
    user_id = db.session.query(User).filter(User.email == user.email).first().id
    return {'user_id': user_id}


@api.operation('deleteUser')
def delete_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True


@api.operation('addRuns')
def add_runs():
    added = 0
    for user, runs in request.json.items():
        runner_id = int(user)
        for run in runs:
            db_run = Run()
            db_run.strava_id = run['strava_id']
            db_run.distance = run['distance']
            db_run.start_date = datetime.fromtimestamp(run['start_date'])
            db_run.elapsed_time = run['elapsed_time']
            db_run.average_speed = run['average_speed']
            db_run.average_heartrate = run['average_heartrate']
            db_run.total_elevation_gain = run['total_elevation_gain']
            db_run.runner_id = runner_id
            db_run.title = run['title']
            db_run.description = run['description']
            db.session.add(db_run)

            added += 1

    if added > 0:
        db.session.commit()

    return {'added': added}


@api.operation('getRuns')
def get_runs(runner_id):
    runs = db.session.query(Run).filter(Run.runner_id == runner_id)
    return jsonify([run.to_json() for run in runs])
