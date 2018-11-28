from dataservice.tests.utility import client, new_user
from dataservice.database import db, User
import requests
import requests_mock


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

