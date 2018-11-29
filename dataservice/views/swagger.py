import os
from datetime import datetime
from flakon import SwaggerBlueprint
from flask import request, jsonify, abort, make_response
from dataservice.database import db, User, Run
import requests

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)

OBJECTIVESERVICE = os.environ['OBJECTIVE_SERVICE']
MAILSERVICE = os.environ['MAIL_SERVICE']
CHALLENGESERVICE = os.environ['CHALLENGE_SERVICE']


@api.operation('getUsers')
def get_users():
    users = db.session.query(User)
    page = 0
    page_size = 0
    if page_size:
        users = users.limit(page_size)  # pragma: no cover
    if page != 0:
        # TODO: review this pagination
        users = users.offset(page * page_size) # pragma: no cover
    return jsonify([user.to_json() for user in users])


@api.operation('getUser')
def get_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user is None:
        abort(404)
    return user.to_json()


@api.operation('addUser')
def add_user():
    # Check if already exists
    json = request.get_json()
    existing = db.session.query(User).filter(User.email == json['email']).first()
    print(existing)
    if existing is not None:
        abort(409)

    # Create a new user
    user = User()
    user.email = json['email']
    user.firstname = json['firstname']
    user.lastname = json['lastname']
    user.age = json['age']
    user.weight = json['weight']
    user.max_hr = json['max_hr']
    user.rest_hr = json['rest_hr']
    user.vo2max = json['vo2max']

    db.session.add(user)
    db.session.commit()

    # Return the new id
    user_id = db.session.query(User).filter(User.email == user.email).first().id
    return {'user': user_id}


@api.operation('setToken')
def set_token(user_id):
    strava_token = request.get_json()
    if not 'strava_token' in strava_token:
        abort(400)
    strava_token = strava_token['strava_token']

    existing = db.session.query(User).filter(User.strava_token == strava_token).first()
    if existing:
        abort(409)

    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        abort(404)

    user.strava_token = strava_token
    print(user)
    db.session.add(user)
    db.session.commit()
    return make_response('ok')


@api.operation('deleteUser')
def delete_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return abort(404)

    db.session.delete(user)
    db.session.commit()

    requests.delete(OBJECTIVESERVICE + '/objectives?user_id='+str(user_id))

    requests.delete(CHALLENGESERVICE + '/challenges?user_id=' + str(user_id))

    requests.delete(MAILSERVICE + '/reports?user_id=' + str(user_id))

    runs = db.session.query(Run.runner_id == user_id)

    for run in runs:
        db.session.delete(run)

    return make_response('ok')


@api.operation('addRuns')
def add_runs():
    added = 0
    for user, runs in request.json.items():
        runner_id = int(user)
        for run in runs:

            run_old = db.session.query(Run).filter(Run.strava_id == run['strava_id']).first()

            if run_old is not None:
                continue

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
def get_runs():
    user_id = request.args.get('user_id')
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        abort(400)
    
    runs = db.session.query(Run).filter(Run.runner_id == user_id)
    return jsonify([run.to_json() for run in runs])


@api.operation('getRun')
def get_run(run_id):
    run = db.session.query(Run).filter(Run.id == run_id).first()
    if not run:
        abort(404)
    return run.to_json()
