import os
from datetime import datetime
from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from dataservice.database import db, User, Run, Objective, Challenge

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


@api.operation('getUsers')
def get_users():
    users = db.session.query(User)
    page = 0
    page_size = 0
    if page_size:
        users = users.limit(page_size)
    if page != 0:
        # TODO: review this pagination
        users = users.offset(page * page_size)
    return jsonify([user.to_json() for user in users])


@api.operation('getUser')
def get_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    return user.to_json()


@api.operation('addUser')
def add_user():
    # Check if already exists
    existing = db.session.query(User).filter(User.email == request.json['email']).first()
    if existing:
        abort(409)

    # Create a new user
    user = User()
    user.email = request.json['email']
    user.firstname = request.json['firstname']
    user.lastname = request.json['lastname']
    user.age = request.json['age']
    user.weight = request.json['weight']
    user.max_hr = request.json['max_hr']
    user.rest_hr = request.json['rest_hr']
    user.vo2max = request.json['vo2max']
    db.session.add(user)
    db.session.commit()

    # Return the new id
    user_id = db.session.query(User).filter(User.email == user.email).first().id
    return {'user': user_id}


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
def get_runs():
    user_id = request.args.get('user_id')
    if not user_id:
        abort(400)
    runs = db.session.query(Run).filter(Run.runner_id == user_id)
    return jsonify([run.to_json() for run in runs])


@api.operation('getRun')
def get_run(run_id):
    run = db.session.query(Run).filter(Run.id == run_id)
    return run.to_json()


@api.operation('getObjectives')
def get_objectives(user_id):
    objectives = db.session.query(Objective).filter(Objective.runner_id == user_id)
    return jsonify([objective.to_json() for objective in objectives])


@api.operation('createObjective')
def create_objective(user_id):
    req = request.json.items()
    objective = Objective()
    objective.runner_id = user_id
    objective.name = req.name
    objective.target_distance = req.target_distance
    objective.start_date = req.start_date
    objective.end_date = req.end_date
    db.session.commit()
    return objective.to_json()


@api.operation('getObjective')
def get_objective(objective_id):
    objective = db.session.query(Objective).filter(Objective.id == objective_id)
    return objective.to_json()


@api.operation('getChallenges')
def get_challenges(user_id):
    challenges = db.session.query(Challenge).filter(Challenge.runner_id == user_id)
    return jsonify([challenge.to_json() for challenge in challenges])


@api.operation('createChallenge')
def create_challenge(user_id):
    req = request.json.items()
    challenge = Challenge()
    challenge.runner_id = user_id
    challenge.run_one = req.run_one
    challenge.name_run_one = req.name_run_one
    challenge.run_two = req.run_two
    challenge.name_run_two = req.name_run_two
    db.session.commit()
    return challenge.to_json()


@api.operation('getChallenge')
def get_challenge(challenge_id):
    challenge = db.session.query(Challenge).filter(Challenge.id == challenge_id)
    return challenge.to_json()
