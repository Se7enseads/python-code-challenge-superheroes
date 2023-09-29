#!/usr/bin/env python3

from models import db, HeroPower
import os

from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from dotenv import load_dotenv

load_dotenv()


app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db" # os.getenv('DATABASE_URI)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


class Home(Resource):
    def get(self):
        heroes = HeroPower.query.all()

        heroes_data = []
        for hero in heroes:
            hero_data = {
                'id': hero.id,
                'strength': hero.strength
            }
            heroes_data.append(hero_data)

        return heroes_data, 200


api.add_resource(Home, '/')
