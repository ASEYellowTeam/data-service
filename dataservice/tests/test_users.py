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

