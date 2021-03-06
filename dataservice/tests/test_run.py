from dataservice.tests.utility import client, new_user, new_user_two, new_run
from dataservice.database import db, Run
from datetime import datetime
import json
import requests
import requests_mock

def test_add_run(client):
    tested_app, app = client

    with app.app_context():

        runs = {

            1:
                [{"id": 1,
                "user_id": 1,
                "strava_id": 1936220842,
                "title": "Test Run",
                "distance": 50000.0,
                "description": None,
                "average_speed": 10.0,
                "elapsed_time": 5000.0,
                "total_elevation_gain": 3.0,
                "average_heartrate": None,
                "start_date": 1500000000.0,}]
        }

        # Test for adding a single run
        reply = tested_app.post('/runs',json=runs)
        assert reply.status_code == 200

        # Checking value of return
        run_json = json.loads(str(reply.data, 'utf8'))
        assert str(run_json) == "{'added': 1}"

        # Check that the run is added in the database
        with app.app_context():
            run_one = db.session.query(Run).filter(Run.id == 1).first()
            assert run_one is not None
            assert run_one.id == 1
            assert run_one.runner_id == 1
            assert run_one.title == "Test Run"
            assert run_one.distance == 50000.0
            assert run_one.description is None
            assert run_one.average_speed == 10.0
            assert run_one.elapsed_time == 5000.0
            assert run_one.total_elevation_gain == 3.0
            assert run_one.average_heartrate is None

            runs = {

                1:
                    [{"id": 1,
                      "user_id": 1,
                      "strava_id": 1936220842,
                      "title": "Test Run",
                      "distance": 50000.0,
                      "description": None,
                      "average_speed": 10.0,
                      "elapsed_time": 5000.0,
                      "total_elevation_gain": 3.0,
                      "average_heartrate": None,
                      "start_date": 1500000000.0, }],
                2:
                    [{
                      "id": 2,
                      "user_id": 2,
                      "strava_id": 2374629462,
                      "title": "Test Second Run",
                      "distance": 100000.0,
                      "description": None,
                      "average_speed": 8.0,
                      "elapsed_time": 4000.0,
                      "total_elevation_gain": 2.0,
                      "average_heartrate": None,
                      "start_date": 1100000000.0,}]
            }


            # Test: Add the second run, the first is already added
            reply_one = tested_app.post('/runs', json=runs)
            assert tested_app.post('/runs', json=runs).status_code == 200

            # Check the value in the response
            run_json = json.loads(str(reply_one.data, 'utf8'))
            assert str(run_json) == "{'added': 1}"

            # Check the insertion of the second run in the database
            run_two = db.session.query(Run).filter(Run.id == 2).first()
            assert run_two is not None
            assert run_two.id == 2
            assert run_two.runner_id == 2
            assert run_two.title == "Test Second Run"
            assert run_two.distance == 100000.0
            assert run_two.description is None
            assert run_two.average_speed == 8.0
            assert run_two.elapsed_time == 4000.0
            assert run_two.total_elevation_gain == 2.0
            assert run_two.average_heartrate is None

            # Test when all the runs are already added
            reply_two = tested_app.post('/runs', json=runs)
            assert tested_app.post('/runs', json=runs).status_code == 200

            # Check that the value is zero for runs added
            run_json = json.loads(str(reply_two.data, 'utf8'))
            assert str(run_json) == "{'added': 0}"

def test_get_runs(client):
    tested_app, app = client

    with app.app_context():

        # I create a first user with three runs
        user_one = new_user()
        new_run(user_one)
        new_run(user_one)
        new_run(user_one)

        # Get runs of an existing user
        reply = tested_app.get('/runs?user_id='+repr(user_one.id))
        assert reply.status_code == 200

        # Get runs of an not existing user
        reply_one = tested_app.get('/runs?user_id=5')
        assert reply_one.status_code == 400

        reply_two = tested_app.get('/runs')
        assert reply_two.status_code == 400

def test_get_run(client):

    tested_app, app = client

    with app.app_context():
        user = new_user()
        new_run(user)

        # Check of getting a not existing run
        assert tested_app.get('/runs/40').status_code == 404

        # Check of getting an existing run
        assert tested_app.get('/runs/1').status_code == 200
