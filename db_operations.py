import random

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, update

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def object_to_dict(self):
        cafe_dict = {}
        for key in vars(self):
            if str(key) == "_sa_instance_state":
                continue
            cafe_dict[str(key)] = str(vars(self)[key])
        return cafe_dict


no_of_cafes = 0


def select_all():
    with app.app_context():
        # all_cafes = db.session.execute(db.select(Cafe).order_by(asc(Cafe.id))).scalars()
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        global no_of_cafes
        no_of_cafes = len(all_cafes)
        return all_cafes


def random_cafe() -> Cafe:
    with app.app_context():
        all_cafes = select_all()
        r_cafe = random.choice(all_cafes)
        return r_cafe


def search(location) -> Cafe:
    with app.app_context():
        cafe_search = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()
        return cafe_search


def search_by_id(cafe_id):
    with app.app_context():
        cafe_search = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalars().all()
        return cafe_search
