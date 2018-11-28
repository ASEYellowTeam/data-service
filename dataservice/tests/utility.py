import pytest
import os
import tempfile
from dataservice.app import create_app
from dataservice.database import db, User


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
