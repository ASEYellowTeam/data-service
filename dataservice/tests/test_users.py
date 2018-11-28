from dataservice.tests.utility import client, new_user
from dataservice.database import db, User
import json


def test_add_user(client):
    tested_app, app = client

    user1 = new_user()
    json = user1.to_json()

    # inserting 'mario@rossi.it', the only one in DB
    assert tested_app.post('/users', json=json).status_code == 200

    # trying to add two times the same user
    assert tested_app.post('/users', json=json).status_code == 409

    # checking the correct insertion
    with app.app_context():
        user = db.session.query(User).filter(user1.email == User.email).first()
        assert user.email == user1.email
        assert user.age == user1.age
        assert user.firstname == user1.firstname
        assert user.lastname == user1.lastname
        assert user.max_hr == user1.max_hr
        assert user.rest_hr == user1.rest_hr
        assert user.weight == user1.weight
        assert user.vo2max == user1.vo2max


def test_get_users(client):
    tested_app, app = client

    user1 = new_user()
    user2 = new_user('marco@bianchi.it')
    user3 = new_user('paolo@verdi.it')
    user4 = new_user('matteo@gialli.it')

    users = [user1, user2, user3, user4]

    reply = tested_app.get('/users')

    assert reply.status_code == 200

    users_json = json.loads(str(reply.data, 'utf8'))

    assert users_json == []

    for user in users:
        assert tested_app.post('/users', json=user.to_json()).status_code == 200

    reply = tested_app.get('/users')

    users_json = json.loads(str(reply.data, 'utf8'))

    assert str(users_json) == "[{'age': 23, 'email': 'mario@rossi.it', 'firstname': 'mario', 'id': 1, " \
                              "'lastname': 'rossi', 'max_hr': 120, 'rest_hr': 60, 'strava_token': None, 'vo2max': 0.0, " \
                              "'weight': 70.0}, {'age': 23, 'email': 'marco@bianchi.it', 'firstname': 'mario', 'id': 2, " \
                              "'lastname': 'rossi', 'max_hr': 120, 'rest_hr': 60, 'strava_token': None, 'vo2max': 0.0, " \
                              "'weight': 70.0}, {'age': 23, 'email': 'paolo@verdi.it', 'firstname': 'mario', 'id': 3, " \
                              "'lastname': 'rossi', 'max_hr': 120, 'rest_hr': 60, 'strava_token': None, 'vo2max': 0.0, " \
                              "'weight': 70.0}, {'age': 23, 'email': 'matteo@gialli.it', 'firstname': 'mario', 'id': 4," \
                              " 'lastname': 'rossi', 'max_hr': 120, 'rest_hr': 60, 'strava_token': None, 'vo2max': 0.0," \
                              " 'weight': 70.0}]"


def test_get_user(client):
    tested_app, app = client

    user1 = new_user()
    user_json = user1.to_json()

    # getting non existing user
    reply = tested_app.get('/users/1')
    assert reply.status_code == 404

    # inserting 'mario@rossi.it', the only one in DB -> id=1
    assert tested_app.post('/users', json=user_json).status_code == 200

    reply = tested_app.get('users/1')
    users_json = json.loads(str(reply.data, 'utf8'))

    assert str(users_json) == "{'age': 23, 'email': 'mario@rossi.it', 'firstname': 'mario', 'id': 1, 'lastname': " \
                              "'rossi', 'max_hr': 120, 'rest_hr': 60, 'strava_token': None, 'vo2max': 0.0, " \
                              "'weight': 70.0}"


def test_set_token(client):
    tested_app, app = client

    # syntactically wrong request
    reply = tested_app.post('/users/1', json={})
    assert reply.status_code == 400

    # user 1 not existing
    reply = tested_app.post('/users/1', json={'strava_token': 'aaaaa'})
    assert reply.status_code == 404

    user1 = new_user()
    json = user1.to_json()

    # inserting 'mario@rossi.it', the only one in DB
    assert tested_app.post('/users', json=json).status_code == 200

    # correct request
    reply = tested_app.post('/users/1', json={'strava_token': 'aaaaa'})
    assert reply.status_code == 200

    user2 = new_user(email='paolo@rossi.it')
    json = user2.to_json()

    # inserting 'paolo@rossi.it'
    assert tested_app.post('/users', json=json).status_code == 200

    # two person with same token
    reply = tested_app.post('/users/2', json={'strava_token': 'aaaaa'})
    assert reply.status_code == 409


def test_delete_user(client):
    tested_app, app = client

    # user 1 not existing
    reply = tested_app.delete('/users/1')
    assert reply.status_code == 404

    user1 = new_user()
    json = user1.to_json()

    # inserting 'mario@rossi.it', the only one in DB
    assert tested_app.post('/users', json=json).status_code == 200

    # deleting correctly
    reply = tested_app.delete('/users/1')
    assert reply.status_code == 200

