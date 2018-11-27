from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    strava_token = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Numeric(4, 1))
    max_hr = db.Column(db.Integer)
    rest_hr = db.Column(db.Integer)
    vo2max = db.Column(db.Numeric(4, 2))

    def to_json(self):
        res = {}
        for attr in ('id', 'email', 'firstname', 'lastname', 'age', 'weight',
                     'max_hr', 'rest_hr', 'vo2max', 'strava_token'):
            value = getattr(self, attr)
            if isinstance(value, Decimal):
                value = float(value)
            res[attr] = value
        return res

    def get_id(self):
        return self.id


class Run(db.Model):
    __tablename__ = 'run'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(128))
    description = db.Column(db.Unicode(512))
    strava_id = db.Column(db.Integer)
    distance = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    elapsed_time = db.Column(db.Integer)
    average_speed = db.Column(db.Float)
    average_heartrate = db.Column(db.Float)
    total_elevation_gain = db.Column(db.Float)
    runner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    runner = relationship('User', foreign_keys='Run.runner_id')

    def to_json(self):
        res = {}
        for attr in ('id', 'strava_id', 'distance', 'start_date',
                     'elapsed_time', 'average_speed', 'average_heartrate',
                     'total_elevation_gain', 'runner_id', 'title',
                     'description'):
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            res[attr] = value
        return res


class Objective(db.Model):
    __tablename__ = 'objective'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    target_distance = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    runner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    runner = relationship('User', foreign_keys='Objective.runner_id')

    @property
    def completion(self):
        runs = db.session.query(Run) \
            .filter(Run.start_date > self.start_date) \
            .filter(Run.start_date <= self.end_date) \
            .filter(Run.runner_id == self.runner_id)

        return min(round(100 * (sum([run.distance for run in runs]) / (self.target_distance)), 2), 100)

    def to_json(self):
        res = {}
        for attr in ('id', 'name', 'target_distance', 'start_date',
                     'end_date', 'runner_id'):
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            res[attr] = value
        return res


# add the table Challenge
class Challenge(db.Model):
    __tablename__ = 'challenge'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_one = db.Column(db.Integer)
    name_run_one = db.Column(db.Unicode(128))
    run_two = db.Column(db.Integer)
    name_run_two = db.Column(db.Unicode(128))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', foreign_keys='Challenge.id_user')

    def set_challenge_user(self,id_usr):
        self.id_user = id_usr

    def set_challenge1_run(self,run_one):
        self.run_one = run_one

    def set_challenge2_run(self,run_two):
        self.run_two = run_two

    def set_challenge1_name(self,name_one):
        self.name_run_one = name_one

    def set_challenge2_name(self,name_two):
        self.name_run_two = name_two

    def to_json(self):
        res = {}
        for attr in ('id', 'run_one', 'name_run_one', 'run_two',
                     'name_run_two', 'id_user'):
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            res[attr] = value
        return res
