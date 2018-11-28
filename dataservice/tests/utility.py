import pytest
import os
import tempfile
from random import uniform, randint
from datetime import datetime
from dataservice.app import create_app
from dataservice.database import db, User, Run


@pytest.fixture
def client():
    """ This function initialize a new DB for every test and creates the app. This function returns a tuple,
    the first element is a test client and the second is the app itself. Test client must be used for sending
    request and the app should be used for getting a context when, for example, we need to query the DB.
    I haven't found a more elegant way to do this."""
    app = create_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.config['DATABASE']
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF validation -> DO THIS ONLY DURING TESTS!

    client = app.test_client()

    db.create_all(app=app)
    db.init_app(app=app)

    yield client, app

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def new_user(email=None):
    user = User()
    user.email = email if email is not None else 'mario@rossi.it'
    user.firstname = 'mario'
    user.lastname = 'rossi'
    user.age = 23
    user.weight = 70
    user.rest_hr = 60
    user.max_hr = 120
    user.vo2max = 0
    return user

def new_user_two():
    user = User()
    user.email = 'carlo@franchi.it'
    user.firstname = 'carlo'
    user.lastname = 'franchi'
    user.age = 30
    user.weight = 80
    user.rest_hr = 60
    user.max_hr = 120
    user.vo2max = 0
    return user

def new_run(user, strava_id=randint(100, 100000000), name=None, distance=uniform(50.0, 10000.0), elapsed_time=uniform(30.0, 3600.0),
            average_heartrate=None, total_elevation_gain=uniform(0.0, 25.0), start_date=datetime.now()):
    if name is None :
        name = "Run %s" % strava_id

    run = Run()
    run.runner = user
    run.strava_id = strava_id  # a random number 100 - 1.000.000, we hope is unique
    run.name = name
    run.distance = distance  # 50m - 10 km
    run.elapsed_time = elapsed_time  # 30s - 1h
    run.average_speed = run.distance / run.elapsed_time
    run.average_heartrate = average_heartrate
    run.total_elevation_gain = total_elevation_gain  # 0m - 25m
    run.start_date = start_date
    db.session.add(run)
    db.session.commit()
